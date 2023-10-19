import time
import g4f
import os
import io
import re
import csv
import json
from Prototype import pdfreader, webscraper, DataSorter



def load_JSON_file(name, rights):
    with open(name, rights) as json_file:
        data = json.load(json_file)
        json_file.close()
        return data
    return None

def extract_json(input_string):
    # Find the start and end positions of the JSON part
    start = input_string.find('{')
    end = input_string.rfind('}') + 1

    if start != -1 and end != -1:
        # Extract the JSON part
        json_part = input_string[start:end]
        print('JSON part extracted successfully.')
        return json_part
    else:
        print('No JSON part found in the input string.')
        return None

def attributes_to_json(data):
    attributes = {}

    # Split the data into lines
    lines = data.split('\n')

    for line in lines:
        # Use regular expressions to extract key-value pairs
        match = re.match(r'^(\w+):\s*(.*)', line)
        if match:
            key, value = match.groups()
            attributes[key] = value

    # Convert the attributes dictionary to JSON
    json_data = json.dumps(attributes, indent=4)

    return json_data


def update_element_by_name(file_path, target_name, values_json_str):
    # Open the JSON file in read mode and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Check if the Ai has returned json data
    if values_json_str is None:
        return
    # Iterate through each element in the JSON data
    for element in data:
        # Check if the "Name" attribute exists and matches the target_name
        if "Name" in element and element["Name"] == target_name:
            try:
                # Parse the values_json_str as JSON
                values_dict = json.loads(values_json_str)

                # Iterate through the keys in values_dict
                for key, value in values_dict.items():
                    # Check if the key exists in both the element and values_dict
                    if key in element:
                        if value is not None and value != "":
                            # Update the value of that key in the element
                            element[key] = value
            except json.JSONDecodeError:
                print("Error: Invalid JSON object string")

    # Save the modified JSON data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def split_attributes_by_name(json_file_path, name_to_split, num_attributes=5, start_attribute=0):
    # Öffne die JSON-Datei und lade sie
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Suche nach dem Element mit dem angegebenen "Name"
    found_element = None
    for entry in data:
        if entry.get('Name', '') == name_to_split:
            found_element = entry
            break

    if found_element is not None:
        # Erstelle ein leeres Dictionary für den aufgeteilten Eintrag
        split_entry = {}

        # Begrenze die Anzahl der Schlüssel-Wert-Paare im aufgeteilten Eintrag auf die nächsten 'num_attributes'
        for i, (key, value) in enumerate(found_element.items()):
            if i < start_attribute:
                continue  # Überspringe Schlüssel-Wert-Paare, die vor dem Startattribut kommen
            if len(split_entry) >= num_attributes:
                break  # Stoppe, wenn die gewünschte Anzahl von Attributen erreicht ist
            split_entry[key] = value

        return split_entry, i + 1  # i + 1 gibt den Index des letzten extrahierten Attributs zurück

    else:
        print(f"Element with Name '{name_to_split}' not found.")
        return None, 0  # Wenn das Element nicht gefunden wurde, gebe None und 0 zurück

