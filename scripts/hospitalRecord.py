import requests

# URL of the CSV file
url = "https://data.gov.au/data/dataset/88a95824-c0e7-4ec0-bb78-b36223dd16a8/resource/43b9e4a4-0752-44c7-b825-bc32c46cf3b7/download/public_hospital_list.csv?fbclid=IwZXh0bgNhZW0CMTEAAR37cV8l3WJ7LKm0TnP4YCr8WjquaHYGnfUQCjTMyBWfvkcvZRXsmmYmUjo_aem_BZazk8jxkn7QVKa9hDMupg"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in write mode and save the content
    with open('./data/raw/public_hospital_list.csv', 'wb') as file:
        file.write(response.content)
    print("CSV file has been downloaded and saved as 'public_hospital_list.csv'")
else:
    print(f"Failed to retrieve the file. Status code: {response.status_code}")
