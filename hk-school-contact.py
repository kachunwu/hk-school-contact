import requests
import re
import sqlite3
from bs4 import BeautifulSoup

# Define parameters
primary_url = "https://www.chsc.hk/psp2022/sch_detail.php?sch_id="
pri_id_list = list(range(1, 600))
secondary_url = "https://www.chsc.hk/ssp2022/sch_detail.php?sch_id="
sec_id_list = list(range(1, 600))
special_url = "https://www.chsc.hk/spsp/school_detail.php?sch_id="
spec_id_list = list(range(2800, 2901))
spec_id_list.append(7772)

# a function to extract the name and salutation from the whole cell
def name_str(input):
    try:
        str_index = re.search(r"先生", input).start() 
        output = input[0:str_index+2]
        return output
    except AttributeError:    
        try:
            str_index = re.search(r"女士", input).start()
            output = input[0:str_index+2]
            return output
        except AttributeError:
            try:
                str_index = re.search(r"博士", input).start()
                output = input[0:str_index+2]
                return output
            except AttributeError:
                try:
                    str_index = re.search(r"校長", input).start()
                    output = input[0:str_index+2]
                    return output
                except AttributeError:
                    try:
                        str_index = re.search(r"太平紳士", input).start()
                        output = input[0:str_index+4]
                        return output
                    except AttributeError:
                        try:
                            str_index = re.search(r"居士", input).start()
                            output = input[0:str_index+2]    
                            return output                                    
                        except:
                            try:
                                str_index = re.search(r"神父", input).start()
                                output = input[0:str_index+2]
                                return output
                            except:
                                try:
                                    str_index = re.search(r"修女", input).start()
                                    output = input[0:str_index+2]
                                    return output
                                except:
                                    try:
                                        str_index = re.search(r"小姐", input).start()
                                        output = input[0:str_index+2]
                                        return output
                                    except:                                    
                                        output = input
                                        return output

# setting up database
conn = sqlite3.connect('sch_contact.db')
c = conn.cursor()
create_table = 'CREATE TABLE school(chi_name TEXT, eng_name TEXT, district TEXT, address TEXT, phone TEXT, email TEXT, fax TEXT, website TEXT, supervisor TEXT, principal TEXT, sch_type TEXT, sch_sector TEXT, sch_gender TEXT, religion TEXT, record_url TEXT)'

try:
    c.execute(create_table)
except:
    print('Database already exists.')

# PRIMARY SCHOOL


for sch_id in pri_id_list:

    print(sch_id)

    URL = primary_url + str(sch_id)
    record_url = URL
    page = requests.get(URL, verify=False)

    sch_info = BeautifulSoup(page.content, "html.parser")

    try:
        sch_names = sch_info.find_all('dd', class_="xxzl-info-tit")
        sch_districts = sch_info.find_all('dd', class_="xxzl-info-bh")
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
        
        for sch_district in sch_districts:
            try:
                district_full = sch_district.text
                district_full_split = district_full.split('\xa0\xa0\xa0')
                district = re.sub(r'\n', '', district_full_split[0])
                #print(district)
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
                supervisor = name_str(supervisor)
                principal = re.sub(r"[^\w\s]", '', table_2[5].text)
                principal = name_str(principal)
                sch_type = '小學'
                sch_sector = re.sub(r"[^\w\s]", '', table_2[11].text)
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
        if all(v is not None for v in [chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url]):
            c.execute('''INSERT INTO school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url))
    except:
        c.execute('''INSERT INTO school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', ('', '', '', '', '', '', '', '', '', '', '中學', '', '', '',record_url))
        print('Empty record')
        continue
conn.commit()

## SECONDARY SCHOOL


for sch_id in sec_id_list:

    print(sch_id)

    URL = secondary_url + str(sch_id)
    record_url = URL
    page = requests.get(URL, verify=False)
    sch_info = BeautifulSoup(page.content, "html.parser")

    try:
        
        sch_names = sch_info.find_all('dd', class_="xxzl-info-tit")
        sch_districts = sch_info.find_all('dd', class_="xxzl-info-bh")
        sch_contacts = sch_info.find_all('dd', class_="xxzl-info-dz")
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
                continue


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
                continue    

        for detail in sch_details:
            
            try:
                table_2 = detail.find_all('td') 
                district = re.sub(r"[^\w]+", '', table_2[2].text)
                # supervisor = table_2[8].text
                supervisor = re.sub(r"[^\w]+", '', table_2[8].text)
                supervisor = name_str(supervisor)
                # principal = table_2[11].text
                principal = re.sub(r"[^\w]+", '', table_2[11].text)
                principal = name_str(principal)

                sch_type = '中學'
                sch_sector = re.sub(r"[^\w]+", '', table_2[14].text)
                sch_gender = re.sub(r"[^\w]+", '', table_2[17].text)
                religion = re.sub(r"[^\w]+", '', table_2[29].text)

                # print(supervisor)
                # print(principal)
                # print(sch_type)
                # print(sch_gender)
                # print(religion)
            except:
                continue    

        # Insert new record
        if all(v is not None for v in [chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url]):
            c.execute('''INSERT INTO school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url))
    except:
        c.execute('''INSERT INTO school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', ('', '', '', '', '', '', '', '', '', '', '中學', '', '', '',record_url))
        print('Empty record')
        continue
conn.commit()

# Special School

for sch_id in spec_id_list:

    print(sch_id)

    URL = special_url + str(sch_id)
    record_url = URL
    page = requests.get(URL, verify=False)
    sch_info = BeautifulSoup(page.content, "html.parser")

    try:
        
        sch_tables = sch_info.find_all('div', id="div_update_section_1")
        
        for sch_table in sch_tables:
        
            try:
                table_1 = sch_table.find_all('td') 
                chi_name = re.sub(r'\t', '', table_1[1].text)
                eng_name = re.sub(r'\t', '', table_1[3].text)
                address = re.sub(r'\t', '', table_1[5].text)
                district = re.sub(r'\t', '', table_1[9].text)
                phone = re.sub(r'\t', '', table_1[13].text)
                email = re.sub(r'\t', '', table_1[17].text)
                fax = re.sub(r'\t', '', table_1[15].text)
                website = re.sub(r'\t', '', table_1[19].text)
                supervisor = re.sub(r"[^\w]+", '', table_1[23].text)
                supervisor = name_str(supervisor)
                principal = re.sub(r"[^\w]+", '', table_1[25].text)
                principal = name_str(principal)                
                sch_type = '特殊學校 ('+ table_1[11].text+')'
                sch_sector = re.sub(r"[^\w]+", '', table_1[27].text)
                sch_gender = re.sub(r"[^\w]+", '', table_1[29].text)
                religion = re.sub(r"[^\w]+", '', table_1[33].text)

                # Insert new record
                if all(v is not None for v in [chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url]):
                    c.execute('''INSERT INTO school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url))
                    del chi_name, eng_name, district, address, phone, email, fax, website, supervisor, principal, sch_type, sch_sector, sch_gender, religion,record_url 
            except:
                print('Empty record')
                c.execute('''INSERT INTO school VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', ('', '', '', '', '', '', '', '', '', '', '中學', '', '', '',record_url))
                continue

    except:
        print('Empty record')
        continue

conn.commit()

# Clean empty records by deleting rows without school name
clean_table = 'DELETE FROM school WHERE chi_name=""'
c.execute(clean_table) 
conn.commit()

c.execute("""SELECT * FROM school""") # Select all records from table
results = c.fetchall()
print(results)
