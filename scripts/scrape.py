
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

suburbs_with_zip_codes = [
    "albert-park-vic-3206",
    "middle-park-vic-3206",
    "st-kilda-west-vic-3182",
    "armadale-vic-3143",
    "carlton-north-vic-3054",
    "carlton-vic-3053",
    "parkville-vic-3052",
    "melbourne-vic-3000",
    "st-kilda-road-vic-3004",
    "collingwood-vic-3066",
    "abbotsford-vic-3067",
    "docklands-vic-3008",
    "east-melbourne-vic-3002",
    "st-kilda-east-vic-3183",
    "elwood-vic-3184",
    "fitzroy-vic-3065",
    "fitzroy-north-vic-3068",
    "clifton-hill-vic-3068",
    "flemington-vic-3031",
    "kensington-vic-3031",
    "north-melbourne-vic-3051",
    "west-melbourne-vic-3003",
    "port-melbourne-vic-3207",
    "prahran-vic-3181",
    "windsor-vic-3181",
    "richmond-vic-3121",
    "burnley-vic-3121",
    "south-melbourne-vic-3205",
    "south-yarra-vic-3141",
    "southbank-vic-3006",
    "st-kilda-vic-3182",
    "toorak-vic-3142",
    "balwyn-vic-3103",
    "blackburn-vic-3130",
    "box-hill-vic-3128",
    "bulleen-vic-3105",
    "templestowe-vic-3106",
    "doncaster-vic-3108",
    "burwood-vic-3125",
    "ashburton-vic-3147",
    "camberwell-vic-3124",
    "glen-iris-vic-3146",
    "canterbury-vic-3126",
    "surrey-hills-vic-3127",
    "mont-albert-vic-3127",
    "chadstone-vic-3148",
    "oakleigh-vic-3166",
    "clayton-vic-3168",
    "doncaster-east-vic-3109",
    "donvale-vic-3111",
    "hawthorn-east-vic-3123",
    "glen-waverley-vic-3150",
    "mulgrave-vic-3170",
    "hawthorn-vic-3122",
    "kew-vic-3101",
    "mount-waverley-vic-3149",
    "nunawading-vic-3131",
    "mitcham-vic-3132",
    "vermont-vic-3133",
    "forest-hill-vic-3131",
    "aspendale-vic-3195",
    "chelsea-vic-3196",
    "carrum-vic-3197",
    "bentleigh-vic-3204",
    "brighton-vic-3186",
    "brighton-east-vic-3187",
    "carnegie-vic-3163",
    "caulfield-vic-3162",
    "cheltenham-vic-3192",
    "elsternwick-vic-3185",
    "hampton-vic-3188",
    "beaumaris-vic-3193",
    "malvern-vic-3144",
    "malvern-east-vic-3145",
    "mentone-vic-3194",
    "parkdale-vic-3195",
    "murrumbeena-vic-3163",
    "hughesdale-vic-3166",
    "altona-vic-3018",
    "footscray-vic-3011",
    "keilor-east-vic-3033",
    "avondale-heights-vic-3034",
    "melton-vic-3337",
    "newport-vic-3015",
    "spotswood-vic-3015",
    "st-albans-vic-3021",
    "deer-park-vic-3023",
    "sunshine-vic-3020",
    "sydenham-vic-3037",
    "werribee-vic-3030",
    "hoppers-crossing-vic-3029",
    "west-footscray-vic-3012",
    "williamstown-vic-3016",
    "yarraville-vic-3013",
    "seddon-vic-3011",
    "broadmeadows-vic-3047",
    "roxburgh-park-vic-3064",
    "brunswick-vic-3056",
    "coburg-vic-3058",
    "pascoe-vale-south-vic-3044",
    "craigieburn-vic-3064",
    "brunswick-east-vic-3057",
    "essendon-vic-3040",
    "gladstone-park-vic-3043",
    "tullamarine-vic-3043",
    "keilor-vic-3036",
    "moonee-ponds-vic-3039",
    "ascot-vale-vic-3032",
    "oak-park-vic-3046",
    "glenroy-vic-3046",
    "fawkner-vic-3060",
    "pascoe-vale-vic-3044",
    "coburg-north-vic-3058",
    "sunbury-vic-3429",
    "west-brunswick-vic-3055",
    "bundoora-vic-3083",
    "greensborough-vic-3088",
    "hurstbridge-vic-3099",
    "eltham-vic-3095",
    "research-vic-3095",
    "montmorency-vic-3094",
    "fairfield-vic-3078",
    "alphington-vic-3078",
    "heidelberg-vic-3084",
    "heidelberg-west-vic-3081",
    "ivanhoe-vic-3079",
    "ivanhoe-east-vic-3079",
    "mill-park-vic-3082",
    "epping-vic-3076",
    "northcote-vic-3070",
    "preston-vic-3072",
    "reservoir-vic-3073",
    "thomastown-vic-3074",
    "lalor-vic-3075",
    "thornbury-vic-3071",
    "whittlesea-vic-3757",
    "bayswater-vic-3153",
    "boronia-vic-3155",
    "croydon-vic-3136",
    "lilydale-vic-3140",
    "ferntree-gully-vic-3156",
    "ringwood-vic-3134",
    "rowville-vic-3178",
    "wantirna-vic-3152",
    "scoresby-vic-3179",
    "yarra-ranges-vic-3139",
    "berwick-vic-3806",
    "cranbourne-vic-3977",
    "dandenong-vic-3175",
    "dandenong-north-vic-3175",
    "endeavour-hills-vic-3802",
    "narre-warren-vic-3805",
    "hampton-park-vic-3976",
    "noble-park-vic-3174",
    "pakenham-vic-3810",
    "springvale-vic-3171",
    "dromana-vic-3936",
    "portsea-vic-3944",
    "frankston-vic-3199",
    "hastings-vic-3915",
    "flinders-vic-3929",
    "mount-eliza-vic-3930",
    "mornington-vic-3931",
    "mt-martha-vic-3934",
    "seaford-vic-3198",
    "carrum-downs-vic-3201",
    "belmont-vic-3216",
    "grovedale-vic-3216",
    "corio-vic-3214",
    "geelong-vic-3220",
    "newcombe-vic-3219",
    "herne-hill-vic-3218",
    "geelong-west-vic-3218",
    "lara-vic-3212",
    "newtown-vic-3220",
    "north-geelong-vic-3215",
    "ballarat-vic-3350",
    "mount-clear-vic-3350",
    "buninyong-vic-3357",
    "sebastopol-vic-3356",
    "delacombe-vic-3356",
    "wendouree-vic-3355",
    "alfredton-vic-3350",
    "bendigo-vic-3550",
    "flora-hill-vic-3550",
    "bendigo-east-vic-3550",
    "golden-square-vic-3555",
    "kangaroo-flat-vic-3555",
    "north-bendigo-vic-3550",
    "bairnsdale-vic-3875",
    "benalla-vic-3672",
    "castlemaine-vic-3450",
    "echuca-vic-3564",
    "hamilton-vic-3300",
    "horsham-vic-3400",
    "mildura-vic-3500",
    "moe-vic-3825",
    "newborough-vic-3825",
    "morwell-vic-3840",
    "ocean-grove-vic-3226",
    "barwon-heads-vic-3227",
    "portland-vic-3305",
    "sale-vic-3850",
    "maffra-vic-3860",
    "seymour-vic-3660",
    "shepparton-vic-3630",
    "swan-hill-vic-3585",
    "torquay-vic-3228",
    "traralgon-vic-3844",
    "wangaratta-vic-3677",
    "warragul-vic-3820",
    "warrnambool-vic-3280",
    "wodonga-vic-3690"
]

