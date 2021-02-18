from tabula import read_pdf
import pandas as pd
from omegaconf import OmegaConf
from finanzen_base.Utils.date_ms import date_to_ms


def parse_entgelt(filename: str) -> pd.DataFrame:
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
    schema_defintion = OmegaConf.load("conf/entgelt_valentin.yaml")
    df_dict = {}

    # Get date of Entgelt via row "Überweisung zum EndOfMonth"
    for schema in schema_defintion:
        parsed = parse_df_field(df=df_out,
                                search_column=schema_defintion[schema]["search_column"],
                                target_column=schema_defintion[schema]["target_column"],
                                search_str=schema_defintion[schema]["search_str"],
                                split=schema_defintion[schema]["split"],
                                output_float=schema_defintion[schema]["output_float"])
        if schema == 'date':
            parsed = date_to_ms(date_str=parsed.split(".")[2]+"-"+parsed.split(".")[1]+"-"+parsed.split(".")[0])
        df_dict[schema] = parsed

    # Return Output data as dataframe for further use in mongoDB
    return df_dict


def parse_df_field(df: pd.DataFrame,
                   search_column: str, search_str: str, target_column: str = None,
                   split: str = None, output_float: bool = False):
    if target_column is None:
        target_column = search_column
    try:
        parsed_field = df[target_column][df[search_column].str.contains(search_str, regex=True, na=False)].to_list()[0]
        if split is not None:
            parsed_field = parsed_field.split(split)[-1]
        if output_float:
            parsed_field = parse_float(parsed_field)
    except IndexError:
        if output_float:
            parsed_field = 0
        else:
            parsed_field = ""
    return parsed_field


def parse_float(number_str: str):
    del_chars = ["-", " "]
    for del_char in del_chars:
        if del_char in number_str:
            number_str = number_str.replace(del_char, "")

    # Change german numbers to international ones
    if "," in number_str:
        number_str = number_str.replace(".", "")
        number_str = number_str.replace(",", ".")
    return float(number_str)
