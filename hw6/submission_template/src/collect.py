import json
import requests
import requests.auth
import os, sys

# TODO: Hash these and unhash them to send
CLIENT_ID = "5f5qHORUv3wF94Djz7QFfQ"
CLIENT_SECRET = "qlYhkEfImnvpVW9vFmmzc0B07KwR_Q"
CLIENT_UN = "FairNeedleworker9516"
CLIENT_PW = "JLRMmZ'a0;W6fC?X)B*w/Qt&a"

BASE_URL = "https://oauth.reddit.com/r/aww/new.json"
CACHE_FILE = "new.cache.json"


def auth_request():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": CLIENT_UN, "password": CLIENT_PW}
    headers = {"User-Agent": f"hw6-script by {CLIENT_UN}"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response


def reddit_request(auth_obj):
    print(f'Fetching from {BASE_URL}')
    print(f'Using auth_obj {auth_obj}')
    token_type = auth_obj['token_type']
    access_token = auth_obj['access_token']
    headers = {"Authorization": f"{token_type} {access_token}", "User-Agent": f"hw6-script by {CLIENT_UN}"}
    response = requests.get(BASE_URL, headers=headers)
    return response


def main():

    if not os.path.exists(CACHE_FILE):
        auth_obj = auth_request()
        r = reddit_request(auth_obj.json())
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
