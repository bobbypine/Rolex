import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import config
from sqlalchemy import create_engine


urllib3.disable_warnings()


def prices(ref):
    price_list = []
    for x in range(1, 6):
        url = 'https://www.chrono24.com/search/index.htm?currencyId=USD&dosearch=true&facets=condition&facets=specials&facets=usedOrNew&facets=availability&maxAgeInDays=0&pageSize=120&query=Rolex+{}&redirectToSearchIndex=true&resultview=block&searchexplain=1&showpage={}&sortorder=0&specials=102&usedOrNew=new'.format \
            (ref, x)
        response = requests.get(url=url, verify=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        for prices in soup.findAll('strong')[5:]:
            price_list.append(prices.text)
    data = pd.DataFrame(price_list)
    data.rename(columns={0: ref}, inplace=True)
    data[ref] = data[ref].str.replace('\n', '').str.replace('$', '').str.replace(',', '').str.strip()
    data = data.loc[(data[ref].str.isnumeric())]
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
    ndsub = pd.DataFrame(prices('124060'))
    gmtii = pd.DataFrame(prices('126710BLNR'))
    exii = pd.DataFrame(prices('226570'))
    gsub = pd.DataFrame(prices('126610LV'))
    pricing = pd.concat([sub, gmt, op, ex, ndsub, gmtii, exii, gsub])
    median = pd.pivot_table(pricing, index='Date',
                            values=['126610LN', '126710BLRO', '124300', '124270', '124060', '126710BLNR', '226570',
                                    '126610LV'], aggfunc='median')
    listings = pd.pivot_table(pricing, index='Date', values=['126610LN Listings', '126710BLRO Listings',
                                                             '124300 Listings', '124270 Listings', '124060 Listings',
                                                             '126710BLNR Listings', '226570 Listings',
                                                             '126610LV Listings'], aggfunc='max')

    combined = pd.concat([median, listings], axis=1)
    combined['126610LN Markup'] = (combined['126610LN'] / 10100 - 1) * 100
    combined['126710BLRO Markup'] = (combined['126710BLRO'] / 10750 - 1) * 100
    combined['124300 Markup'] = (combined['124300'] / 6150 - 1) * 100
    combined['124270 Markup'] = (combined['124270'] / 7200 - 1) * 100
    combined['124060 Markup'] = (combined['124060'] / 8950 - 1) * 100
    combined['126710BLNR Markup'] = (combined['126710BLNR'] / 10750 - 1) * 100
    combined['226570 Markup'] = (combined['226570'] / 9500 - 1) * 100
    combined['126610LV Markup'] = (combined['126610LV'] / 10600 - 1) * 100
    saved_data = pd.read_csv('Prices/Weekly_Median_Prices.csv', index_col=0)
    saved_data = pd.concat([saved_data, combined])
    saved_data.to_csv('Prices/Weekly_Median_Prices.csv', index='Date')


def update_db():
    print('Updating Database...')
    new_data = pd.read_csv('Prices/Weekly_Median_Prices.csv').tail(1)
    engine = create_engine(config.api_key)
    with engine.connect() as conn:
        new_data.to_sql(
        "Weekly_Median_Prices.csv",
        conn,
        schema=f"{config.user_name}/rolex_prices",
        index=False,
        if_exists='append')
    conn.close()
    print('Database Updated!')


if __name__ == "__main__":
    run()
    update_db()

