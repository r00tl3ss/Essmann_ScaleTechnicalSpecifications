import re
import json
import os
from tests import JSONConverter
from tests import pdfreader


def cut_last_path_part(path):
    # Split the path into directory and filename
    directory, filename = os.path.split(path)

    # Return the filename (last part of the path)
    return filename


def eliminate_invalid_utf8_characters(input_string):
    # Initialize an empty result string
    result = ""

    # Iterate through each character in the input string
    for char in input_string:
        try:
            # Try to decode the character as UTF-8
            char.encode('utf-8').decode('utf-8')
            # If successful, it's a valid UTF-8 character, so add it to the result
            result += char
        except UnicodeDecodeError:
            # If decoding raises an error, it's not a valid UTF-8 character, so skip it
            pass

    return result

def cut_last_path_part_and_extension(path):
    # Split the path into directory and filename
    directory, filename = os.path.split(path)

    # Split the filename into name and extension
    name, extension = os.path.splitext(filename)

    # Return the name (last part of the path) without extension
    return name

def create_and_write_to_file(subdirectory, filename, content):
    # Create the subdirectory if it doesn't exist
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)

    # Create the full path to the file
    file_path = os.path.join(subdirectory, filename)

    # Open the file in write mode ('w') and add content
    with open(file_path, 'w', encoding='utf-16-le') as file:

        file.write(content)

def run():
    # define the path where the pdf documents are located
    source = '/Users/timon/Desktop/Essmann/tests/Sources/'
    subdirectory = 'tests/Prompts'
    documents_path = []

    for filename in os.listdir(source):
        if os.path.isfile(os.path.join(source, filename)):
            document_path = os.path.join(source, filename)
            if document_path not in documents_path:
                documents_path.append(document_path)
        for path in documents_path:
            text = pdfreader.read(path)
            prompt = f"""These are the technical specifications for a scale. Please create a detailed JSON file
                                    to sort, label and group them. Don't simplify it: {text}"""
            txtfilename = cut_last_path_part_and_extension(path) + ".txt"
            create_and_write_to_file(subdirectory, txtfilename, prompt)
            print(path)
    json_converter = JSONConverter.JSONConverter()
    json_converter.run_convertion()
