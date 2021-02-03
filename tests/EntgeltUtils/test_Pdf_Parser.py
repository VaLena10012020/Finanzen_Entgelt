import pytest
import pandas as pd

from EntgeltUtils.pdf_parser import PdfParser


@pytest.mark.parametrize("filename",
                         ["Test_1table.pdf", "Test_multitable.pdf"]
                         )
def test_single_and_multi_table(filename):
    parser = PdfParser()
    table_parsed_1 = parser.parse_entgelt(filename="./tests/data/" + filename)
    assert type(table_parsed_1) is pd.DataFrame
    assert str(table_parsed_1["date"][0]) == '2020-01-01 00:00:00'
    assert table_parsed_1['file'][0] == filename
