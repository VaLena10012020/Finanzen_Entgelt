import pytest
import os
from boto3 import client
from moto import mock_s3

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


def test_app_init(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    app = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              name='Entgelt')
    assert app.con.list_objects(bucket_name) == []


def test_app_check_all_new(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    # Upload unparsed Files
    files = ["Test_1table.pdf", "Test_multitable.pdf"]
    for file in files:
        s3_client.upload_file("tests/data/" + file, bucket_name, bucket_source+file)

    app = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              name='Entgelt')

    app.check_for_unparsed_files()
    assert "Test_1table" == app.f_unparsed["data/Test_1table.pdf"]
    assert ["Test_1table", "Test_multitable"] == list(app.f_unparsed.values())


def test_app_check_one_new(s3_client, s3_test, bucket_name):
    bucket_source = "data/"
    bucket_target = "database/"

    # Upload unparsed Files
    files = ["Test_1table.pdf", "Test_multitable.pdf"]
    for file in files:
        s3_client.upload_file("tests/data/" + file, bucket_name, bucket_source+file)
    # Upload one parsed file
    s3_client.upload_file("tests/data/Test_1table.csv", bucket_name, bucket_target+"Test_1table.csv")

    app = App(bucket_name=bucket_name,
              bucket_source=bucket_source,
              bucket_target=bucket_target,
              name='Entgelt')

    app.check_for_unparsed_files()

    assert ["Test_multitable"] == list(app.f_unparsed.values())
