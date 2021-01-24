import time
import os
import sys

from finanzen_base.Utils.s3connector import S3Connector
from EntgeltUtils.pdf_parser import PdfParser

if __name__ == '__main__':
    # Set individuals for the app: filepath and APP_NAME
    filepath = os.getcwd()
    bucket_name = "valena1databucket"
    APP_NAME = 'Entgelt'
    params = sys.argv

    # Initialise PDF_Parser
    Parser = PdfParser()

    # Initialise connection to database
    # MongoConnection = MongoConnect(collect=APP_NAME)

    # Connect to s3 bucket
    con = S3Connector(bucket_name=bucket_name)

    while con.connected:
        # files_in_db = MongoConnection.get_distinct_item("file")
        files_in_cloud = con.list_objects(bucket_name=bucket_name,
                                          prefix="Entgelt/Audi")
        list_pdfs = []
        # for file in list(files_in_cloud.keys()):
        #    if file not in files_in_db and ".pdf" in file:
        #        list_pdfs.append(file)

        if len(list_pdfs) > 0:
            for pdf in list_pdfs:
                filename = pdf.split("/")[-1]
                con.download_file(filepath=pdf, target_path=filename)
                pdf_parsed_list = Parser.parse_entgelt(filename)
                # MongoConnection.insert_dicts(pdf_parsed_list)
                os.remove(filename)
        else:
            print("No new pdfs found")
        time.sleep(30*60)
