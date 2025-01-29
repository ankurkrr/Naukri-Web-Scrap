import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime, timedelta
import logging
import time

# Setup logging
logging.basicConfig(filename="AnkurKumar_Errors.log", level=logging.ERROR, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Set up WebDriver
service = Service(executable_path=r"chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open Naukri.com
driver.get("https://www.naukri.com/")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root')))

# Search for "Data Science" jobs
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div.qsbWrapper > div > div > div.keywordSugg > div > div > div > div:nth-child(1) > div > input'))
)
search_input.send_keys("Data Science")
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div.qsbWrapper > div > div > div.qsbSubmit'))
)
search_button.click()

# Scrape job postings from multiple pages
max_pages = 3
job_links = []

for current_page in range(0, max_pages + 1):
    print(f"Scraping page {current_page}...")
    soup = bs(driver.page_source, "lxml")
    postings = soup.find_all('div', class_='cust-job-tuple layout-wrapper lay-2 sjw__tuple')

    print(f"Number of job postings found: {len(postings)}")

    # Extract job links
    job_links += [post.find('a', class_='title').get('href') for post in postings]

    # Navigate to next page
    if current_page < max_pages:
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#lastCompMark > a:nth-child(4)"))
            )
            next_button.click()
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'cust-job-tuple'))
            )
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Error navigating to page {current_page}: {e}")
            break

def is_within_last_7_days(date_string):
    today = datetime.now()
    if "Today" in date_string or "Just now" in date_string:
        return True
    if "Yesterday" in date_string:
        return True  # Yesterday is within 7 days
    try:
        # Handle formats like "2 days ago" or "1 week ago"
        if "day" in date_string.lower():
            days = int("".join(filter(str.isdigit, date_string)))
            return (today - timedelta(days=days)) >= (today - timedelta(days=7))
        elif "week" in date_string.lower():
            weeks = int("".join(filter(str.isdigit, date_string)))
            days = weeks * 7
            return (today - timedelta(days=days)) >= (today - timedelta(days=7))
    except Exception as e:
        logging.error(f"Error parsing date '{date_string}': {e}")
    return False

# Scrape details for each job link
job_details = []

for link in job_links:
    try:
        driver.get(link)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Wait for specific elements to be present
        page_soup = bs(driver.page_source, "lxml")

        job_title = page_soup.find('h1', class_='styles_jd-header-title__rZwM1').text if page_soup.find('h1', class_='styles_jd-header-title__rZwM1') else "N/A"
        company = page_soup.find('div', class_='styles_jd-header-comp-name__MvqAI').a.text.strip() if page_soup.find('div', class_='styles_jd-header-comp-name__MvqAI') else "N/A"
        location = page_soup.find('span', class_='styles_jhc__location__W_pVs').text if page_soup.find('span', class_='styles_jhc__location__W_pVs') else "N/A"
        job_type = page_soup.find('div', class_='styles_details__Y424J').a.text if page_soup.find('div', class_='styles_details__Y424J') else "N/A"
        date_posted = page_soup.find('span', class_='styles_jhc__stat__PgY67').span.text if page_soup.find('span', class_='styles_jhc__stat__PgY67') else "N/A"
        description_div = page_soup.find('div', class_='styles_JDC__dang-inner-html__h0K4t')
        description = description_div.get_text(separator="\n").strip() if description_div else "N/A"

        if not is_within_last_7_days(date_posted):
            continue

        job_details.append({
            "Job Title": job_title,
            "Company Name": company,
            "Location": location,
            "Job Type": job_type,
            "Date Posted": date_posted,
            "Job Description": description,
            "Application Link": link,
        })
        logging.info(f"Scraped job: {job_title}")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Error loading page or finding elements for {link}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error scraping job details from {link}: {e}")

df = pd.DataFrame(job_details)
if df.duplicated().any():
    print("Duplicates found! Removing duplicate rows...")
    df.drop_duplicates(inplace=True)
else:
    print("No duplicates found.")

# Save the cleaned data to a CSV file
try:
    output_file = "AnkurKumar_Naukri_Output.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved successfully to '{output_file}'.")
    logging.info(f"Scraping completed. Data saved to '{output_file}'.")
except Exception as e:
    logging.error(f"Error saving data to CSV: {e}")
finally:
    driver.quit()

