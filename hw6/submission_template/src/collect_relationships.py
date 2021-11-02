import os, sys
import argparse
import bs4
import json
import requests
import shutil

from pathlib import Path


BASE_URL="http://whosdatedwho.com/dating/"
ROOT_DIR = Path(__file__).parents[1].absolute()


def populate_cache_dir(config_dict):
    cache_loc = os.path.join(ROOT_DIR, config_dict['cache_dir'])

    p = Path(os.path.join(cache_loc))
    p.mkdir(parents=True, exist_ok=True)
    
    for person in config_dict['target_people']: 
        person_page_fname = os.path.join(cache_loc, person)
        print(f"Downloading whodatedwho info for {person} to location {person_page_fname}...")
        with requests.get(BASE_URL + person, stream=True) as r:
            with open(person_page_fname, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        print(f"Download successful for {person} to {person_page_fname}!")

    return None


def extract_page_files_from_cache(config_dict):
    cache_loc = os.path.join(ROOT_DIR, config_dict['cache_dir'])
    return {person : os.path.join(cache_loc, person) for person in config_dict['target_people']} 


def get_relationships(person_page_fname):



    soup = bs4.BeautifulSoup(open(person_page_fname, 'r'), 'html.parser')
    data = soup.select("[type='application/ld+json']")[0]
    oJson = json.loads(data.text)["itemListElement"]
    numRelations = len(oJson)
    results = []

    for product in oJson:
        results.append(product['item']['name'])

    return results


def main(args):

    # read config file to dict
    with open(args.configFile, 'r') as fh:
        config_dict = json.load(fh)

    # if cache_dir doesn't exist, create it (dl file for each target person)
    print(f"Checking cache at {config_dict['cache_dir']}...")
    if not os.path.exists(config_dict['cache_dir']):
        print(f"No cache found at {config_dict['cache_dir']}, populating cache by downloading from {BASE_URL}...")
        populate_cache_dir(config_dict)
    print(f"Cache found, extracting relationship data...")

    person_file_map = extract_page_files_from_cache(config_dict)

    # for each target person, read info from cache.
    output = { person: get_relationships(person_page_fname) for person, person_page_fname in person_file_map.items() }

    # publish dict to json
    with open(args.outputFile, 'w') as fh:
        json.dump(output, fh)


## Usage
# python3 collect_relationships.py -c <config-file.json> -o <output_file.json>
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='collects relationships for target people given in input json file. see args for details')
    parser.add_argument('-c',
            required=True,
            help='json config file with cache_dir and target_people keys',
            type=str,
            dest='configFile'
            )
    parser.add_argument('-o',
            required=True,
            help='output config file with target_people keys (enumerates their relationships)',
            type=str,
            dest='outputFile'
            )
    args = parser.parse_args()

    main(args)
