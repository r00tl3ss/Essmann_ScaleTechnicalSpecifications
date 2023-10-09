import pdfplumber

def read(filename):
    with pdfplumber.open(filename) as pdf:
        text = ''

        for page in pdf.pages:
            text += page.extract_text()

    return text