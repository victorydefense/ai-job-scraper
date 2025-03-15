import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Debugging Screenshot Path
DEBUG_SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), "../data/debug_screenshot.png")

# CSV File Path
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/weworkremotely_jobs.csv")

# URL to scrape
URL = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"

def take_debug_screenshot(driver):
    """Saves a screenshot for debugging purposes"""
    driver.save_screenshot(DEBUG_SCREENSHOT_PATH)
    print(f"✅ Debug screenshot saved at: {DEBUG_SCREENSHOT_PATH}")

def scrape_jobs():
    """Scrapes job listings from WeWorkRemotely and saves them to a CSV file."""
    print("🔍 Starting job scraping...")

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(URL)
        time.sleep(3)  # Allow time for the page to load

        # Save debug screenshot
        take_debug_screenshot(driver)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()  # Close the browser

        job_listings = []

        # Find job listing sections
        job_sections = soup.find_all("li", class_="feature")

        for job in job_sections:
            try:
                title = job.find("h4").text.strip()
                company = job.find("p", class_="new-listing__company-name").text.strip()
                location = job.find("p", class_="new-listing__company-headquarters").text.strip()
                job_listings.append({"Title": title, "Company": company, "Location": location})
            except AttributeError:
                continue

        # Save to CSV
        df = pd.DataFrame(job_listings)
        df.to_csv(CSV_FILE_PATH, index=False)
        print(f"✅ Saved {len(job_listings)} jobs to {CSV_FILE_PATH}")

    except Exception as e:
        print(f"❌ Error scraping jobs: {e}")

if __name__ == "__main__":
    scrape_jobs()