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

    def parse_entgelt(self, filename: str) -> pd.DataFrame:
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

        # read schema definitions
        schema_defintion = pd.read_csv("./config/entgelt_definition.csv")
        df_dict = {}

        # Get date of Entgelt via row "Überweisung zum EndOfMonth"
        for i, schema in schema_defintion.itterrow():
            parsed = self.parse_df_field(df=df_out,
                                         search_column=schema["search_column"],
                                         target_column=schema["target_column"],
                                         search_str=schema["search_str"],
                                         split=schema["split"],
                                         output_float=schema["output_float"])
            if schema['parser_type'] == 'date':
                parsed = datetime.strptime(parsed, "%d.%m.%Y")
            df_dict[schema['parser_type']] = parsed

        # Return Output data as dataframe for further use in mongoDB
        return df_dict

    def parse_df_field(self, df: pd.DataFrame,
                       search_column: str, search_str: str, target_column: str = None,
                       split: str = None, output_float: bool = False):
        if target_column is None:
            target_column = search_column
        parsed_field = df[target_column][df[search_column].str.contains(search_str, regex=True, na=False)].to_list()[0]
        if split is not None:
            parsed_field = parsed_field.split(split)[-1]
        if output_float:
            parsed_field = self.parse_float(parsed_field)
        return parsed_field

    def parse_float(self, number_str: str):
        del_chars = ["-", " "]
        for del_char in del_chars:
            if del_char in number_str:
                number_str = number_str.replace(del_char, "")

        # Change german numbers to international ones
        if "," in number_str:
            number_str = number_str.replace(".", "")
            number_str = number_str.replace(",", ".")
        return float(number_str)
