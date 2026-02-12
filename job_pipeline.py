# job_pipeline.py
from scrapers.job_scraper_fake import scrape_fake
from scrapers.job_scraper_jobs_ac_uk import scrape_jobs_ac_uk
from scrapers.job_scraper_reed import scrape_reed

from job_filter import should_keep_job
import csv
import os
import time

# -----------------------------
# Output folder
# -----------------------------
OUTPUT_FOLDER = "output/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # create folder if it doesn't exist

# -----------------------------
# Write all jobs from list to TXT
# -----------------------------
def write_all_jobs_from_list(job_list, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for job in job_list:
            f.write("======\n")
            f.write(f"Source: {job['source']}\n")
            f.write(f"Title: {job['title']}\n")
            f.write(f"Description: {job['description']}\n")

# -----------------------------
# Read jobs from TXT
# -----------------------------
def read_jobs(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    jobs = content.split("======")
    return [job.strip() for job in jobs if job.strip()]

# -----------------------------
# Filter jobs
# -----------------------------
def filter_jobs(jobs):
    kept_jobs = []
    for job in jobs:
        if should_keep_job(job.lower()):
            kept_jobs.append(job)
    return kept_jobs

# -----------------------------
# Write filtered jobs to TXT
# -----------------------------
def write_filtered_jobs(jobs, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for job in jobs:
            f.write("======\n")
            f.write(job + "\n")

# -----------------------------
# CSV writing helper
# -----------------------------
def parse_job_block(job_text):
    """
    Convert a TXT-style job block into a dictionary.
    Cleans non-breaking spaces (\xa0) to normal spaces.
    """
    lines = job_text.splitlines()
    data = {}
    for line in lines:
        if line.startswith("Source:"):
            data["source"] = line.replace("Source:", "").strip()
        elif line.startswith("Title:"):
            data["title"] = line.replace("Title:", "").strip()
        elif line.startswith("Description:"):
            desc = line.replace("Description:", "").strip()
            data["description"] = desc.replace("\xa0", " ")  # clean non-breaking space
    return data

def write_filtered_jobs_csv(jobs, filename):
    """
    Write filtered jobs to CSV using UTF-8 BOM for Excel compatibility.
    Handles both TXT-style job blocks and dictionary jobs.
    """
    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["source", "title", "description"])
        writer.writeheader()
        for job in jobs:
            if isinstance(job, str):
                job_data = parse_job_block(job)
            else:
                job_data = job
                job_data["description"] = job_data.get("description", "").replace("\xa0", " ")
            writer.writerow(job_data)

# -----------------------------
# Multi-source scraping
# -----------------------------
def scrape_all_sources():
    all_jobs = []

    # 1️ Fake jobs (for testing)
    #print("Scraping fake jobs...")
    #all_jobs.extend(scrape_fake(max_pages=3))

    # 2️ jobs.ac.uk
    #print("Scraping jobs.ac.uk...")
    #all_jobs.extend(scrape_jobs_ac_uk(max_pages=5))

    print("Scraping Reed")
    all_jobs.extend(scrape_reed(max_pages=3))


    
    print(f"Total jobs scraped: {len(all_jobs)}")
    return all_jobs

# -----------------------------
# Main
# -----------------------------
def main():
    # 1️ Scrape jobs from all sources
    all_jobs = scrape_all_sources()
    print("DEBUG all_jobs length:", len(all_jobs))

    # 2️ Save all jobs to TXT
    write_all_jobs_from_list(all_jobs, f"{OUTPUT_FOLDER}jobs.txt")

    # 3️ Read jobs from TXT and filter
    jobs = read_jobs(f"{OUTPUT_FOLDER}jobs.txt")
    #filtered = filter_jobs(jobs)
    filtered=jobs

    # 4️ Write filtered jobs to TXT and CSV
    write_filtered_jobs(filtered, f"{OUTPUT_FOLDER}filtered_jobs.txt")
    write_filtered_jobs_csv(filtered, f"{OUTPUT_FOLDER}filtered_jobs.csv")

    # 5️ Done
    print(f"Done! Total jobs scraped: {len(all_jobs)}, Filtered jobs: {len(filtered)}")
    print(f"Check folder: {OUTPUT_FOLDER} for TXT and CSV files.")

# -----------------------------
# Run only if executed directly
# -----------------------------
if __name__ == "__main__":
    main()

