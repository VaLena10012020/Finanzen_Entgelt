import pytest
import os
import pandas as pd
from boto3 import client
from moto import mock_s3

from finanzen_base.Utils.extract_filename import extract_filename

from EntgeltUtils.app import App


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


def test_app_integration(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    # Upload Parsed Files
    files = ["Test_1table.pdf", "Test_multitable.pdf"]
    for file in files:
        s3_client.upload_file("tests/data/" + file, bucket_name, "data/"+file)

    app = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              name='Entgelt')
    app.check_for_unparsed_files()
    app.parse_files()
    # Get file in S3 storage
    files_source = extract_filename(app.con.list_objects(bucket_name=bucket_name,
                                                         prefix=bucket_source))
    files_target = extract_filename(app.con.list_objects(bucket_name=bucket_name,
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
    app.con.download_file(file_path=bucket_target+files[0][:-4]+".csv",
                          target_path="")
    df = pd.read_csv(files[0][:-4]+".csv")
    df_test = pd.read_csv("tests/data/Test_1table.csv")
    assert df.equals(df_test)
    os.remove(files[0][:-4]+".csv")
