import os
from boto3 import client
import pytest
from moto import mock_s3
import pandas as pd

from EntgeltUtils.app import App
from finanzen_base.Utils.extract_filename import extract_filename


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = client("s3", region_name="us-east-1")
        yield conn


@pytest.fixture
def bucket_name():
    return "my-test-bucket"


@pytest.fixture
def s3_test(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
    yield


def test_app_init(s3_client, s3_test, bucket_name):
    APP = App(bucket_name=bucket_name,
              bucket_source="data",
              bucket_target="database",
              APP_NAME='Entgelt',
              params=None)
    # Initialise PDF_Parser
    assert APP.con.list_objects(bucket_name) == []


def test_app_check_all_new(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    # Upload unparsed Files
    files = ["Test_1table.pdf", "Test_multitable.pdf"]
    for file in files:
        s3_client.upload_file("tests/data/" + file, bucket_name, bucket_source+file)

    APP = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              APP_NAME='Entgelt',
              params=None)

    APP.check_for_unparsed_files()
    assert "Test_1table" == APP.f_unparsed["data/Test_1table.pdf"]
    assert ["Test_1table", "Test_multitable"] == list(APP.f_unparsed.values())


def test_app_check_one_new(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    # Upload unparsed Files
    files = ["Test_1table.pdf", "Test_multitable.pdf"]
    for file in files:
        s3_client.upload_file("tests/data/" + file, bucket_name, bucket_source+file)
    # Upload one parsed file
    s3_client.upload_file("tests/data/Test_1table.csv", bucket_name, bucket_target+"Test_1table.csv")

    APP = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              APP_NAME='Entgelt',
              params=None)

    APP.check_for_unparsed_files()

    assert ["Test_multitable"] == list(APP.f_unparsed.values())


def test_app_integration(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    # Upload Parsed Files
    files = ["Test_1table.pdf", "Test_multitable.pdf"]
    for file in files:
        s3_client.upload_file("tests/data/" + file, bucket_name, "data/"+file)

    APP = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              APP_NAME='Entgelt',
              params=None)
    APP.check_for_unparsed_files()
    APP.parse_files()
    # Get file in S3 storage
    files_source = extract_filename(APP.con.list_objects(bucket_name=bucket_name,
                                                         prefix=bucket_source))
    files_target = extract_filename(APP.con.list_objects(bucket_name=bucket_name,
                                                         prefix=bucket_target))
    for file in files:
        # Check if original file are still in S3 storage
        assert file in list(files_source.values())
        # Check if new file is at the desired place in S3
        assert file[:-4]+".csv" in list(files_target.values())
        # Check if files are not longer stored locally
        assert file not in os.listdir()
        assert file[:-4]+".csv" not in os.listdir()

    # Check if files are parsed correctly
    APP.con.download_file(file_path=bucket_target+files[0][:-4]+".csv",
                          target_path="")
    df = pd.read_csv(files[0][:-4]+".csv")
    df_test = pd.read_csv("tests/data/Test_1table.csv")
    assert df.equals(df_test)
    os.remove(files[0][:-4]+".csv")
