
import cloudstorage as gcs

#Get the default bucket from google cloud storage
default_bucket = 'fanapton.appspot.com'

def upload_file(file):
  uploaded_file_content = file.file.read()
  uploaded_file_filename = file.filename
  uploaded_file_type = file.type

  write_retry_params = gcs.RetryParams(backoff_factor=1.1)
  gcs_file = gcs.open(
    "/" + default_bucket + "/" + uploaded_file_filename,
    "w",
    content_type=uploaded_file_type,
    retry_params=write_retry_params
  )
  gcs_file.write(uploaded_file_content)
  gcs_file.close()

  return 'https://%(bucket)s.storage.googleapis.com/%(file)s' % {'bucket':default_bucket, 'file':uploaded_file_filename}

