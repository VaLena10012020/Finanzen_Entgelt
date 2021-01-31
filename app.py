import time
import os
import sys

from finanzen_base.Utils.s3connector import S3Connector
from finanzen_base.Utils.extract_filename import extract_filename
from EntgeltUtils.pdf_parser import PdfParser

if __name__ == '__main__':
    # Set individuals for the app: filepath and APP_NAME
    filepath = os.getcwd()
    bucket_name = "valena1databucket"
    bucket_source = "files/Entgelt/Audi"
    bucket_target = "database/raw/Entgelt/Audi/"
    APP_NAME = 'Entgelt'
    params = sys.argv

    # Initialise PDF_Parser
    Parser = PdfParser()

    # Connect to s3 bucket
    con = S3Connector(bucket_name=bucket_name)

    while True:
        files_raw = extract_filename(con.list_objects(bucket_name=bucket_name,
                                                      prefix=bucket_source))
        files_parsed = extract_filename(con.list_objects(bucket_name,
                                                         bucket_target))
        list_pdfs = {}
        for file in files_raw:
            if files_raw[file] not in files_parsed.values() and ".pdf" in file:
                list_pdfs[file] = files_raw[file]

        if len(list_pdfs) > 0:
            temp_file_name = "temp_file"
            for pdf in list_pdfs:
                con.download_file(filepath=pdf, target_path=list_pdfs[pdf])
                pdf_parsed_df = Parser.parse_entgelt(list_pdfs[pdf])
                pdf_parsed_df.to_csv(temp_file_name)
                con.upload_file(file_path=temp_file_name,
                                target_path=bucket_target + list_pdfs[pdf])
                os.remove(list_pdfs[pdf])
                os.remove(temp_file_name)
        else:
            print("No new pdfs found")
        time.sleep(30 * 60)
