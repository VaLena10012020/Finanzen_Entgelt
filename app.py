import time
import os
import sys

from EntgeltUtils.pdf_parser import PdfParser
from finanzen_base.Utils.MongoClasses import MongoConnect
from finanzen_base.Utils.MongoLogger import MongoLogger
from finanzen_base.Utils.OneDriveConnector import OneDriveConnector
from finanzen_base.Utils.credentials import credential

if __name__ == '__main__':
    # Set individuals for the app: filepath and APP_NAME
    filepath = os.getcwd()
    APP_NAME = 'Entgelt'
    params = sys.argv
    
    # Initialise Logging and log the start of the app
    if 'test' in params:
        MongoLogging = MongoLogger(collection=APP_NAME, logging_active=False)
    else:
        MongoLogging = MongoLogger(collection=APP_NAME, logging_active=True)
    MongoLogging.write_start_log()

    # Initialise PDF_Parser
    Parser = PdfParser(MongoLogging)
    
    # Initialise connection to database
    MongoConnection = MongoConnect(collect=APP_NAME)
    MongoLogging.write_log('Connected to Mongo Database')

    # Get Credentials
    credentials = credential(filepath=filepath, credential_type='onedrive')
    sec1, sec2 = credentials.get_credentials()
    MongoLogging.write_log({'Credentials found': credentials.credential_available})

    # Connect to mail server
    con = OneDriveConnector(sec1, sec2)
    con.test_connection()
    MongoLogging.write_log({'Connection to Mail server': con.connected})
    
    while con.connected:
            files_in_db = MongoConnection.get_distinct_item("file")
            files_in_cloud = con.show_files_in_folder("Entgelt/AudiAG")
            list_pdfs = []
            for file in list(files_in_cloud.keys()):
                if file not in files_in_db:
                    list_pdfs.append(file)
            
            if len(list_pdfs) > 0:
                MongoLogging.write_log({'New pdfs found': list_pdfs})
                for pdf in list_pdfs:
                    con.download_file(id_of_file=files_in_cloud[pdf], name_of_file=pdf)
                    pdf_parsed_list = Parser.parse_Entgelt(pdf)
                    MongoConnection.insert_dicts(pdf_parsed_list)
                    os.remove(pdf)
                    MongoLogging.write_log({'pdfs stored to database': pdf})
            else: 
                MongoLogging.write_log('no new pdfs found')
            time.sleep(30*60)
    
    MongoLogging.shut_down_log("mail server crashed")
