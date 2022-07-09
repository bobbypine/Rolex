import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


# returns all Rolex model families
def all_watches():
    watches = []
    url = 'https://www.rolex.com/en-us/watches.html'
    response = requests.get(url, verify=True)
    soup = BeautifulSoup(response.text, 'html.parser')
    for x in soup.find_all('span', class_='sc-fzoLag sc-fznxsB cUWXFh sc-qYhBd gVLbVc')[:-6]:
        watch = x.text.strip()
        watches.append(watch)
        name = watch.lower().replace(' ', '-')
        link = f'https://www.rolex.com/en-us/watches/{name}/all-models.html#p=1'
    return watches


# returns names, references, and URLs for each Rolex model family
def scrape(model):
    model = model.lower().replace(' ','-')
    length = len(model) + 11
    pd.set_option('display.max_colwidth', None)
    data = pd.DataFrame()
    url2 = f'https://www.rolex.com/en-us/watches/{model.lower()}/all-models.html#p=1'
    response2 = requests.get(url2, verify=True)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    name = []
    spec = []
    link = []
    reference = []
    for x in soup2.find_all('h2', class_='sc-fzoLag sc-fzpjYC sc-qanuI dNwPNE'):
        name.append(x.text.strip())
    for x in soup2.find_all('span', class_='sc-fznKkj sc-fzoyAV fQsatj')[14:]:
        spec.append(x.text.strip())
    for x in soup2.find_all('a', class_='sc-fzpans cKJzHK sc-qQwsb kWQips wa-guidedsearch'):
        href = x['href']
        link.append(f'https://www.rolex.com/en-us{href}')
        reference.append(href[length:-5].upper())
    data['Name'] = name
    data['Description'] = spec
    data['Reference'] = reference
    data['Link'] = link
    return data


if __name__ == "__main__":
    with pd.ExcelWriter(f'../Models/All Rolex Models {datetime.datetime.today().month}.{datetime.datetime.today().year}.xlsx') as writer:
        total = pd.DataFrame()
        for x in all_watches():
            df = scrape(x)
            df.to_excel(writer, sheet_name = x, index=False)
            total = pd.concat([total, df])
        total.to_excel(writer, sheet_name='All Watches', index=False)