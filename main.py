from datetime import datetime
from prettytable import PrettyTable
import requests
from bs4 import BeautifulSoup


def get_url(position,location):
    template='https://internshala.com/jobs/{}-jobs-in-{}/'
  
    url=template.format(position,location)
    return url
position = input("Enter job position: ")
location = input("Enter job location: ")
url = get_url(position, location)
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')
cards = soup.find_all('div', class_='container-fluid individual_internship visibilityTrackerItem')

if len(cards) == 0:
    print("No job posts found for the specified location or job name.")
else:
    card=cards[0]
    def get_record(card):
        atag=card.h3.a
        job_title=atag.text
        job_url='https://internshala.com'+atag.get('href')
        company_name=card.find('h4',class_='heading_6 company_name').text.strip()
        job_location=card.find('a',class_='location_link view_detail_button').text.strip()
        try:
            post_date=card.find('div',class_='status-container').text
        except AttributeError:
            post_date = 'NOT MENTIONED'      
        today=datetime.today().strftime('%D')
  
        salary=card.find('div',class_='item_body salary').text.strip()
   
        record=(job_title,company_name,job_location,salary,job_url, post_date,today)    
        return record

records=[]

for card in cards:
    record=get_record(card)
    records.append(record)
headers = ["Profile", "Company Name", "Job Location", "CTC", "Job URL", "Post Date","date"]
table = PrettyTable(headers)
table.add_rows(records)
table.border = True
table.align = 'l'
table.max_width["Profile"] = 40 
table.max_width["Company Name"] = 30 
table.max_width["Post Date"] = 12
table.max_width["CTC"] = 20
table.max_width["date"] = 12
table.max_width["Job URL"] = 50
print(table)








   





