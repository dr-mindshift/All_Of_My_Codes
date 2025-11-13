import datetime
from google.cloud import storage

def generate_signed_url():
    """Generates a v4 signed URL for uploading a blob using a service account."""
    # The path to your service account key file
    service_account_key_file = "FILE LOCATION HERE"

    # The name of your bucket
    bucket_name = "PROJECT NAME/BUCKET NAME"

    # The name of your object
    object_name = "record9.wav"

    # The HTTP method to allow
    http_method = "PUT"

    # The expiration time for the URL
    expiration_time = datetime.timedelta(hours=1)

    # Create a client using the service account key
    storage_client = storage.Client.from_service_account_json(service_account_key_file)

    # Get the bucket and blob
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    # Generate the signed URL
    signed_url = blob.generate_signed_url(
        version="v4",
        expiration=expiration_time,
        method=http_method,
        content_type="audio/wav",
    )

    print(signed_url)

if __name__ == "__main__":
    generate_signed_url()