def add_empty_fields(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

        empty_fields = {
        "Hersteller": "",
        "Hersteller-Artikelnummer": "",
        "WaWi - EAN-Nummer": "",
        "Kategorie": "",
        "Name DE": "Auswertegeräte",
        "Name EN": "",
        "Zusatz DE": "",
        "Zusatz EN": "",
        "Beschreibung DE": "",
        "Beschreibung EN": "",
        "SHOP DE (HTML)": "",
        "SHOP EN (HTML)": "",
        "Meta-Titel DE (max. 56 Zeichen)": "",
        "Meta-Titel EN  (max. 56 Zeichen)": "",
        "Meta-Beschreibung DE (max. 155 Zeichen)": "",
        "Meta-Beschreibung EN (max. 155 Zeichen)": "",
        "Listenpreis 2023": "",
        "Shoprabatt": "",
        "VK mit Rabatt": "",
        "Wägebereich [Max] in g": "",
        "Wägebereich [Max] in kg": "",
        "Wägebereich [Max] in t": "",
        "Wägebereich [Max] in ct": "",
        "Ziffernschritt [d] in g": "",
        "Ziffernschritt [d] in kg": "",
        "Ziffernschritt [d] in mg": "",
        "Mengenwaage - Wägebereich [Max] in kg": "",
        "Mengenwaage - Ziffernschritt [d] in g": "",
        "Referenzwaage - Wägebereich [Max] in kg": "",
        "Referenzwaage - Ziffernschritt [d] in g": "",
        "Eichwert [e] in g": "",
        "Eichwert [e] in kg": "",
        "Eichklasse": "",
        "Mindestlast [Min] in g": "",
        "Mindestlast [Min] in kg": "",
        "Wiederholgenauigkeit (Standardabweichung) in g": "",
        "Wiederholgenauigkeit (Standardabweichung) in kg": "",
        "Wiederholgenauigkeit (Standardabweichung) in mg": "",
        "Linearität in ± g": "",
        "Linearität in ± kg": "",
        "Linearität in ± mg": "",
        "Max. Trocknungstemperatur in °C": "",
        "Heiztechnologie": "",
        "Kleinstes Teilegewicht (Normal) in g/Stück": "",
        "FPVO Nennfüllmenge der Fertigpackungen in g": "",
        "Dienstleistungen Eichung": "",
        "Dienstleistungen DAkkS": "",
        "Dienstleistungen ISO": "",
        "Auswertegerät": "",
        "Material Wägeplatte": "",
        "Material Struktur": "",
        "Material Gehäuse": "",
        "Material Auswertegerät": "",
        "Material Windschutz": "",
        "Gehäuse Breite in mm": "",
        "Gehäuse Tiefe in mm": "",
        "Gehäuse Höhe in mm": "",
        "Wägeplattform Breite in mm": "",
        "Wägeplattform Tiefe in mm": "",
        "Wägeplattform Höhe in mm": "",
        "Wägeplattform Durchmesser in mm": "",
        "Display-Art": "",
        "Wägeeinheiten": "",
        "Stabilisierungszeit in s": "",
        "Stromversorgung": "",
        "Akku-Betriebsdauer in h - Hinterleuchtung aus": "",
        "Batterie Betriebsdauer in h": "",
        "Luftfeuchte Umgebung (Max) in %": "",
        "Umgebungstemperatur (Max) in °C": "",
        "Umgebungstemperatur (Min) in °C": "",
        "OIML Klasse": "",
        "Empfohlenes Justiergewicht": "",
        "Nennwert": "",
        "Toleranz (OIML) in mg": "",
        "ATEX": "",
        "Eigenschaften": "",
        "Auswertegerät Kabellänge in m": "",
        "Bauart der Waage": "",
        "Funktionen": "",
        "Gewährleistung in Jahren": "",
        "IP-Schutz - Anzeige": "",
        "IP-Schutz - Plattform": "",
        "Justage": "",
        "Schnittstellen": "",
        "Schnittstellen Serie": "",
        "Schnittstellen optional": "",
        "Versand": "",
        "URL": ""
        }
        for item in data:
            item.update(empty_fields)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

def extract_json_and_save_to_file(input_string, output_file):
        # Find the start and end positions of the JSON part
    start = input_string.find('{')
    end = input_string.rfind('}') + 1

    if start != -1 and end != -1:
            # Extract the JSON part
        json_part = input_string[start:end]

            # Write the JSON part to the specified output file
        with open(output_file, 'w') as file:
            file.write(json_part)

        print(f'JSON part extracted and saved to {output_file}')
    else:
        print('No JSON part found in the input string.')

def runConversion():
    data = load_JSON_file("items_data.json", 'r')
    index = 0
    file_name = "items_data.json"
    for item in data:
        # Access individual properties of each dictionary
        index += 1
        name = item['Name']
        link = item['Link']
        table_content = item['Table Content']
        pdf_reference = item['PDF Reference']

        print(f'file name: {file_name}')
        prompt = ''
        if os.path.exists(file_name):
            print("file already exists")
        else:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4_32k,
                provider=g4f.Provider.Phind,
                messages=[{"role": "user", "content": prompt}])

            print(f'json data: {response}')
            extract_json_and_save_to_file(response, file_name)

def runAdvancedConversion():
    data = load_JSON_file("items_data.json", 'r')
    file_name = "items_data.json"
    for item in data:
        # Access individual properties of each dictionary
        index = 0
        index += 1
        name = item['Name']
        link = item['Link']
        table_content = item['Table Content']
        pdf_reference = item['PDF Reference']
        websiteContent = ""

        pdf_data_string = ''
        if os.path.exists(pdf_reference):
            pdf_data_string = pdfreader.read(pdf_reference)
        else:
            print("PDF file doesn't exist")
            pdf_data_string = ""
        websiteContent = webscraper.fetch_url_as_text(link)
        num_attributes = 5
        start_attribute = 0
        while True:
            split_attr, last_attribute_index = split_attributes_by_name(file_name, name, num_attributes, start_attribute)
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
                prompt = f"Du bist JSON-Experte und hast folgende Daten über eine Waage gegeben: {pdf_data_string}; {table_content}; {websiteContent}. Nun gib folgende Werte im JSON-Format für das Gerät wieder: {attribute_string}. Das Format sind 5 Schlüssel-Werte-Paare. Hast du einen Wert nicht erfasst so gib einen leeren String wieder."
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    provider=g4f.Provider.Phind,
                    messages=[{"role": "user", "content": prompt}])

                print(f'response: {response}')
                json_response = extract_json(response)

                print(f'extracted json content: {json_response}')
                update_element_by_name("items_data Kopie.json", name, json_response)

                time.sleep(1)

                start_attribute = last_attribute_index
                print(f'start attribute: {start_attribute}')
                if "URL:" in attribute_string:
                    break
        else:
             result = "Empty"
        print("Schleife beendet")

