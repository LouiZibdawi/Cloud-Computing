from __future__ import print_function
import time
import boto3
import os
import json

s3 = boto3.resource('s3')

bucket = s3.Bucket("cis4010-irish")
for obj in bucket.objects.all():

  transcribe = boto3.client('transcribe')
  job_name = "TranscribeIrish-"+obj.key
  job_uri = "https://cis4010-irish.s3.amazonaws.com/"+obj.key
  # fileName = "awsIrishTranscriptions/" + os.path.splitext(obj.key)[0] + ".txt"

  try:
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)
    print('Creating transcribe job..')
  except Exception as e:
    # Do nothing
    print('Creating transcribe job..')
  finally:
    print("Transcribing " + obj.key)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        OutputBucketName="cis4010-irish-transcriptions",
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-IE'
    )
    attempt = 1
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Waiting ("+str(attempt)+"): Retrying in 10 seconds..." )
        attempt = attempt + 1
        time.sleep(10)

    print("Finished transcribing " + obj.key)