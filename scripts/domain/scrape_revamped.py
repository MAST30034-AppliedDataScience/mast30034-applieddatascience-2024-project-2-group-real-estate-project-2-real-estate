"""
A very simple, naive, and basic web scraping script. This will not
work completely and is only applicable to domain.com.

Feel free to use this as a source of inspiration, it is by no means production code.
"""

"""
We need to first get a list of every single property that needs to be scraped into a file. This will
require using different search parameters to make this work.

Then from there we need to 
"""


# built-in imports
import re
import os
import csv
from math import ceil
from json import dump
from tqdm import tqdm

from collections import defaultdict
import urllib.request

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# constants
BASE_URL = "https://www.domain.com.au"

# directory constants
DIRECTORY = './data/raw/domain'
METADATA_DIRECTORY = DIRECTORY + '/metadata'
PAGE_DIRECTORY = DIRECTORY + '/pages'

LISTINGS_PER_PAGE = 20

N_PAGES = range(1, 50) # update this to your liking


# create folders if they don't exist
if not os.path.exists(METADATA_DIRECTORY):
    os.makedirs(METADATA_DIRECTORY)
if not os.path.exists(PAGE_DIRECTORY):
    os.makedirs(PAGE_DIRECTORY)


# begin code
url_links = []


# HELPER FUNCTIONS
# ----------------

def get_search_url_for_price_range(price_min, price_max):
    return f'{BASE_URL}/rent/?price={price_min}-{price_max}&state=vic&sort=price-desc'


