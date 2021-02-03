from EntgeltUtils.app import App

if __name__ == '__main__':
    # Set individuals for the app: filepath and APP_NAME
    APP = App(bucket_name="valena1databucket",
              bucket_source="files/Entgelt/Audi",
              bucket_target="database/raw/Entgelt/Audi/",
              name='Entgelt')
    APP.check_for_unparsed_files()
    APP.parse_files()
