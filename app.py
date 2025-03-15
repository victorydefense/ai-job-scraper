from flask import Flask, render_template, send_file
import os
import subprocess
import csv

app = Flask(__name__)

# Paths
SCRAPER_SCRIPT = os.path.join(os.path.dirname(__file__), "scraper.py")
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/weworkremotely_jobs.csv")

def run_scraper():
    """Runs the job scraper before starting the app."""
    print("🔄 Running job scraper...")
    try:
        subprocess.run(["python", SCRAPER_SCRIPT], check=True)
        print("✅ Scraper completed successfully.")
    except Exception as e:
        print(f"❌ Error running scraper: {e}")

def get_job_listings():
    """Reads jobs from the CSV file and returns them as a list of dictionaries."""
    jobs = []
    if os.path.exists(CSV_FILE_PATH) and os.stat(CSV_FILE_PATH).st_size > 0:
        with open(CSV_FILE_PATH, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                jobs.append(row)
    return jobs

@app.route("/")
def home():
    """Main page with job listings and CSV download link."""
    if not os.path.exists(CSV_FILE_PATH) or os.stat(CSV_FILE_PATH).st_size == 0:
        run_scraper()  # Ensure we have data before rendering

    jobs = get_job_listings()
    
    # Generate the HTML page dynamically
    job_html = ""
    if jobs:
        job_html += "<ul>"
        for job in jobs:
            job_html += f'<li><a href="{job.get("URL", "#")}" target="_blank">{job["Title"]}</a> - {job["Company"]} ({job["Location"]})</li>'
        job_html += "</ul>"
    else:
        job_html = "<p>No jobs found.</p>"

    return f"""
    <h1>AI Job Scraper</h1>
    <p>Click below to download the latest job listings:</p>
    <a href='/download' download>
        <button>Download CSV</button>
    </a>
    <h2>Job Listings:</h2>
    {job_html}
    """

@app.route("/download")
def download():
    """Allows users to download the scraped job listings as CSV."""
    if os.path.exists(CSV_FILE_PATH) and os.stat(CSV_FILE_PATH).st_size > 0:
        return send_file(CSV_FILE_PATH, as_attachment=True)
    else:
        return "No job listings available yet. Try again later.", 404

if __name__ == "__main__":
    run_scraper()  # Run scraper on app start
    app.run(debug=True)