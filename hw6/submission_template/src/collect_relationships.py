import os, sys
import argparse
import bs4

# either get element from request or from cache if it exists
# wait let's plan this:

# if cache:
#   - beautiful soup on person_page that's in cache
# else:
#   - wget in python???
#   - CREATE HTML DUMP that "if cache" can use
#   - beautifulsoup, /dating/


def get_element(request):

    if not os.path.exists(CACHE_FILE):
        root_element = request.json()
        with open(CACHE_FILE, 'w') as fh:
            json.dump(root_element, fh)
    else:
        print('Loading from cache')
        with open(CACHE_FILE, 'r') as fh:
            root_element = json.load(fh)

    return root_element

def main(args):
    soup = bs4.BeautifulSoup(open(args.person_page_fname, 'r'), 'html.parser')

    age_div = soup.find('div', 'age')
    fact_div = age_div.find('div', 'fact')
    print(fact_div.string)


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
