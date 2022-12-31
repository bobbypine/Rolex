import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import pandas as pd
import numpy as np
import config
from sqlalchemy import create_engine

# Collects pricing information for Rolex watches by reference number.
# To add a new reference just add the reference number to 'ref_list' and the reference and MSRP in dict form in 'ref_prices'

ref_list = ['126610LN', '126710BLRO', '124300', '124270', '124060', '126710BLNR', '226570', '126610LV', '116500LN',
            '126711CHNR', '126622', '126720VTNR']
ref_listings = [x + ' Listings' for x in ref_list]
ref_prices = {'126610LN': '10100', '126710BLRO': '10750 ', '124300': '6150', '124270': '7200', '124060': '8950',
              '126710BLNR': '10750', '226570': '9500', '126610LV': '10600', '116500LN': '14550', '126711CHNR': '15250',
              '126622': '12350', '126720VTNR': '11250'}


def prices(ref):
    price_list = []
    for x in range(1, 6):
        try:
            url = f'https://www.chrono24.com/search/index.htm?currencyId=USD&dosearch=true&facets=condition&facets=specials&facets=usedOrNew&facets=availability&maxAgeInDays=0&pageSize=120&query=Rolex+{ref}&redirectToSearchIndex=true&resultview=block&searchexplain=1&showpage={x}&sortorder=0&specials=102&usedOrNew=new'
            options = Options()
            options.headless = True
            options.add_argument("--window-size=1920,1200")
            DRIVER_PATH = config.cd_path
            driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
            driver.get(url)
            element = driver.find_elements(By.ID, "wt-watches")[0].get_attribute("innerHTML")
            soup = BeautifulSoup(element, 'html.parser')
            for items in soup.findAll('div', {'class': 'd-flex justify-content-between align-items-end m-b-2'}):
                for price in items.findAll('div', {'class': 'text-bold'}):
                    price_list.append(price.text.strip())
            driver.quit()
        except:
            break
    data = pd.DataFrame(price_list)
    data.rename(columns={0: ref}, inplace=True)
    data[ref] = data[ref].str.replace('\n', '', regex=False).str.replace('$', '', regex=False).str.replace(',', '',
                                                                                                           regex=False).str.strip()
    data = data.loc[(data[ref].str.isnumeric())]
    data[ref] = data[ref].astype('int')
    data[f'{ref} Listings'] = len(data)
    data['Date'] = datetime.date.today().strftime('%m/%d/%Y')
    data.set_index('Date', inplace=True)
    median = np.median(data[ref])
    print(f'{ref} Median Price: ${median}')
    print(f'{ref} Recorded {len(data)} Observations \r\n')
    return data


def run():
    pricing = pd.DataFrame()
    for x in ref_list:
        obs = prices(x)
        pricing = pd.concat([pricing, obs])
    median = pd.pivot_table(pricing, index='Date', values=[x for x in ref_list], aggfunc='median')
    listings = pd.pivot_table(pricing, index='Date', values=[x for x in ref_listings], aggfunc='max')
    combined = pd.concat([median, listings], axis=1)
    for x in ref_list:
        combined[f'{x} Markup'] = (combined[x] / int(ref_prices[x]) - 1) * 100
    saved_data = pd.read_csv('../Prices/Weekly_Median_Prices.csv', index_col=0)
    saved_data = pd.concat([saved_data, combined])
    saved_data.to_csv('../Prices/Weekly_Median_Prices.csv', index='Date')


def update_db():
    print('Updating Database...')
    new_data = pd.read_csv('../Prices/Weekly_Median_Prices.csv').tail(1)
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
