from geopy.geocoders import GoogleV3
from shapely.geometry import Point
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
google_api_key = os.getenv('GOOGLE_API_KEY')


def get_coordinates(address):
    """
    This function takes a string address and returns its latitude and longitude as a tuple.
    If the address is not found, it returns None.
    """
    geolocator = GoogleV3(api_key=google_api_key)  # Replace with your API key
    location = geolocator.geocode(address, timeout=10)

    if location:
        return (location.latitude, location.longitude)
    else:
        return (None, None)
    
def find_location_id(lat, lon, gdf):
    """
    Find the SA2_CODE21 for a given latitude and longitude based on a GeoDataFrame of SA2 zones.
    
    Parameters:
    lat (float): Latitude of the location.
    lon (float): Longitude of the location.
    gdf (GeoDataFrame): GeoDataFrame containing SA2 zones and their geometries.
    
    Returns:
    int or None: SA2_CODE21 if the point is within an SA2 zone, otherwise None.
    """
    point = Point(lon, lat)
    for idx, zone in gdf.iterrows():
        if zone['geometry'] is not None and zone['geometry'].contains(point):
            return zone['SA2_CODE21']
    return None


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="your_app_name")  # Replace with your app name
def get_coordinates_osm(address):
    """
    This function takes a string address and returns its latitude and longitude as a tuple.
    If the address is not found, it returns (None, None).
    """
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except Exception as e:
        # Handle possible exceptions such as timeout or service unavailability
        print(f"Error geocoding {address}: {e}")
        return (None, None)