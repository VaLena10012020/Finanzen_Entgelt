import pytest

from EntgeltUtils.pdf_parser import parse_entgelt


@pytest.mark.parametrize("filename",
                         ["Test_1table.pdf", "Test_multitable.pdf"]
                         )
def test_single_and_multi_table(filename):
    table_parsed_1 = parse_entgelt(filename="./tests/data/" + filename)
    assert type(table_parsed_1) is dict
    assert table_parsed_1["date"] == 1577836800000
    assert table_parsed_1['brutto'] == 0
