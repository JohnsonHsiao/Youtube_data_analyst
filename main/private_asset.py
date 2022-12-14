import os
from datetime import datetime
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
