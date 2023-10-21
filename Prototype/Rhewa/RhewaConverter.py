import openai
import tiktoken
import json
import re
import csv
import io
import os
import time
from Prototype.Rhewa import CSVConverter as csvcon
from Prototype import webscraper, pdfreader, DataSorter

openai.api_key = ""

class RhewaConverter:
    file_name = "test_data_rhewaconverter.json"
    data = csvcon.load_JSON_file(file_name, 'r')

    @staticmethod
    def fill_with_data(cls):
        for item in cls.data:
            name = item['Name']
            link = item['Link']
            table_content = item['Table Content']
            pdf_reference = item['PDF Reference']
            websiteContent = ""
            pdfDataString = ""

            if os.path.exists(pdf_reference):
                pdf_data_string = pdfreader.read(pdf_reference)
            else:
                print("PDF file doesn't exist")
                pdf_data_string = ""

            websiteContent = webscraper.fetch_url_as_text(link)

            num_attributes = 5
            start_attribute = 0

            while True:
                split_attr, last_attribute_index = csvcon.split_attributes_by_name(cls.file_name, name, num_attributes,
                                                                            start_attribute)
                if split_attr:
                    attribute_strings = [f"{key}: {value}" for key, value in split_attr.items()]
                    attribute_string = "\n".join(attribute_strings)
                    print(f'attribute_string: {attribute_string}')
                    sample_format = """{
                    wert1: wert,
                    wert2: wert,
                    wert3: wert,
                    wert4: wert,
                    wert5: wert
                    }"""
                    response = ""
                    try:
                        completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                            {"role": "system", "content": f"Du bist JSON-Experte und gibts als Antwort nur JSON Daten in folgendem Format wieder: {sample_format} das sind die Werte die du ausfüllen musst: {attribute_string}"},
                            {"role": "user", "content": f"Folgende Daten hast du über eine Waage gegeben: {pdfDataString}, {table_content}, {websiteContent}"}
                            ]
                        )
                        response = completion.choices[0].message.content
                    except openai.error.Timeout as e:
                        print("Timeout")
                    finally:
                        print(f'response: {response}')

                    time.sleep(1)

                    json_response = csvcon.extract_json(response)

                    print(f'extracted json content: {json_response}')
                    csvcon.update_element_by_name(cls.file_name, name, json_response)

                    start_attribute = last_attribute_index
                    print(f'start attribute: {start_attribute}')

                    if "URL:" in attribute_string:
                        break
            else:
                print("Schleife nicht durchlaufen")
            print("Schleife beendet")