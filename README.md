# Job Scraping Task - Naukri.com

## Objective
-To scrape recent job postings from Naukri.com and extract key details such as job title, company name, location,  and more.

## Tools Used
- Python
- Selenium
- BeautifulSoup
- pandas

## How to Run
1. Install required libraries:
   ```bash
   pip install selenium beautifulsoup4 pandas

#2. Ensure chromedriver is installed and set in the correct path.

#3. Run the script:
 ```bash
    python main.py
```

#Output

A CSV file named YourName_Naukri_Output.csv containing scraped job data.
Errors (if any) logged in YourName_Errors.log.

#Assumptions and Limitations
Assumes the website's structure remains consistent.
Does not handle CAPTCHA or blocked requests.

