import argparse
import json
import requests
import requests.auth
import os, sys

# TODO: Hash these and unhash them to send
CLIENT_ID = "5f5qHORUv3wF94Djz7QFfQ"
CLIENT_SECRET = "qlYhkEfImnvpVW9vFmmzc0B07KwR_Q"
CLIENT_UN = "FairNeedleworker9516"
CLIENT_PW = "JLRMmZ'a0;W6fC?X)B*w/Qt&a"

BASE_URL = "https://oauth.reddit.com/r/"
NUM_POSTS = 100

def auth_request():
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": CLIENT_UN, "password": CLIENT_PW}
    headers = {"User-Agent": f"hw6-script by {CLIENT_UN}"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response


def reddit_request(auth_obj, url):
    print(f'Fetching from {url} using auth_obj {auth_obj["access_token"]}')
    token_type = auth_obj['token_type']
    access_token = auth_obj['access_token']
    headers = {"Authorization": f"{token_type} {access_token}", "User-Agent": f"hw6-script by {CLIENT_UN}"}
    payload = {"limit": NUM_POSTS, "type": "link"}
    response = requests.get(url, headers=headers, params=payload)
    return response


def get_top_posts_from_subreddit(subreddit):
    posts = []
    auth_obj = auth_request()
    r = reddit_request(auth_obj.json(), BASE_URL + subreddit + "/new.json")
    root_element = r.json()
    for post in root_element['data']['children']:
        posts.append(post)
    return posts


def dump_top_posts_from_subreddit_to_file(filename, subreddit):
    print(f"Grabbing newest {NUM_POSTS} from subreddit '{subreddit}', storing in {filename}...")
    posts = get_top_posts_from_subreddit(subreddit)
    with open(filename, 'w') as fh:
        fh.write("\n".join(json.dumps(post) for post in posts))
    print(f"Finished grabbing posts and writing file!") 


def main(args):
    dump_top_posts_from_subreddit_to_file(args.outputFile, args.subreddit)


## Usage
# python3 collect_newest.py -o <output_file> -s <subreddit>
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='collects 100 newest posts for specified subreddit, stores each post on own line as json in specified outpuf file.')
    parser.add_argument('-s',
            required=True,
            help='subreddit to grab posts from',
            type=str,
            dest='subreddit'
            )
    parser.add_argument('-o',
            required=True,
            help='output json file with newest posts stored as jsons on separate lines',
            type=str,
            dest='outputFile'
            )
    args = parser.parse_args()

    main(args)
