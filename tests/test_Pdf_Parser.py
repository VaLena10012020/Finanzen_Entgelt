from EntgeltUtils.pdf_parser import Parse_PDF


def single_table():
    parser = Parse_PDF()
    filename = "Test_1table.pdf"
    table_parsed_1 = parser.parse_Entgelt(filename="./data/"+filename)
    assert type(table_parsed_1) is list
    assert str(table_parsed_1[0]["date"]) == '2020-01-01 00:00:00'
    assert table_parsed_1[0]['file'] == filename


def multi_table():
    parser = Parse_PDF()
    filename = "Test_multitable.pdf"
    table_parsed_1 = parser.parse_Entgelt(filename="./data/"+filename)
    assert type(table_parsed_1) is list
    assert str(table_parsed_1[0]["date"]) == '2020-01-01 00:00:00'
    assert table_parsed_1[0]['file'] == filename
