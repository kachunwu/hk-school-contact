# hk-school-contact (HK School Contact Web Scraper)
This is a python script for web scraping the Hong Kong school contacts (including address, phone, fax, email and website, etc.). Given my work requires to send mass email to all schools for promotional purposes, a reliable contact list of these schools is essential. This script helps me to generate such list with a simple button pressing.

## Known Issue
- Still waiting for the secondary school profiles for 2022-23.
- Still need to cross-check the number of schools with the Student Enrolment Statistics (2021/22) announced by Education Bureau as the number of schools may not fit.
- The names extracted from the website may not be sufficiently cleaned because of the variety of salutations. Also the script cannot handle English names which require manual cleaning.

## Data source
The Education Bureau of HKSAR updated their database of the all schools (including primary, secondary, and special schools) in Hong Kong. Given the URL of the profiles are composed of the identifier of each specific school, we can tell the excel to visit each profiles from the list and extract required information from the page automatically. If the government uses the same URL composition, in theory we can just renew the path to the newest database and the script will works fine with small modification.

## Output
The script create a .db file with the table SCHOOL. You can read the data by DB Browser.
