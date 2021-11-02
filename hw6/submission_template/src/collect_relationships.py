import os, sys
import argparse
import bs4
import json
import requests
import shutil

from json import JSONDecodeError
from pathlib import Path


BASE_URL="http://whosdatedwho.com/dating/"
ROOT_DIR = Path(__file__).parents[1].absolute()


def populate_cache_dir(config_dict):
    
    print(f"Checking cache at {config_dict['cache_dir']}...")
    if not os.path.exists(config_dict['cache_dir']):
        print(f"No cache found, creating directory...")
    else:
        print(f"Cache exists, will double check to make sure there is a cached file for each target person...")

    cache_loc = os.path.join(ROOT_DIR, config_dict['cache_dir'])

    p = Path(os.path.join(cache_loc))
    p.mkdir(parents=True, exist_ok=True)
    
    for person in config_dict['target_people']: 
        person_page_fname = os.path.join(cache_loc, person)
        if not os.path.exists(person_page_fname):
            print(f"Downloading whodatedwho info for {person} to location {person_page_fname}...")
            with requests.get(BASE_URL + person, stream=True) as r:
                with open(person_page_fname, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print(f"Download successful for {person} to {person_page_fname}!")
        else:
            print(f"Cache already exists for {person} in cache dir {cache_loc}!")

    return None


def extract_page_files_from_cache(config_dict):
    cache_loc = os.path.join(ROOT_DIR, config_dict['cache_dir'])
    return {person : os.path.join(cache_loc, person) for person in config_dict['target_people']} 


def get_relationships(person_page_fname):
    soup = bs4.BeautifulSoup(open(person_page_fname, 'r'), 'html.parser')
    data = soup.select("[type='application/ld+json']")[0]

    result = [] 
    try:
        relationships_list = json.loads(data.text)
    except JSONDecodeError as e:
        print(f"Error: malformed relationship json for {person_page_fname}, will report empty list for target")
        return result

    try:
        result = [relationship['item']['name'] for relationship in relationships_list["itemListElement"]]
    except KeyError as e:
        print(f"Warning: no relationship information for {person_page_fname}, will report empty list for target") 

    return result


def main(args):

    # read config file to dict
    with open(args.configFile, 'r') as fh:
        config_dict = json.load(fh)

    populate_cache_dir(config_dict)
    print(f"Cache ready, extracting relationship data...")

    person_file_map = extract_page_files_from_cache(config_dict)
    output = {person: get_relationships(person_page_fname) for person, person_page_fname in person_file_map.items()}

    print(f"Writing relationship data to {args.outputFile}...")
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