home_url = "https://www.domain.com.au/"


def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def scrape_property_details(url):
    print(f"Scraping details for: {url}")
    response = fetch_page(url)
    if not response:
        return None
    
    bsobj = BeautifulSoup(response.text, "lxml")
    pattern1 = re.compile(r'>(.+)<.')
    pattern2 = re.compile(r'destination=(.+)" rel=.')
    pattern = re.compile(r'(\d+)<!-- -->')

    try:
        property_name = bsobj.find("h1", {"class": "css-164r41r"}).text.strip() if bsobj.find("h1", {"class": "css-164r41r"}) else None


        property_price = bsobj.find("div", {"data-testid": "listing-details__summary-title"})
        property_price = pattern1.findall(str(property_price))[0] if property_price else None


        all_basic_features = bsobj.find("div", {"data-testid": "property-features-wrapper"})
        print(all_basic_features)
        all_basic_features = all_basic_features.findAll("span", {"data-testid": "property-features-text-container"})
        print(all_basic_features)
        property_features = []
        for feature in all_basic_features:
            number = feature.contents[0].strip()  
            print(number)
            property_features.append(number)

        type_div = bsobj.find("div", {"data-testid": "listing-summary-property-type"})
        property_type = type_div.find("span").text.strip() if type_div and type_div.find("span") else "N/A"
        # Extract latitudes and longitudes
        lat_long = bsobj.find("a", {"target": "_blank", 'rel': "noopener noreferrer"})
        latitude, longitude = None, None
        if lat_long:
            lat_long_match = pattern2.findall(str(lat_long))
            if lat_long_match:
                latitude, longitude = lat_long_match[0].split(',')
        property_header = bsobj.find("h3", {"data-testid": "listing-details__description-headline"})
        property_headline = property_header.get_text(strip=True) if property_header else "N/A"
        
        # Extract property description
        property_description = ""
        if property_header:
            for p in property_header.find_next_siblings('p'):
                property_description += p.get_text(strip=True) + " "
        
        return {
            "URL": url,
            "Rent_Price": property_price,
            "Address": property_name,
            "Bedrooms": property_features[0],
            "Bathrooms": property_features[1],
            "Parking": property_features[2],
            "Property_Type": property_type,
            "Latitude": latitude,
            "Longitude": longitude,
            "Property_Headline": property_headline,
            "Property_Description": property_description.strip()
        }
    except Exception as e:
        print(f"Error extracting details from {url}: {e}")
        return None

