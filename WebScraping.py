import requests
import pandas as pd


class Rolex:
    def __init__(self):
        self.personal = ''
        self.secret = ''
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        self.auth = requests.auth.HTTPBasicAuth(self.personal, self.secret)
        # here we pass our login method (password), username, and password
        self.data = {'grant_type': 'password',
            'username': '',
            'password': ''}
        # setup our header info, which gives reddit a brief description of our app
        self.headers = {'User-Agent': 'MyBot/0.0.1'}
        # send our request for an OAuth token
        self.res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=self.auth, data=self.data, headers=self.headers)
        # convert response to JSON and pull access_token value
        self.TOKEN = self.res.json()['access_token']
        self.keylist = ['call ', 'called', 'picked up']

    def scrape(self, keyword):
        # add authorization to our headers dictionary
        authheaders = {**self.headers, **{'Authorization': f"bearer {self.TOKEN}"}}
        # while the token is valid (~2 hours) we just add headers=headers to our requests
        requests.get('https://oauth.reddit.com/api/v1/me', headers=authheaders)
        res = requests.get("https://oauth.reddit.com/r/rolex/new",
                   headers=authheaders, params={'limit':'100'})
        for post in res.json()['data']['children']:
            if keyword in post['data']['title'].lower():
                print(post['kind']+'_'+post['data']['id'], post['data']['title'], post['data']['created'], post['data']['thumbnail'])


if __name__ == '__main__':
    test = Rolex()
    for keyword in test.keylist:
        test.scrape(keyword)

