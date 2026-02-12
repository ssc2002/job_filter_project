import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.jobs.ac.uk/search/?page={}"

def scrape_jobs_ac_uk(max_pages=3):
    print("Scraping jobs.ac.uk...")
    all_jobs = []

    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Fetching jobs.ac.uk page {page}: {url}")

        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("div", class_="j-search-result__result")
        if not job_cards:
            print("No more jobs found. Stopping.")
            break

        for card in job_cards:

            # -------- TITLE & LINK --------
            link_tag = card.find("a")
            title = link_tag.text.strip() if link_tag else "No title"
            job_url = "https://www.jobs.ac.uk" + link_tag["href"] if link_tag else None

            # -------- EMPLOYER --------
            employer_tag = card.find("div", class_="j-search-result__employer")
            employer = employer_tag.text.strip() if employer_tag else "Unknown employer"

            # -------- LOCATION --------
            location = "Unknown location"
            for div in card.find_all("div"):
                if "Location:" in div.text:
                    location = div.text.replace("Location:", "").strip()

            # -------- SALARY --------
            salary = "No salary info"
            salary_div = card.find("div", class_="j-search-result__info")
            if salary_div:
                salary = salary_div.get_text(" ", strip=True).replace("Â", "").replace("\xa0", " ").strip()

            # -------- FULL DESCRIPTION --------
            full_description = ""
            if job_url:
                detail_resp = requests.get(job_url, headers=headers)
                detail_resp.encoding = "utf-8"
                detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                about_div = detail_soup.find("div", class_="job-description")  # main content container
                if about_div:
                    full_description = about_div.get_text(" ", strip=True)

                time.sleep(0.5)  # polite delay per job

            # -------- BUILD DESCRIPTION FIELD --------
            description = f"Employer: {employer}. Location: {location}. Salary: {salary}. About the role: {full_description}"

            # -------- FINAL JOB DICTIONARY --------
            job = {
                "source": "jobs.ac.uk",
                "title": title,
                "description": description
            }

            all_jobs.append(job)

        time.sleep(1)  # polite delay per page

    print(f"Total jobs scraped from jobs.ac.uk: {len(all_jobs)}")
    return all_jobs