def get_number_in_price_range(price_min, price_max):
    url = get_search_url_for_price_range(price_min, price_max)
    print(f"Visiting {url}")

    # load the webpage and parse it as a beautiful soup object
    bs_object = BeautifulSoup(urlopen(Request(url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
    
    # get the number of results
    results_text = bs_object.find('h1', class_='css-ekkwk0').find('strong').text.strip()

    number_of_results = int(re.search(r'\d+', results_text).group())
    return number_of_results

def write_to_csv(path, data):
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def readlines_from_file(path):
    with open(path, 'r') as file:
        return file.readlines()

def write_to_file(path, data):
    with open(path, 'w') as file:
        for line in data:
            file.write(line + '\n')

# data is a list of lines (strings)
def append_to_file(path, data):
    with open(path, 'a') as file:
        for line in data:
            file.write(line + '\n')

def append_to_csv(path, data):
    with open(path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def read_from_csv(path):
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        return [row for row in reader]



# the lower bound of the final bin
FINAL_BIN_LOWER = 50000

TARGET_NUMBER = 950

# split up the number of requests into x bins
def bin_results(min_price, max_price, number_of_bins_per_split, max_bin_frequency):
    """
    number_to_split: how many equal width bins to try and split it into
    """
    bin_frequency = get_number_in_price_range(min_price, max_price)

    if bin_frequency <= max_bin_frequency:
        return [(min_price, max_price, bin_frequency)]
    else:
        bin_width = (max_price - min_price) / number_of_bins_per_split
        res = []
        for i in range(number_of_bins_per_split):
            # should be the larger of the two
            range_min = int(min_price + i * bin_width)
            range_max = int(min_price + (i + 1) * bin_width) - 1

            # for the end of the final range, should be exactly equal to the max price
            range_max = max_price if (i == number_of_bins_per_split - 1) else range_max

            res += bin_results(range_min, range_max, number_of_bins_per_split, max_bin_frequency)

        return res
    

RANGE_MIN_INDEX = 0
RANGE_MAX_INDEX = 1
NUMBER_LISTINGS_INDEX = 2

def merge_bins(binned_results):
    """
    Takes in the binned results and merges adjacent ones together so there's less bins.
    """

    # next step is to merge the bins where possible so they are still under the limit
    prelim_splits = sorted(binned_results.copy())

    i = 0
    while i < len(prelim_splits) - 1:
        merged_count = prelim_splits[i][NUMBER_LISTINGS_INDEX] + prelim_splits[i + 1][NUMBER_LISTINGS_INDEX]
        if merged_count <= TARGET_NUMBER:
            # merge the two listing bins if possible
            prelim_splits[i] = (prelim_splits[i][RANGE_MIN_INDEX], prelim_splits[i + 1][RANGE_MAX_INDEX], merged_count)
            prelim_splits.pop(i + 1)
        else:
            i += 1

    return prelim_splits
    

price_splits_path = METADATA_DIRECTORY + '/price_splits.csv'

if os.path.exists(price_splits_path):
    print("Already saved splits, reading from csv.")
    price_bins = read_from_csv(price_splits_path)
else:
    print("Getting price bins for search.")
    # 1: get the set of bins
    price_bins = bin_results(0, FINAL_BIN_LOWER, 6, TARGET_NUMBER)

    # 2: add the final bin
    price_bins += [(FINAL_BIN_LOWER + 1, "any", get_number_in_price_range(FINAL_BIN_LOWER + 1, "any"))]

    # 3: merge the splits
    price_bins = merge_bins(price_bins)
    print("Fetched base urls with total listings of:", sum(i[2] for i in price_bins))

    # 3: save the splits to a csv so the script doesn't need to be ran again
    # CSV with schema of start price, end price, number of listings in that range
    write_to_csv(METADATA_DIRECTORY + '/price_splits.csv', price_bins)


def download_listing_links(price_bins, url_links_path):

    url_links = []

    for bin in price_bins:

        url_bin_links = []

        num_listings = get_number_in_price_range(bin[RANGE_MIN_INDEX], bin[RANGE_MAX_INDEX])

        num_pages = ceil(num_listings / LISTINGS_PER_PAGE)
        print(num_pages)

        # generate list of urls to visit
        for page in range(1, num_pages + 1):
            url = get_search_url_for_price_range(bin[RANGE_MIN_INDEX], bin[RANGE_MAX_INDEX]) + f'&page={page}'
            print(f"Visiting {url}")
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
                    url_bin_links.append(link['href'])

        append_to_file(url_links_path, url_bin_links)

        url_links += url_bin_links

        print(f"Saved {len(url_bin_links)} new links. Total is {len(url_links)}")

    return url_links


# STEP 2: GET ALL URLS FOR THE LISTINGS
# -------------------------------------

url_links_path = METADATA_DIRECTORY + '/listings_links.csv'

if os.path.exists(url_links_path):
    print("Already saved listing urls. Reading from list.")
    listing_urls = readlines_from_file(url_links_path)
else:
    print("Searching for listing urls and saving to file.")
    listing_urls = download_listing_links(price_bins, url_links_path)

# remove duplicates from the list
listing_urls_set = set(listing_urls)

print(f"Removed {len(listing_urls) - len(listing_urls_set)} duplicate links." +
      f"Total number of links are {len(listing_urls_set)}.")
listing_urls = list(listing_urls_set)


# next step is to save each page!

# STEP 3: SAVE EACH PAGE
# ----------------------

def extract_data(property_url):
    bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")

    property_metadata = {'bedrooms': None, 'bathrooms': None, 'car_parks': None, 'url': property_url}

    try: 
        # looks for the header class to get property name
        property_metadata['name'] = bs_object \
            .find("h1", {"class": "css-164r41r"}) \
            .text

        # looks for the div containing a summary title for cost
        property_metadata['cost_text'] = bs_object \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text

        # get rooms and parking
        rooms = bs_object \
                .find("div", {"data-testid": "property-features"}) \
                .findAll("span", {"data-testid": "property-features-text-container"})


        # get the number of bedrooms and bathrooms
        for feature in rooms:
            # find the number and room type

            # check if a match with zero (has a dash)
            text = re.sub(r'−', '0', feature.text)
            match = re.findall(r'\d+\s[A-Za-z]+', text)
            
            if match:
                room_text = match[0]
                
                # check for bedrooms
                if 'Bed' in room_text:
                    property_metadata['bedrooms'] = int(re.search(r'\d+', room_text).group())
                
                # check for bathrooms
                if 'Bath' in room_text:
                    property_metadata['bathrooms'] = int(re.search(r'\d+', room_text).group())

            # check for parking
            if match and 'Parking' in feature.text:
                parking_text = match[0]
                property_metadata['car_parks'] = int(re.search(r'\d+', parking_text).group())

        # get the type of residency (apartment, house etc)
        property_metadata['type'] = bs_object \
            .find("div", {"data-testid": 'listing-summary-property-type'}) \
            .find('span') \
            .text

        # get the coordinate from the google maps API search
        # locate the 'a' tag that performs the searches and get the href
        coord_url = bs_object \
                .find("a", {'aria-label': 'Directions - Opens Google Maps for directions'})['href']
        # then match the coordinates from the search
        coordinates = re.findall(r'destination=(-?\d+\.\d+),(-?\d+\.\d+)', coord_url)[0]

        property_metadata['latitude'] = coordinates[0]
        property_metadata['longitude'] = coordinates[1]

        # get the description content - can add here later if needed
        # print(bs_object \
        #         .find('h2', string='Property Description') \
        #         # get the sibling (which has the description text)
        #         .find_next_sibling()
        #         # then get the content inside the expander
        #         .find("div", {"class": "noscript-expander-content css-1mnayj9"}) \
        #         .get_text(separator='\n', strip=True)
        # )

        # first argument was if it was successful
        return True, property_metadata
        
    except AttributeError:
        print(f"Issue with {property_url}")

        # the scrape was unsuccessful
        return False, None


# 1: start by creating the dataframe to be saved
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# init spark session
spark = SparkSession.builder.appName("DomainScrape").getOrCreate()

# define schema for each scraped entry
schema = StructType([
    StructField("bedrooms", IntegerType(), True),
    StructField("bathrooms", IntegerType(), True),
    StructField("car_parks", IntegerType(), True),
    StructField("url", StringType(), True),
    StructField("name", StringType(), True),
    StructField("cost_text", StringType(), True),
    StructField("type", StringType(), True),
    StructField("latitude", StringType(), True),
    StructField("longitude", StringType(), True)
])

BATCH_SIZE = 500

# download the data in batches so if something goes wrong can reset easily
for i in range(0, len(listing_urls), BATCH_SIZE):

    output_data = spark.createDataFrame([], schema=schema)
    unprocessed_links = []

    page_directory = PAGE_DIRECTORY + f'/{i}-{i+BATCH_SIZE}.parquet'

    if os.path.exists(page_directory):
        print(f"Skipping scraping range {i}-{i+BATCH_SIZE}")
        continue

    for j in range(i, min(len(listing_urls), i + BATCH_SIZE)):
        url = listing_urls[j]

        print(f'Searching url {j} of batch {i}-{i + BATCH_SIZE}: {url}')

        try:

            data = extract_data(url)

            # check if the scrape for that listing was successful
            if data[0]:
                row = Row(**data[1])  # convert dictionary to Row object
                row_df = spark.createDataFrame([row], schema=schema)  # create dataframe for this row
                output_data = output_data.union(row_df)
            else:
                unprocessed_links.append(url)

        except:
            # if the processing fails handle it
            print(f'Processing error for link: {url}')
            unprocessed_links.append(url)

    # save the scraped data to a parquet file
    print(f"Saving batch {i}-{i+BATCH_SIZE} to file. Successfully processed {output_data.count()} listings.")
    print(f"{len(unprocessed_links)} were not processed.")
    output_data.write.parquet(page_directory)

    # if there's any unprocessed links
    if len(unprocessed_links) > 0:
        append_to_file(METADATA_DIRECTORY + '/unprocessed.txt', unprocessed_links)
    

print(output_data.count())
print(unprocessed_links)

# print(property_metadata[test_url])

# pbar = tqdm(listing_urls[1:2])
# success_count, total_count = 0, 0
# for property_url in pbar:
#     bs_object = BeautifulSoup(urlopen(Request(property_url, headers={'User-Agent':"PostmanRuntime/7.6.0"})), "lxml")
#     total_count += 1
    
#     try: 
#         # looks for the header class to get property name
#         property_metadata[property_url]['name'] = bs_object \
#             .find("h1", {"class": "css-164r41r"}) \
#             .text

#         # looks for the div containing a summary title for cost
#         property_metadata[property_url]['cost_text'] = bs_object \
#             .find("div", {"data-testid": "listing-details__summary-title"}) \
#             .text

#         # get rooms and parking
#         rooms = bs_object \
#                 .find("div", {"data-testid": "property-features"}) \
#                 .findAll("span", {"data-testid": "property-features-text-container"})

#         # rooms
#         property_metadata[property_url]['rooms'] = [
#             re.findall(r'\d+\s[A-Za-z]+', feature.text)[0] for feature in rooms
#             if 'Bed' in feature.text or 'Bath' in feature.text
#         ]
#         # parking
#         property_metadata[property_url]['parking'] = [
#             re.findall(r'\S+\s[A-Za-z]+', feature.text)[0] for feature in rooms
#             if 'Parking' in feature.text
#         ]

#         property_metadata[property_url]['desc'] = re \
#             .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
#             .strip('</p>')
#         success_count += 1
        
#     except AttributeError:
#         print(f"Issue with {property_url}")

#     print(bs_object.prettify())

#     pbar.set_description(f"{(success_count/total_count * 100):.0f}% successful")







# then should check if file exists and remove it if it does


# then should save each page from the list of links


# then should get the data wanted and save it as a parquet file



# the max search is any

# print(get_number_in_price_range(300, 310))

