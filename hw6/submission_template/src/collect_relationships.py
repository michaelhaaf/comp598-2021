import os, sys
import argparse
import bs4
import json

from pathlib import Path


BASE_URL="http://whosdatedwho.com/dating/"
ROOT_DIR = Path(__file__).parents[1].absolute()


def populate_cache_dir(config_dict):
    cache_loc = os.path.join(ROOT_DIR, config_dict['cache_dir'])

    p = Path(os.path.join(cache_loc))
    p.mkdir(parents=True, exist_ok=True)
    
    cmds = [f"wget {BASE_URL + person} -O {os.path.join(cache_loc, person)}" for person in config_dict['target_people']]
    run_cmds = lambda cmd: os.system(cmd)
    
    map(run_cmds, cmds)
    return None


def extract_page_files_from_cache(config_dict):
    return {}


def get_relationships(person_page_fname):
    soup = bs4.BeautifulSoup(open(person_page_fname, 'r'), 'html.parser')
    age_div = soup.find('div', 'age')
    fact_div = age_div.find('div', 'fact')
    return [fact_div.string]


def main(args):

    # read config file to dict
    with open(args.configFile, 'r') as fh:
        config_dict = json.load(fh)

    # if cache_dir doesn't exist, create it (dl file for each target person)
    ## TODO: refactor to method, so that actors are actually looked at
    # if not os.path.exists(config_dict['cache_dir']):
        populate_cache_dir(config_dict)

    person_file_map = extract_page_files_from_cache(config_dict)

    # for each target person, read info from cache.
    output = { person: get_relationships(person_page_fname) for person, person_page_fname in person_file_map.items() }

    # publish dict to json
    with open(args.outputFile, 'w') as fh:
        json.dump(output, fh)


## Usage
# python3 collection_relationships.py -c <config-file.json> -o <output_file.json>
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
