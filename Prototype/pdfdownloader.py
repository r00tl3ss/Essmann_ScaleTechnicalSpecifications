import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def contains_word(text, word):
    return word in text

def doesNotContainWord(text, word):
    return word not in text

def download_pdf_from_website(url, subdirectory, filename=None):
    # Create the subdirectory if it doesn't exist
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links in the HTML
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            if href and href.endswith('.pdf'):
                pdf_url = urljoin(url, href)
                if doesNotContainWord(pdf_url, 'Bedienungsanleitung'):
                    if filename is None:
                        user_filename = input(f"Enter a filename for '{pdf_url}': ")
                    else:
                        user_filename = filename.replace("/", " ")
                    pdf_filename = os.path.join(subdirectory, user_filename) + ".pdf"

                    # Download the PDF file
                    with open(pdf_filename, 'wb') as pdf_file:
                        pdf_response = requests.get(pdf_url)
                        if pdf_response.status_code == 200:
                            pdf_file.write(pdf_response.content)
                            print(f"Downloaded {pdf_filename}")
                        else:
                            print(f"Failed to download {pdf_url}")

    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")

def pdf_file_exists(subdirectory, filename):
    pdf_path = os.path.join(subdirectory, filename)
    return os.path.exists(pdf_path)