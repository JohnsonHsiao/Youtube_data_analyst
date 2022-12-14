import argparse
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from io import FileIO
import urllib.request
import urllib.error

def get_authenticated_service():

  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()

  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):

  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

# Call the YouTube Reporting API's jobs.list method to retrieve reporting jobs.
def list_reporting_jobs(youtube_reporting, **kwargs):
  # Only include the onBehalfOfContentOwner keyword argument if the user
  # set a value for the --content_owner argument.
  kwargs = remove_empty_kwargs(**kwargs)

  # Retrieve the reporting jobs for the user (or content owner).
  results = youtube_reporting.jobs().list(**kwargs).execute()

  if 'jobs' in results and results['jobs']:
    jobs = results['jobs']
    for job in jobs:
      print ('Reporting job id: %s\n name: %s\n for reporting type: %s\n'
        % (job['id'], job['name'], job['reportTypeId']))
  else:
    print('No jobs found')
    return False

  return True

# Call the YouTube Reporting API's reports.list method to retrieve reports created by a job
# Only include the onBehalfOfContentOwner keyword argument if the user
# set a value for the --content_owner argument

def report_retrieve(youtube_reporting, **kwargs):

  kwargs = remove_empty_kwargs(**kwargs)

  # Retrieve available reports for the selected job
  results = youtube_reporting.jobs().reports().list(**kwargs).execute()

  if 'reports' in results and results['reports']:
    reports = results['reports']
    for report in reports:
      print ('Report dates: %s to %s\n       download URL: %s\n'
        % (report['startTime'], report['endTime'], report['downloadUrl']))

# Call the YouTube Reporting API's media.download method to download the report
def download_report(youtube_reporting, report_url, local_file):
  request = youtube_reporting.media().download(
    resourceName=' '
  )
  request.uri = report_url
  fh = FileIO(local_file, mode='wb')
  # Stream/download the report in a single request
  downloader = MediaIoBaseDownload(fh, request, chunksize=-1)

  done = False
  while done is False:
    status, done = downloader.next_chunk()
    if status:
      print ('Download %d%%.' % int(status.progress() * 100))
  print ('Download Complete!')

# Prompt the user to select a job and return the specified ID
def get_job_id_from_user():

  job_id = input('Please enter the job id for the report retrieval: ')
  print ('You chose "%s" as the job Id for the report retrieval.' % job_id)
  return job_id

# Prompt the user to select a report URL and return the specified URL
def get_report_url_from_user():

  report_url = input('Please enter the report URL to download: ')
  print ('You chose "%s" to download.' % report_url)
  return report_url