def scrape_page(suburb, page_number):
    print(f"Scraping page {page_number} for suburb {suburb}...")
    response = fetch_page(f"{home_url}/rent/{suburb}/?page={page_number}")
    if response:
        bsobj = BeautifulSoup(response.text, "lxml")
        result_list = bsobj.find("ul", {"data-testid": "results"})
        if result_list:
            all_links = result_list.findAll("a", href=re.compile(r"https://www.domain.com.au/*"))
            return list(set(link.attrs['href'] for link in all_links if 'href' in link.attrs))
    return []

def main():
    list_of_links = []
    properties_details = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for suburb in suburbs_with_zip_codes:
            for page in range(1, 3):  
                futures.append(executor.submit(scrape_page, suburb, page))

        for future in as_completed(futures):
            links = future.result()
            if links:
                list_of_links.extend(links)


    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_link = {executor.submit(scrape_property_details, link): link for link in set(list_of_links)}
        for future in as_completed(future_to_link):
            property_details = future.result()
            if property_details:
                properties_details.append(property_details)
    cwd = os.getcwd()
    csv_file = os.path.join(cwd, "data/landing/alt_properties.csv")
    csv_columns = ["URL", "Rent_Price", "Address", "Bedrooms", "Bathrooms", "Parking", "Property_Type", "Latitude", "Longitude", "Property_Headline","Property_Description"]
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
            for data in properties_details:
                writer.writerow(data)
        print(f"\nData has been saved to {csv_file}")
    except IOError as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    main()
