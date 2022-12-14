import argparse
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from io import FileIO
import argparse

# example channel_id to use
# UCFN4dYd4H_CsW64qZqgQY-A

# this is a sample code from yt document
# https://developers.google.com/youtube/reporting/v1/code_samples/python?hl=en#create_a_reporting_job

SCOPES = ['https://www.googleapis.com/auth/youtubepartner']

CLIENT_SECRETS_FILE = '/Users/chouwilliam/api-data-download/key/client_secret.json'
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'

# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

  # Remove keyword arguments that are not set.
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value

    return good_kwargs

# Call the YouTube Reporting API's reportTypes.list method to retrieve report types.
def list_report_types(youtube_reporting, **kwargs):
    # Provide keyword arguments that have values as request parameters.
    kwargs = remove_empty_kwargs(**kwargs)
    results = youtube_reporting.reportTypes().list(**kwargs).execute()
    reportTypes = results['reportTypes']

    if 'reportTypes' in results and results['reportTypes']:
        reportTypes = results['reportTypes']
        for reportType in reportTypes:
            print('Report type id: %s\n name: %s\n' % (reportType['id'], reportType['name'])) 
    else:
        print('No report types found')
        return False

    return True

# Call the YouTube Reporting API's jobs.create method to create a job.
def create_reporting_job(youtube_reporting, report_type_id, **kwargs):
    # Provide keyword arguments that have values as request parameters.
    kwargs = remove_empty_kwargs(**kwargs)

    reporting_job = youtube_reporting.jobs().create(
        body=dict(
        reportTypeId=args.report_type,
        name=args.name
        ),
        **kwargs
    ).execute()

    print ('Reporting job "%s" created for reporting type "%s" at "%s"'% (reporting_job['name'], reporting_job['reportTypeId'],reporting_job['createTime']))

# Prompt the user to enter a report type id for the job. Then return the id.
def get_report_type_id_from_user():
    report_type_id = input('Please enter the reportTypeId for the job: ')
    print ('You chose "%s" as the report type Id for the job.' % report_type_id)
    return report_type_id

# Prompt the user to set a job name
def prompt_user_to_set_job_name():
    job_name = input('Please set a name for the job: ')
    print ('Great! "%s" is a memorable name for this job.' % job_name)
    return job_name


if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  # The 'name' option specifies the name that will be used for the reporting job.
  parser.add_argument('--content_owner', default='', help='ID of content owner for which you are retrieving jobs and reports.')
  parser.add_argument('--include-system-managed', default=False, help='Whether the API response should include system-managed reports')
  parser.add_argument('--name', default='', help='Name for the reporting job. The script prompts you to set a name ' + 'for the job if you do not provide one using this argument.')
  parser.add_argument('--report_type', default=None, help='The type of report for which you are creating a job.')
  args = parser.parse_args()

  youtube_reporting = get_authenticated_service()

  try:
    # Prompt user to select report type if they didn't set one on command line.
    if not args.report_type:
        if list_report_types(youtube_reporting, onBehalfOfContentOwner=args.content_owner, includeSystemManaged=args.include_system_managed):
            args.report_type = get_report_type_id_from_user()
    # Prompt user to set job name if not set on command line.
    if not args.name:
        args.name = prompt_user_to_set_job_name()
    # Create the job.
    if args.report_type:
      create_reporting_job(youtube_reporting, args, onBehalfOfContentOwner=args.content_owner)

  except HttpError as e:
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))