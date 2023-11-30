import requests
import time
import json


# Define a function named "result" that takes a jobid as an argument
def result(jobid):
    # Concatenate the jobid to the base URL
    url = "https://price-analytics.p.rapidapi.com/poll-job/" + jobid
    # Print the URL for debugging purposes
    print(url)
    # Define the headers for the API request
    headers = {
        "X-RapidAPI-Key": "47a719d0a8msh25950a7f3520aefp1483bejsn12e7330e9de2",
        "X-RapidAPI-Host": "price-analytics.p.rapidapi.com"
    }
    # Initialize the status as "working"
    status = "working"
    # Initialize a counter
    count = 0
    # Loop while the status is "working"
    while status == "working":
        # Send a GET request to the URL with the defined headers
        response = requests.get(url, headers=headers)
        # Parse the response as JSON
        j = response.json()
        # Update the status from the response
        status = j["status"]
        # If the status is not "working", extract the offers from the response
        if status != "working":
            r = j["results"][0]
            c = r["content"]
            o = c["offers"]
        # Print the status and count for debugging purposes
        print(status + str(count))
        # Increment the counter
        count = count + 1
        # Pause execution for 0.1 seconds to avoid overloading the API
        time.sleep(0.1)
    # Return the offers extracted from the response
    return o




