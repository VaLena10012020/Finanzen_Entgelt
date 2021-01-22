import os
import sys
import pandas as pd

from finanzen_base.Utils.MongoLogger import MongoLogger
from finanzen_base.Utils.OneDriveConnector import OneDriveConnector
from finanzen_base.Utils.credentials import credential


if __name__ == '__main__':
    # Set individuals for the app: filepath and APP_NAME
    filepath = os.getcwd()
    APP_NAME = 'Entgelt_meta'
    params = sys.argv

    # Initialise Logging and log the start of the app
    #if 'test' in params:
    #    MongoLogging = MongoLogger(collection=APP_NAME, logging_active=False)
    #else:
    #    MongoLogging = MongoLogger(collection=APP_NAME, logging_active=True)
    #MongoLogging.write_start_log()

    # Get meta_data from OneDrive

    # Get Credentials
    credentials = credential(filepath=filepath, credential_type='onedrive')
    sec1, sec2 = credentials.get_credentials()
    #MongoLogging.write_log({'Credentials found': credentials.credential_available})

    # Get Data
    print(sec1)
    print(sec2)
    con = OneDriveConnector(sec1, sec2)
    files_in_cloud = con.show_files_in_folder("Entgelt/AudiAG_meta")
    meta_csv = 'types_entgelt.csv'
    con.download_file(id_of_file=files_in_cloud[meta_csv], name_of_file=meta_csv)
    meta = pd.read_csv(meta_csv)
    os.remove(meta_csv)
    print(meta)
