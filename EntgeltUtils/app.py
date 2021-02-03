import os

from finanzen_base.Utils.s3connector import S3Connector
from finanzen_base.Utils.extract_filename import extract_filename
from EntgeltUtils.pdf_parser import PdfParser


class App:
    def __init__(self, bucket_name: str = "valena1databucket",
                 bucket_source: str = "files/Entgelt/Audi",
                 bucket_target: str = "database/raw/Entgelt/Audi/",
                 name: str = 'Entgelt',
                 params: str = None):
        self.bucket_name = bucket_name
        self.bucket_source = bucket_source
        self.bucket_target = bucket_target
        self.APP_NAME = APP_NAME
        self.Parser = PdfParser()
        self.con = S3Connector(bucket_name=self.bucket_name)
        self.f_unparsed = {}

    def check_for_unparsed_files(self):
        f_raw = self.con.list_objects(bucket_name=self.bucket_name,
                                      prefix=self.bucket_source)
        f_raw = extract_filename(f_raw, file_ext=False)
        f_parsed = self.con.list_objects(bucket_name=self.bucket_name,
                                         prefix=self.bucket_target)
        f_parsed = extract_filename(f_parsed, file_ext=False)
        self.f_unparsed = {}
        for file in f_raw:
            if f_raw[file] not in f_parsed.values():
                self.f_unparsed[file] = f_raw[file]

    def parse_files(self):
        if len(self.f_unparsed) > 0:
            temp_file_name = "temp_file"
            for pdf in self.f_unparsed:
                self.con.download_file(file_path=pdf,
                                       target_path="")
                pdf_parsed_df = self.Parser.parse_entgelt(self.f_unparsed[pdf]+".pdf")
                pdf_parsed_df.to_csv(temp_file_name)

                file_upload_name = self.bucket_target+self.f_unparsed[pdf]+".csv"
                self.con.upload_file(file_path=temp_file_name,
                                     target_path=file_upload_name)
                os.remove(self.f_unparsed[pdf]+".pdf")
                os.remove(temp_file_name)
            return self.f_unparsed
        else:
            print("No new pdfs found")
