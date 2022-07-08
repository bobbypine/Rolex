import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import re


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
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    names = []
    address = []
    for x in soup.findAll('p', {"class": "sc-psOQA kGGsZi"}):
        names.append(x.text.strip())
    for x in soup.findAll('address', {"class": "sc-qXjgK sZlfd"}):
        address.append(x.text.strip()[:-13])
    data['Name'] = names
    data['Full Address'] = address
    data['State'] = data['Full Address'].str[:-5].str.split(' ').str[-1]
    data.loc[data.State == '', 'State'] = data['Full Address'].str[:-5].str.split(' ').str[-2]
    data.loc[data['Full Address'].str.split(' ').str[-3].isin(['North', 'South', 'Rhode', 'New']), 'State']\
        = data['Full Address'].str.split(' ').str[-3:-1]
    data['State'] = data['State'].apply(list_convert)
    data['State'] = data['State'].replace(states)
    data['Zip'] = data['Full Address'].str.split(' ').str[-1]
    data['Address'] = data['Full Address'].apply(lambda x: re.sub(r"(\w)([A-Z])", r"\1, \2", x))
    data['Test'] = (data.State.str.len() + 1 + data.Zip.str.len()) * -1  # finds the character length of the zip and state and removes it from address
    data['Address'] = data.apply(lambda row: row['Address'][:row['Test']], axis=1)
    data['City'] = data.Address.str.split(',').str[-1]
    data['Test'] = (1 + data.City.str.len()) * -1  # finds length of city and removes it
    data['Address'] = data.apply(lambda row: row['Address'][:row['Test']], axis=1)
    data.drop(columns=['Full Address', 'Test'], inplace=True)  # drops columns no longer needed
    data = data[['Name', 'Address', 'City', 'State', 'Zip']]
    data['ID'] = data.Name + data.Address + data.City + data.State + data.Zip
    data.ID = data.ID.str.replace(',', '').str.replace(' ', '').str.upper().str.strip()
    data.to_csv(f'../AD_List/Rolex_AD_List_{datetime.date.today().month}_{datetime.date.today().year}.csv', index=False)


def adcount():
    file = open('../AD_Count/AD_Count.txt', 'a')
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    name_table = soup.findAll('p', {"class": "sc-psOQA kGGsZi"})
    address_table = soup.findAll('address', {"class": "sc-qXjgK sZlfd"})
    file.write('{}/{}: {} \n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    print('File Updated.')
    print('{}/{}: {} \r\n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    file.close()


if __name__ == "__main__":
    adcount()
    ads()