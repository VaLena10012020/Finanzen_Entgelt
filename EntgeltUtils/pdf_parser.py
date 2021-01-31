from tabula import read_pdf
import pandas as pd
from datetime import datetime


class PdfParser:
    def __init__(self, mongologger=None):
        if mongologger is not None:
            self.MongoLogging = mongologger
            self.MongoLogging.write_log('Initialised PDF Parser')
        else:
            self.MongoLogging = None

    def parse_entgelt(self, filename):
        # Read in pdf
        df = read_pdf(filename, multiple_tables=True, output_format="json",
                      pages='all')

        # create output dataframe
        df_out = pd.DataFrame(columns=range(0, 8), index=range(1, len(df)*40))

        # extract values from raw data and insert into output dataframe
        for k in range(0, (len(df))):
            data_pdf = df[k]['data']
            for i, data_pdfx in enumerate(data_pdf):
                for j, data in enumerate(data_pdfx):
                    df_out.at[(k*40)+i, j] = str(data['text'])

        # rename columns
        df_out.columns = ["type", "1", "2", "3", "4", "value2", "value", "7"]

        # Get date of Entgelt via row "Überweisung zum EndOfMonth"
        date_raw = df_out["type"][df_out["type"].str.contains(
            "Überweisung zum", regex=True, na=False)].to_list()[0]
        df_out["date"] = datetime.strptime(date_raw[16:], "%d.%m.%Y")

        # Set Name of File
        df_out["file"] = filename.split("/")[-1]

        # Return Output data as dataframe for further use in mongoDB
        return df_out
