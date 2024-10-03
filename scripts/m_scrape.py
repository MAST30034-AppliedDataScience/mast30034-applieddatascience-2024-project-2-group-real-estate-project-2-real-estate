import re
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from json import dump, loads
import pandas as pd
import time

from collections import defaultdict
import urllib.request

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from utilities import get_vic_subs, get_accessible_subs

# constants
BASE_URL = "https://www.domain.com.au"

# Get accessible Victoria suburbs
get_vic_subs('../australian-postcodes-2021-04-23.csv')
get_accessible_subs('../data/raw/suburb.txt')


df = pd.read_csv('../data/raw/suburb_accessible.csv')

property_metadata = defaultdict(dict)

def scrape_suburb_data(sub):
    # begin code
    url_links = []

    # generate list of urls to visit
    for page in range(1, df.loc[df['suburb'] == sub, 'total_page'].values[0] + 1):
        url = BASE_URL + f"/rent/{sub}/?ssubs=0&sort=price-desc&page={page}"
        try:
            bs_object = BeautifulSoup(urlopen(Request(url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
            # find the unordered list (ul) elements which are the results, then
            # find all href (a) tags that are from the base_url website.
            index_links = bs_object \
                .find(
                    "ul",
                    {"data-testid": "results"}
                ) \
                .findAll(
                    "a",
                    href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
                )

            for link in index_links:
                # if its a property address, add it to the list
                if 'address' in link['class']:
                    url_links.append(link['href'])
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code} with {url}")
        except Exception as e:
            print(f"Issue with {url}: {e}")
    
    def scrape_features(property_url):
        try: 
            bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
            # looks for the header class to get property name
            property_metadata[property_url]['name'] = bs_object \
                .find("h1", {"class": "css-164r41r"}) \
                .text

            # looks for the div containing a summary title for cost
            property_metadata[property_url]['cost_text'] = bs_object \
                .find("div", {"data-testid": "listing-details__summary-title"}) \
                .text

            # get rooms and parking
            rooms = bs_object \
                    .find("div", {"data-testid": "property-features"}) \
                    .findAll("span", {"data-testid": "property-features-text-container"})

            property_metadata[property_url]['rooms'] = [
                re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
                if 'Bed' in feature.text or 'Bath' in feature.text
            ]
        
            
            # parking
            property_metadata[property_url]['parking'] = [
                re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
                if 'Parking' in feature.text
            ]
            
            # type
            property_metadata[property_url]['type'] = bs_object \
                .find("div", {"data-testid": "listing-summary-property-type"}) \
                .text
                
            
            # schools with distance <= 2.5km
            script = bs_object.find('script', {'id': '__NEXT_DATA__'})
            if script:
                json_content = script.string.strip()
                data = loads(json_content)
                schools = data.get('props', {}).get('pageProps', {}).get('componentProps', {}).get('schoolCatchment', {}).get('schools', [])
                num_schools = sum(1 for school in schools if school['distance'] <= 2500)
                property_metadata[property_url]['schools'] = num_schools
                    
            # description
            property_metadata[property_url]['desc'] = re \
                .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
                .strip('</p>')
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code} with {property_url}")  
        except AttributeError:
            print(f"Issue with {property_url}")
       
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(scrape_features, url_links), total=len(url_links), desc="Scraping Properties"))

subs = df['suburb'].tolist()

with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(scrape_suburb_data, subs), total=len(subs), desc="Scraping Suburbs"))

# output to json file in data/raw/
with open('../data/raw/current_rent_info.json', 'w') as f:
    dump(property_metadata, f)
