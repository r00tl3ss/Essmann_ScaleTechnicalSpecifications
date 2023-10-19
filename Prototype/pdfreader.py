import pdfplumber

def read(filename):
    text = ''
    try:
        with pdfplumber.open(filename) as pdf:

            for page in pdf.pages:
                text += page.extract_text()
    except Exception as e:
        print(f'An error occured when trying to read/open the pdf file. Error log: {e}')
        text = ''
    return text

