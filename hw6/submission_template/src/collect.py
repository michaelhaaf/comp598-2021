import json
import requests
import os, sys

BASE_URL = "https://www.reddit.com/r/aww/new.json"
CACHE_FILE = "new.cache.json"

def main():
    url = BASE_URL
    print(f'Getting url={url}')

    # TODO: authenticate so we don't keep getting blocked (agent_identifier)
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
