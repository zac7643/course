# import the requests library
import requests

# define a function to search for an item on Amazon UK
def search(item):
    # define the URL of the API endpoint
    url = "https://price-analytics.p.rapidapi.com/search-by-term/"

    # define the payload of the request, which includes the source (Amazon), the country (UK), and the item to search for
    payload = {
        "source": "amazon",
        "country": "uk",
        "values": item
    }
    
    # define the headers of the request, which includes the content type and the API key
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "47a719d0a8msh25950a7f3520aefp1483bejsn12e7330e9de2",
        "X-RapidAPI-Host": "price-analytics.p.rapidapi.com"
    }

    # send a POST request to the API endpoint with the defined payload and headers
    response = requests.post(url, data=payload, headers=headers)

    # return the JSON response from the API
    return response.json()
