# scrapers/job_scraper_reed.py

import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.reed.co.uk/jobs?page={}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_reed(max_pages=3):
    print("Scraping Reed...")
    all_jobs = []

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Fetching Reed page {page}: {url}")

        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        # Each job card on Reed
        job_cards = soup.find_all("article", class_="job-result")

        if not job_cards:
            print("No more jobs found on Reed.")
            break

        for card in job_cards:
            # -------------------
            # TITLE + LINK
            # -------------------
            title_tag = card.find("h2")
            if not title_tag:
                continue

            link_tag = title_tag.find("a")
            if not link_tag:
                continue

            title = link_tag.text.strip()
            job_url = "https://www.reed.co.uk" + link_tag["href"]

            # -------------------
            # Fetch job detail page
            # -------------------
            job_response = requests.get(job_url, headers=HEADERS)
            job_soup = BeautifulSoup(job_response.text, "html.parser")

            # Full description block
            desc_div = job_soup.find("div", class_="job-description")

            if desc_div:
                description = desc_div.get_text(" ", strip=True)
            else:
                description = "No description found"

            job = {
                "source": "reed",
                "title": title,
                "description": description
            }

            all_jobs.append(job)

            time.sleep(0.5)  # polite delay per job

        time.sleep(1)  # polite delay per page

    print(f"Total jobs scraped from Reed: {len(all_jobs)}")
    return all_jobs
