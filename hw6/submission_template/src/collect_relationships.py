import os, sys
import argparse
import bs4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('person_page_fname')
    args = parser.parse_args()

    soup = bs4.BeautifulSoup(open(args.person_page_fname, 'r'), 'html.parser')

    age_div = soup.find('div', 'age')
    fact_div = age_div.find('div', 'fact')
    print(fact_div.string)


if __name__ == '__main__':
    main()
