from EntgeltUtils.app import App


def lambda_handler(event, context):
    event["Resource"]
    app = App(bucket_name="valena1databucket",
              bucket_source="files/Entgelt/Audi",
              bucket_target="database/raw/Entgelt/Audi/",
              name='Entgelt')
    app.check_for_unparsed_files()
    app.parse_files()
    app.upload_parsed_files()
