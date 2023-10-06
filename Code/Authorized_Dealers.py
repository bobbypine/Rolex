import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import config


# Compiles and counts U.S.-based Rolex ADs

def list_convert(cell):
    if type(cell) == str:
        return cell
    else:
        return ' '.join(cell)


def ads():
    states = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
              "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
              "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
              "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
              "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
              "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
              "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
              "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
              "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
              "WI": "Wisconsin", "WY": "Wyoming"}

    data = pd.DataFrame()
    url = 'https://www.rolex.com/en-us/store-locator/unitedstates?lat=30.858763796809384&lng=-121.54549680328962&z=3'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    DRIVER_PATH = config.cd_path
    driver = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    names = []
    address = []
    country = []
    for x in soup.findAll('h2', {"class": "css-x99bf7 e89nfm54"}):
        names.append(x.text.encode('ascii', 'ignore').decode('ascii'))
    for x in soup.findAll('p', {"class": "css-1l2psjl e89nfm52"}):
        countries = x.text.strip()[-13:]
        country.append(countries)
        address.append(x.text.strip())
    data['Name'] = names
    data['Full Address'] = address
    data['Country'] = country
    data = data.loc[data.Country == 'United States']
    data['State'] = data['Full Address'].str[:-18].str.split(' ').str[-1]
    data.loc[data.State == '', 'State'] = data['Full Address'].str[:-18].str.split(' ').str[-2]
    data.loc[data['Full Address'].str.split(' ').str[-4].isin(['North', 'South', 'Rhode', 'New']), 'State']\
        = data['Full Address'].str.split(' ').str[-4:-2]
    data['State'] = data['State'].apply(list_convert)
    data['Zip'] = data['Full Address'].str.split(' ').str[-2].str.extract('(\d+)')
    data['Address'] = data['Full Address'].apply(lambda x: re.sub(r"(\w)([A-Z])", r"\1, \2", x))
    data['Test'] = (data.State.str.len() + 1 + data.Zip.str.len() + 1 + data.Country.str.len()) * -1  # finds the character length of the zip and state and removes it from address
    data['Address'] = data.apply(lambda row: row['Full Address'][:row['Test']], axis=1)
    data['City'] = data.Address.str.split(',').str[-1]
    data['City'] = data['Address'].apply(lambda x: re.findall('[A-Z][^A-Z\s]+(?:\s+\S[^A-Z\s]*)*', x)).str[-1]
    data['Test'] = (data.City.str.len()) * -1  # finds length of city and removes it
    data['Address'] = data.apply(lambda row: row['Address'][:row['Test']], axis=1)
    data.drop(columns=['Full Address', 'Test'], inplace=True)  # drops columns no longer needed
    data = data[['Name', 'Address', 'City', 'State', 'Zip']]
    data['State'] = data['State'].replace(states)
    data['ID'] = data.Name + data.Address + data.City + data.State + data.Zip
    data.ID = data.ID.str.replace(',', '').str.replace(' ', '').str.upper().str.strip()
    data.to_csv(f'../AD_List/Rolex_AD_List_{datetime.date.today().month}_{datetime.date.today().year}.csv', index=False)
    driver.quit()

def adcount():
    file = open('../AD_Count/AD_Count.txt', 'a')
    url = 'https://www.rolex.com/en-us/store-locator/unitedstates'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    DRIVER_PATH = config.cd_path
    driver = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    name_table = soup.findAll('h2', {"class": "css-x99bf7 e89nfm54"})
    print(len(name_table))
    file.write('{}/{}: {} \n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    print('File Updated.')
    print('{}/{}: {} \r\n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    file.close()
    driver.quit()


def adcount_test():  # allows you to see if a count is returned without amending the text file
    url = 'https://www.rolex.com/en-us/store-locator/unitedstates'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    DRIVER_PATH = config.cd_path
    driver = webdriver.Chrome(service=Service(DRIVER_PATH), options=options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    name_table = soup.findAll('h2', {"class": "css-x99bf7 e89nfm54"})
    print('{}/{}: {} \r\n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    driver.quit()

if __name__ == "__main__":
    # adcount_test()
    # adcount()
    ads()