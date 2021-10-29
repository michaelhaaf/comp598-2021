import json
import requests
import requests.auth
import os, sys

# TODO: Hash these and unhash them to send
CLIENT_ID = "S-5YZ5hVQrvZzV8rogZsOQ"
CLIENT_SECRET = "QMHIOc5zwD70iQcuTVHJBhzQyTs8Xg"
CLIENT_UN = "williashatner"
CLIENT_PW = "q04qPk1ZjtZd"

BASE_URL = "https://www.reddit.com/r/aww/new.json"
CACHE_FILE = "new.cache.json"


def auth_request():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": CLIENT_UN, "password": "snoo"}
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response


def reddit_request():
    auth_obj = auth_request()
    #TODO use the auth obj
    headers = {"Authorization": "bearer fhTdafZI-0ClEzzYORfBSCR7x3M", "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

def main():
    url = BASE_URL
    print(f'Getting url={url}')

    if not os.path.exists(CACHE_FILE):
        print(f'Fetching from {url}')
        r = requests.get(url)
        root_element = r.json()
        with open(CACHE_FILE, 'w') as fh:
            json.dump(root_element, fh)
    else:
        print('Loading from cache')
        with open(CACHE_FILE, 'r') as fh:
            root_element = json.load(fh)

    posts = root_element['data']['children']

    for post in posts:
            print(post['data']['title'])

if __name__ == '__main__':
    main()
