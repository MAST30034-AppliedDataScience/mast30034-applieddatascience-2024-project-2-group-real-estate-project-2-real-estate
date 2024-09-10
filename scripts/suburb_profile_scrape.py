import requests
from bs4 import BeautifulSoup
from scrape_oldlistings import scrape_postcodes_from_file


def scrape_suburb_profiles():
    BASE_URL = "https://www.domain.com.au/suburb-profile/"
    suburbs_df = scrape_postcodes_from_file()
    for index, row in suburbs_df.iterrows():
        # Replace spaces with hyphens and lowercase suburb names
        suburb = row['suburb'].lower().replace(" ", "-")
        postcode = row['postcode']
        # Construct the URL assuming the state is "vic"
        link = f"{BASE_URL}{suburb}-vic-{postcode}"
        response = requests.get(link)
        
        if response.status_code == 200:
            # Parse the page content using BeautifulSoup
            bs_object = BeautifulSoup(response.content, 'html.parser')
            try: 
                

    



# Example usage:
#scrape_suburb_profiles()