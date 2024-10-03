import re
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import json
import pandas as pd

from collections import defaultdict
import urllib.request

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


BASE_URL = "https://www.domain.com.au/rent/"

def get_vic_subs(aus_subs_file):
    sub = pd.read_csv(aus_subs_file)
    sub = sub[(sub['State'] == 'VIC') & (3000 <= sub['Zip']) & (sub['Zip'] <= 3999)].sort_values('Zip')
    sub[['Suburb', 'State']] = sub[['Suburb', 'State']].apply(lambda x: x.str.lower())
    sub['Suburb'] = sub['Suburb'].str.replace(' ', '-')
    sub['merge'] = sub[['Suburb', 'State', 'Zip']].astype(str).agg('-'.join, axis=1)
    s = sub['merge'].drop_duplicates()
    s.to_csv('../data/raw/suburb.txt', index=False, header=False)
    print(f"Succesfully get all the Victoria suburbs - Total: {len(s)}")


def get_vic_subs_as_csv(aus_subs_file):
    sub = pd.read_csv(aus_subs_file)
    sub = sub[(sub['State'] == 'VIC') & (3000 <= sub['Zip']) & (sub['Zip'] <= 3999)].sort_values('Zip')
    sub[['Suburb', 'State']] = sub[['Suburb', 'State']].apply(lambda x: x.str.lower())
    sub['Suburb'] = sub['Suburb'].str.replace(' ', ',')
    sub = sub[['Suburb', 'State', 'Zip']].drop_duplicates()
    sub.to_csv('../data/raw/vic_suburbs.csv', index=False, header=False)
    print(f"Succesfully get all the Victoria suburbs - Total: {len(sub)}")

def get_accessible_subs(vic_subs_file):
    sub_dict = {}

    with open(vic_subs_file, 'r') as f:    
        subs = f.readlines()

    subs = [sub.strip() for sub in subs]

    def check_url(sub):
        url = BASE_URL + sub + '/?ssubs=0'
        try:
            response = requests.get(url, headers={'User-Agent': "PostmanRuntime/7.6.0"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "lxml")
                script = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
                if script:
                    data = json.loads(script.string)
                    total_page = data["props"]["pageProps"]["layoutProps"]["digitalData"]["page"]["pageInfo"]["search"]["resultsPages"]
                if total_page >= 1:
                    sub_dict[sub] = total_page
                return True
            else:
                return False        
        except requests.exceptions.RequestException:
            return False

    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(check_url, subs), total=len(subs), desc="Checking URLs"))

    df = pd.DataFrame(list(sub_dict.items()), columns=['suburb', 'total_page'])
    df.to_csv('../data/raw/suburb_accessible.csv', index=False)
    f.close()
    print(f'Successfully get all the accessible suburbs - {len(sub_dict)} suburbs with >= 1 page')
    


