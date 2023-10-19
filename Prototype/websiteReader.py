#written and optimized for rhewa.com
from bs4 import BeautifulSoup
import requests
import time
from Prototype import pdfdownloader
import json

def extract_list_items(ul_element):
    list_items = []
    for li in ul_element.find_all('li'):
        anchor = li.find('a')
        if anchor:
            item_text = anchor.find('span').get_text(strip=True)
            item_link = anchor['href']
            final_link = "https://www.rhewa.com" + item_link
            print(f'current link: {final_link}')
            table = extract_table(final_link)
            time.sleep(1)
            pdf_path = "Prototype/Rhewa/pdfs/" + item_text.replace("/", " ") + ".pdf"
            pdf_filename = item_text.replace("/", " ")
            print(f'file name: {pdf_filename}')
            if pdfdownloader.pdf_file_exists("Prototype/Rhewa/pdfs/", pdf_filename + ".pdf"):
                print("file already exists")
            else:
                pdf_doc = pdfdownloader.download_pdf_from_website(final_link, "Prototype/Rhewa/pdfs", filename=pdf_filename)
            time.sleep(1)


            # Extract the table
            list_items.append({'name': item_text, 'link': final_link, 'table': table, 'pdf_path': pdf_path})

        # Check for nested lists and recursively extract items
        sub_ul = li.find('ul')
        if sub_ul:
            list_items += extract_list_items(sub_ul)

    return list_items

def extract_table(url):
    page = requests.get(url)
    if page.status_code == 200:
        content = page.content
        DOMdocument = BeautifulSoup(content, 'html.parser')
        table = DOMdocument.find('table', {'class': 'prodtable'})
        if table:
            # Extract the table content
            table_rows = table.find_all('tr')
            table_content = []
            for row in table_rows:
                row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
                table_content.append(row_data)
            return table_content
    return None

def read():
    page = requests.get("https://www.rhewa.com/service/sitemap")
    if page.status_code == 200:
        content = page.content
        #print(f'content: {content}')
        DOMdocument = BeautifulSoup(content, 'html.parser')
        Data = {}
        # Find the top-level list containing the items by searching for the anchor tag with the title attribute.
        top_level_anchor = DOMdocument.find('a', {'title': 'Produkte'})
        if top_level_anchor:
            top_level_list = top_level_anchor.find_parent('li')
            items_data = extract_list_items(top_level_list)
            print(f'items data: {items_data}')
            return items_data
    return None


def write_items_data_to_json(items_data, output_file_path):
    data_to_write = []

    if items_data:
        for item in items_data:
            data_item = {
                "Name": item['name'],
                "Link": item['link'],
                "Table Content": item['table'],
                "PDF Reference": item['pdf_path'] # Add the PDF Reference attribute
            }
            data_to_write.append(data_item)

    with open(output_file_path, 'w') as json_file:
        json.dump(data_to_write, json_file, indent=4)

def generate_data():
    items_data = read()
    print(f'items data: {items_data}')
    output_path = "Prototype/Rhewa/items_data.json"
    write_items_data_to_json(items_data, output_path)

