# hk-school-contact
This is a python script for web scraping the Hong Kong school contacts (including address, phone, fax, email and website, etc.). Given my work requires to send mass email to all schools for promotional purposes, a reliable contact list of these schools is essential. This script helps me to generate such list with a simple button pressing.

# Work in Progress
1. Still waiting for the secondary school profiles for 2022-23.
2. Cross-check the number of schools with the Student Enrolment Statistics (2021/22) announced by Education Bureau.

## Data source
The Education Bureau of HKSAR updated their database of the all schools (including primary, secondary, and special schools) in Hong Kong. Given the URL of the profiles are composed of the identifier of each specific school, we can tell the excel to visit each profiles from the list and extract required information from the page automatically. If the government uses the same URL composition, in theory we can just renew the path to the newest database and the script will works fine with small modification.

## Output
The script create a .db file for each type of school. You can read the data by DB Browser.
