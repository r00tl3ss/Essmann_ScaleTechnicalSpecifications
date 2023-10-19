from bs4 import BeautifulSoup
import requests


def fetch_url_as_text(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the text from the HTML
            text = soup.get_text()
            return text
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None