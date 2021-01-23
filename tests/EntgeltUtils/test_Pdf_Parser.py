import pytest
import os
from EntgeltUtils.pdf_parser import PdfParser


@pytest.mark.parametrize("filename",
                         ["Test_1table.pdf", "Test_multitable.pdf"]
                         )
def test_single_and_multi_table(filename):
    parser = PdfParser()
    print(os.getcwd())
    table_parsed_1 = parser.parse_Entgelt(filename="./tests/data/"+filename)
    assert type(table_parsed_1) is list
    assert str(table_parsed_1[0]["date"]) == '2020-01-01 00:00:00'
    assert table_parsed_1[0]['file'] == filename
