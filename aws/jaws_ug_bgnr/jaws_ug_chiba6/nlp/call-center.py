import boto3
import datetime
import json
import requests
from requests_aws4auth import AWS4Auth
import time
import urllib3
import urllib
import urllib.request

# Variables to update
audio_file_name = 'xxxxxxxxxx.mp3' # For example, 000001.mp3
bucket_name = 'xxxxxxxxxx' # For example, my-transcribe-test
domain = 'https://xxxxxxxxxx.us-west-2.es.amazonaws.com' # For example, https://search-my-transcribe-test-12345.us-west-2.es.amazonaws.com
index = 'support-calls'
type = 'call'
es_region = 'us-west-2'

# Upload audio file to S3.
s3_client = boto3.client('s3')

audio_file = open(audio_file_name, 'rb')

print('Uploading ' + audio_file_name + '...')
response = s3_client.put_object(
    Body=audio_file,
    Bucket=bucket_name,
    Key=audio_file_name,
)

response = s3_client.get_bucket_location(
    Bucket=bucket_name
)

bucket_region = response['LocationConstraint']

# Build the URL to the audio file on S3.
mp3_uri = 'https://s3-' + bucket_region + '.amazonaws.com/' + bucket_name + '/' + audio_file_name

# Start transcription job.
transcribe_client = boto3.client('transcribe')
job_name = "%s_%s.mp3" % (
    audio_file_name.strip('.mp3'),
    int(datetime.datetime.now().timestamp())
)

print('Starting transcription job...')
response = transcribe_client.start_transcription_job(
    TranscriptionJobName=job_name,
    LanguageCode='ja-JP',
    MediaFormat='mp3',
    Media={
        'MediaFileUri': mp3_uri
    },
    Settings={
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 2 # assumes two people on a phone call
    }
)

# Wait for the transcription job to finish.
print('Waiting for job to complete...')
while True:
    response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    if response['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    else:
        print('Still waiting...')
    time.sleep(10)

transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']

# Open the JSON file, read it, and get the transcript.
response = urllib.request.urlopen(transcript_uri)
raw_json = response.read()
loaded_json = json.loads(raw_json)
transcript = loaded_json['results']['transcripts'][0]['transcript']

# Send transcript to Comprehend for key phrases and sentiment.
comprehend_client = boto3.client('comprehend')

# If necessary, trim the transcript.
# If the transcript is more than 5 KB, the Comprehend calls fail.
if len(transcript) > 5000:
    trimmed_transcript = transcript[:5000]
else:
    trimmed_transcript = transcript

print('Detecting key phrases...')
response = comprehend_client.detect_key_phrases(
    Text=trimmed_transcript,
    LanguageCode='ja'
)

keywords = []
for keyword in response['KeyPhrases']:
    keywords.append(keyword['Text'])

print('Detecting sentiment...')
response = comprehend_client.detect_sentiment(
    Text=trimmed_transcript,
    LanguageCode='ja'
)

sentiment = response['Sentiment']

# Build the Amazon Elasticsearch Service URL.
id = audio_file_name.strip('.mp3')
url = domain + '/' + index + '/' + type + '/' + id

# Create the JSON document.
json_document = {'transcript': transcript, 'keywords': keywords, 'sentiment': sentiment, 'timestamp': datetime.datetime.now().isoformat()}

# Provide all details necessary to sign the indexing request.
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, es_region, 'es', session_token=credentials.token)

# Add explicit header for Elasticsearch 6.x.
headers = {'Content-Type': 'application/json'}

# Index the document.
print('Indexing document...')
response = requests.put(url, auth=awsauth, json=json_document, headers=headers)

print(response)
print(response.json())