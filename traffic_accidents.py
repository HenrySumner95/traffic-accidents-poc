import requests
from bs4 import BeautifulSoup
import pandas as pd

#Get Wikipedia page on global traffic accidents
website_url = (requests
               .get('https://en.wikipedia.org/wiki/List_of_countries_by_traffic-related_death_rate#List')
               .text)
soup = BeautifulSoup(website_url, 'lxml')
My_table = soup.find('table', {'class' : 'wikitable'})
items = My_table.findAll('td')

def divide_chunks(l, n): 
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

n = 7

item_list = list(divide_chunks(items, n))
        
df = pd.DataFrame()

columns = ['Country', 'Continent', 'Fatalities per 100K pop',
           'Fatalities per 100K vehicles', 'Fatalities per 1bil km',
           'Total fatalities latest year', 'Source year']

for i_list in item_list:
    row_dict = {}
    i = 0
    for i_item in i_list:
        #print(i_item)
        if 'flag' in str(i_item).split('>')[1]:
            row_dict.update({columns[i] : [str(i_item).split('title="')[1].split('">')[0]]})
        else:
            row_dict.update({columns[i] : [str(i_item).split('>')[1].split('<')[0]]})
        
        i += 1
            
    row_df = pd.DataFrame.from_dict(row_dict, orient = 'columns')
    df = df.append(row_df)

df = df.reset_index(drop = True)
#Get first four characters of year column
df['Source year'] = df['Source year'].str[:4]
#Remove commas from numerical fields
df['Total fatalities latest year'] = df['Total fatalities latest year'].str.replace(",", "")
#Rename columns
df = df.rename(columns = {'Fatalities per 100K pop'       : 'deaths_per_100k_capita',
                          'Fatalities per 1bil km'        : 'deaths_per_1bil_km',
                          'Fatalities per 100K vehicles'  : 'deaths_per_100k_vehicles',
                          'Total fatalities latest year'  : 'deaths_latest_year'})

df = df[:7]

df.to_csv("C:\\Users\\ashto\\work\\d3 basic\\traffic_accidents.csv", index = False)