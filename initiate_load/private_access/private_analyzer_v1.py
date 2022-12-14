import os
from datetime import datetime
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tabulate import tabulate

from pathlib import Path
user_home_path = str(Path.home())

import sys
sys.path.append(f'{user_home_path}/api-data-download')

import configparser
project_path_config = configparser.ConfigParser()
project_path_config.read(f'{user_home_path}/api-data-download/user_info/user_path.ini')
PROJECT_PATH = project_path_config['PROJECT_PATH']['API_DATA_DOWNLOAD']

from main.scopes import *
from main.private_metric import PRIVATE_METRICS

CLIENT_SECRETS_FILE = f'{user_home_path}/api-data-download/key/client_secret.json'
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
SCOPES = YT_SCOPES_B

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(
      **kwargs
    ).execute()
    return response

def create_table(table, headers=None):
    if headers:
        headerstring = "\t{}\t" * len(headers)
        print(headerstring.format(*headers))
    rowstring = "\t{}\t" * len(table[0])

    for row in table:
        print(rowstring.format(*row))

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument('--channel_id', help="CHANNEL_ID or MINE", required=True)
  args = parser.parse_args()

  channel_id = args.channel_id

  youtubeAnalytics = get_service()
  result = execute_api_request(
      youtubeAnalytics.reports().query,
      ids=f'channel=={channel_id}',
      startDate='2020-01-01',
      endDate='2022-08-30',
      metrics='averageViewDuration',
      dimensions='video',
      sort = 'day'
  )

print(tabulate(result['rows'], tablefmt="pretty"))


  # data arrangement
  #headers = ['video', 'estMinutesWatched', 'views', 'likes', 'subscribersGained','averageViewDuration']
  # create_table(result['rows'], headers=headers)
  #print(tabulate(result['rows'], headers=headers, tablefmt="pretty"))
   
