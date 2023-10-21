import re
import json
from Prototype import technicalsheet
from Prototype import websiteReader
from Prototype.Rhewa import CSVConverter, RhewaConverter


def main():
    #technicalsheet.run()
    #websiteReader.generate_data()
    #CSVConverter.runAdvancedConversion()
    rhewaconverter = RhewaConverter.RhewaConverter()
    rhewaconverter.fill_with_data(rhewaconverter)

if __name__ == '__main__':
    main()


