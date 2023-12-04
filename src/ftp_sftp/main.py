
from ftplib import FTP
import io
from datetime import date, datetime
from google.cloud import bigquery
from google.cloud import storage
from google.cloud import secretmanager


def main(request):
    """
        This function will pull the Amazon Data
        file daily from the ftp and upload it to
        cloud storage.

        It is triggered to run at 8:00 MDT
        0 14 * * *
    """

    # Initialize clients
    bigquery_client = bigquery.Client()
    storage_client = storage.Client()
    secrets = secretmanager.SecretManagerServiceClient()

    # Access Secrets
    ftp_username = secrets.access_secret_version(
        request={"name": "projects/xxx/secrets/FTP_USER/versions/latest"}).payload.data.decode("utf-8")
    ftp_password = secrets.access_secret_version(
        request={"name": "projects/xxx/secrets/FTP_PASS/versions/latest"}).payload.data.decode("utf-8")
    ftp_host = secrets.access_secret_version(
        request={"name": "projects/xxx/secrets/FTP_HOST/versions/latest"}).payload.data.decode("utf-8")

    # Establish FTP connection
    with FTP(ftp_host) as ftp:
        ftp.login(user=ftp_username, passwd=ftp_password)

        # List all files in the directory
        file_list = ftp.nlst()

        for file_name in file_list:
            # get specific file name from i.e. .csv
            if file_name.endswith('.csv') and "" in file_name:

                # Read the file from FTP server
                ftp_file = io.BytesIO()
                ftp.retrbinary('RETR ' + file_name, ftp_file.write)
                ftp_file.seek(0)

                gcs_bucket_name = 'cloud_0'
                gcs_folder_name = 'data'

                bucket = storage_client.bucket(gcs_bucket_name)
                blob = bucket.blob(f"{gcs_folder_name}/{file_name}")
                if blob.exists() is False:
                    # Upload to Cloud Storage if file does not exist
                    blob.upload_from_file(ftp_file, content_type='text/csv')

                    # Define the URI for the CSV file in Google Cloud Storage
                    gcs_uri = f"gs://{gcs_bucket_name}/{gcs_folder_name}/{file_name}"

                    # Create a BigQuery table reference
                    table_ref = ".."

                    # Create a BigQuery job configuration
                    job_config = bigquery.LoadJobConfig()
                    job_config.source_format = bigquery.SourceFormat.CSV
                    job_config.skip_leading_rows = 1
                    job_config.autodetect = True
                    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED
                    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

                    # Load the CSV data from Google Cloud Storage into BigQuery
                    job = bigquery_client.load_table_from_uri(
                        gcs_uri,
                        table_ref,
                        job_config=job_config
                    )
                    job.result()

                    destination_table = bigquery_client.get_table(table_ref)

                    print(
                        f"File '{file_name}' transferred into BigQuery table '{destination_table}'")
                else:
                    print(
                        f"File '{file_name}' already exists in Cloud Storage")
                    
    print('Success! Cloud Function is complete.')
    return ('OK')


if __name__ == '__main__':
    main('request')
