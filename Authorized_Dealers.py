import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import pandas as pd

urllib3.disable_warnings()


def ads():
    data = pd.DataFrame()
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    name_table = soup.findAll('p', {"class" : "sc-pRhbc ePDsLp"})
    address_table = soup.findAll('address', {"class" : "sc-oTzDS fotNMM"})
    data = data.append(name_table)
    data['Address'] = address_table
    data.rename(columns={0:'Name'}, inplace=True)
    data.sort_values('Name', ascending=True, inplace=True)
    print(data)


def adcount():
    file = open('AD_Count.txt', 'a')
    url = 'https://www.rolex.com/rolex-dealers/unitedstates.html#mode=list&placeId=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    name_table = soup.findAll('p', {"class" : "sc-pRhbc ePDsLp"})
    address_table = soup.findAll('address', {"class" : "sc-oTzDS fotNMM"})
    file.write('{}/{}: {} \n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    print('File Updated.')
    print('{}/{}: {} \r\n'.format(datetime.date.today().month, datetime.date.today().year, len(name_table)))
    file.close()


if __name__ == "__main__":
    adcount()