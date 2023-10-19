import g4f
import os
from Prototype import technicalsheet

class JSONConverter:
    PATH = '/Users/timon/Desktop/Essmann/Prototype/Prompts/'
    def __init__(self):
        pass

    @staticmethod
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


    @classmethod
    def run_convertion(cls):
        if os.path.exists(cls.PATH) and os.path.isdir(cls.PATH):
            for filename in os.listdir(cls.PATH):
                file_path = os.path.join(cls.PATH, filename)

                if os.path.isfile(file_path):

                    with open(file_path, 'r', encoding='utf-16-le') as file:
                        prompt = file.read()
                        response = g4f.ChatCompletion.create(
                            model=g4f.models.claude_v2 ,
                            provider=g4f.Provider.You,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        print(f"Result: {response}")
                        jsonfilename = technicalsheet.cut_last_path_part_and_extension(file_path) + ".json"
                        output_path = '/Prototype/SpecificationsData/' + jsonfilename
                        jsoncontent = cls.extract_json_and_save_to_file(response, output_path)

