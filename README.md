# Job Scraping Task - Naukri.com

## 📌 Project Overview
This project scrapes recent job postings from **Naukri.com** using **Selenium** and **BeautifulSoup**. The extracted job data includes title, company name, location, job type, date posted, job description, and application links.

## 🚀 Features
- Extracts **recent job postings** (last 7 days).
- Captures **job title, company name, location, experience, job type, and application link**.
- Supports **pagination** for multiple job listings.
- Saves data in a structured **CSV file** for analysis.

## Tools Used
- **Python**
- **Selenium**
- **BeautifulSoup**
- **Pandas**
- **Chrome WebDriver**

## 📝 Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Naukri_Job_Scraper.git
   cd Naukri_Job_Scraper

## How to Run
1. Install required libraries:
   ```bash
   pip install -r requirements.txt

# 2. Ensure chromedriver is installed and set in the correct path.

# 3. Run the script:
 ```bash
    python main.py
```

# Output

-A CSV file named YourName_Naukri_Output.csv containing scraped job data.

-Errors (if any) logged in YourName_Errors.log.

#Assumptions and Limitations
Assumes the website's structure remains consistent.
Does not handle CAPTCHA or blocked requests.

