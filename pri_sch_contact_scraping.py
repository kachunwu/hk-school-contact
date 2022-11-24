import requests
import re
import sqlite3
from bs4 import BeautifulSoup

# setting up database
conn = sqlite3.connect('sch_contact.db')
c = conn.cursor()
c.execute('''CREATE TABLE pri_school(chi_name TEXT, eng_name TEXT, address TEXT, phone TEXT, email TEXT, fax TEXT, website TEXT, supervisor TEXT, principal TEXT, sch_type TEXT, sch_gender TEXT, religion TEXT, record_url TEXT)''')

# web scraper
for sch_id in range(1, 600):

    print(sch_id)

    URL = "https://www.chsc.hk/psp2022/sch_detail.php?sch_id=" + str(sch_id)
    record_url = URL
    page = requests.get(URL, verify=False)

    sch_info = BeautifulSoup(page.content, "html.parser")

    sch_names = sch_info.find_all('dd', class_="xxzl-info-tit")
    sch_contacts = sch_info.find_all('dd', class_="xxzl-info-dz c")
    sch_details = sch_info.find_all('dd', class_="xmcslr01")


    for sch_name in sch_names:
        
        try:
            sch_name_full = sch_name.text
            # print(sch_name_full)
            sch_name_sep = sch_name_full.splitlines()
            # print(sch_name_sep)
            chi_name = re.sub(r'\t', '', sch_name_sep[1])
            eng_name = re.sub(r'\t', '', sch_name_sep[2])
        except:
            break

    for contact in sch_contacts:

        try:
            table_1 = contact.find_all('td') 
            
            address = table_1[1].text
            phone = table_1[3].text
            email = table_1[6].text
            fax = table_1[8].text
            website = table_1[11].text

            # print(address)
            # print(phone)
            # print(email)
            # print(fax)
            # print(website)
        except:
            break    

    for detail in sch_details:
        
        try:
            table_2 = detail.find_all('td') 
        
            supervisor = table_2[2].text
            principal = re.sub(r"[^\w\s]", '', table_2[5].text)
            sch_type = re.sub(r"[^\w\s]", '', table_2[11].text)
            sch_gender = table_2[14].text
            religion = table_2[20].text

            # print(supervisor)
            # print(principal)
            # print(sch_type)
            # print(sch_gender)
            # print(religion)
        except:
            break    
    
    # Insert new record
    if all(v is not None for v in [chi_name, eng_name, address, phone, email, fax, website, supervisor, principal, sch_type, sch_gender, religion,record_url]):
        c.execute('''INSERT INTO pri_school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (chi_name, eng_name, address, phone, email, fax, website, supervisor, principal, sch_type, sch_gender, religion,record_url))

conn.commit()

c.execute('''SELECT * FROM pri_school''')
results = c.fetchall()
print(results)
