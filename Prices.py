import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np


urllib3.disable_warnings()


def prices(ref):
    price_list = []
    for x in range(1 ,6):
        url = 'https://www.chrono24.com/search/index.htm?currencyId=USD&dosearch=true&facets=condition&facets=specials&facets=usedOrNew&facets=availability&maxAgeInDays=0&pageSize=120&query=Rolex+{}&redirectToSearchIndex=true&resultview=block&searchexplain=1&showpage={}&sortorder=0&specials=102&usedOrNew=new'.format \
            (ref ,x)
        response = requests.get(url=url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        for prices in soup.findAll('strong')[5:]:
            price_list.append(prices.text)
    data = pd.DataFrame(price_list)
    data.rename(columns={0 :ref}, inplace=True)
    data[ref] = data[ref].str.replace('\n', '').str.replace('$', '').str.replace(',' ,'').str.strip()
    data = data.loc[(data[ref] != 'Price on request') & (data[ref] != 'SOLD')]
    data[ref] = data[ref].astype('int')
    data[f'{ref} Listings'] = len(data)
    data['Date'] = datetime.date.today().strftime('%m-%d-%Y')
    data.set_index('Date', inplace=True)
    median = np.median(data[ref])
    print(f'{ref} Median Price: ${median}')
    print(f'{ref} Recorded {len(data)} Observations \r\n')
    return data


def run():
    sub = pd.DataFrame(prices('126610LN'))
    gmt = pd.DataFrame(prices('126710BLRO'))
    op = pd.DataFrame(prices('124300'))
    ex = pd.DataFrame(prices('124270'))
    pricing = pd.concat([sub, gmt, op, ex])
    median = pd.pivot_table(pricing, index='Date', values=['126610LN', '126710BLRO', '124300', '124270'],
                              aggfunc='median')
    listings = pd.pivot_table(pricing, index='Date', values=['126610LN Listings', '126710BLRO Listings',
                                                             '124300 Listings', '124270 Listings'], aggfunc='max')
    combined = pd.concat([median,listings], axis=1)
    combined.to_csv('Prices/Weekly_Median_Prices.csv')


if __name__ == "__main__":
    run()