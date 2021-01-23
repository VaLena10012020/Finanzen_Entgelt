import time
import os
import sys

from finanzen_base.Utils.s3connector import S3Connector
from EntgeltUtils.pdf_parser import PdfParser

if __name__ == '__main__':
    # Set individuals for the app: filepath and APP_NAME
    filepath = os.getcwd()
    APP_NAME = 'Entgelt'
    params = sys.argv

    # Initialise PDF_Parser
    Parser = PdfParser()

    # Initialise connection to database
    MongoConnection = MongoConnect(collect=APP_NAME)

    # Connect to s3 bucket
    con = S3Connector(bucket_name="valena1databucket")

    while con.connected:
        files_in_db = MongoConnection.get_distinct_item("file")
        files_in_cloud = con.show_files_in_folder("Entgelt/AudiAG")
        list_pdfs = []
        for file in list(files_in_cloud.keys()):
            if file not in files_in_db:
                list_pdfs.append(file)

        if len(list_pdfs) > 0:
            for pdf in list_pdfs:
                con.download_file(id_of_file=files_in_cloud[pdf],
                                  name_of_file=pdf)
                pdf_parsed_list = Parser.parse_entgelt(pdf)
                MongoConnection.insert_dicts(pdf_parsed_list)
                os.remove(pdf)
        else:
            print("No new pdfs found")
        time.sleep(30*60)

