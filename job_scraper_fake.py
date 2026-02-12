# job_scraper_fake.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://realpython.github.io/fake-jobs/"

def scrape_fake(max_pages=None):
    """
    Scrapes all job postings from Fake Jobs site across multiple pages.
    
    Args:
        max_pages (int, optional): maximum number of pages to scrape. None = all pages.
        
    Returns:
        List of job dicts: {"source", "title", "description"}
    """
    all_jobs = []
    page_num = 1

    while True:
        if page_num == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}page/{page_num}/"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"No more pages found at page {page_num}. Stopping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="card-content")
        if not job_cards:
            print(f"No jobs found on page {page_num}. Stopping.")
            break

        for card in job_cards:
            title_elem = card.find("h2", class_="title")
            company_elem = card.find("h3", class_="company")
            location_elem = card.find("p", class_="location")
            description_elem = card.find("p", class_="description")

            title = title_elem.get_text(strip=True) if title_elem else "No title"
            company = company_elem.get_text(strip=True) if company_elem else "Unknown company"
            location = location_elem.get_text(strip=True) if location_elem else "Unknown location"
            description = description_elem.get_text(strip=True) if description_elem else ""

            job_dict = {
                "source": "Fake Jobs",
                "title": f"{title} at {company} ({location})",
                "description": description
            }
            all_jobs.append(job_dict)

        print(f"Scraped {len(job_cards)} jobs from page {page_num}.")
        page_num += 1

        if max_pages and page_num > max_pages:
            break

    print(f"Total jobs scraped: {len(all_jobs)}")
    return all_jobs
