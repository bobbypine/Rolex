import bs4
import requests
import webbrowser

personal = 'XojKdiU2bbMb1w'

secret = 'ctok-4bh8PtyT9SYpG_ILLZdiojtTQ'

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(personal, secret)

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'Bobby_Pine',
        'password': 'rjr2990'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/rolex/new",
                   headers=headers, params={'limit':'1000'})

for post in res.json()['data']['children']:
    if 'call' in post['data']['title'].lower():
        print('Title: {} Date: {}'. format(post['data']['title'], post['data']['created']))
