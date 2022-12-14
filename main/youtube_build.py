from pathlib import Path
user_home_path = str(Path.home())

import sys
sys.path.append(f"{user_home_path}/api-data-download")

import configparser
project_path_config = configparser.ConfigParser()
project_path_config.read(f"{user_home_path}/api-data-download/user_info/user_path.ini")
PROJECT_PATH = project_path_config['PROJECT_PATH']['API_DATA_DOWNLOAD']

key_config = configparser.ConfigParser()
key_config.read(f"{PROJECT_PATH}/key/confidential.ini")

API_KEY_1 = key_config['PUBLIC_API_KEY']['API_KEY_1']
API_KEY_2 = key_config['PUBLIC_API_KEY']['API_KEY_2']
API_KEY_3 = key_config['PUBLIC_API_KEY']['API_KEY_3']
API_KEY_4 = key_config['PUBLIC_API_KEY']['API_KEY_4']
API_KEY_5 = key_config['PUBLIC_API_KEY']['API_KEY_5']

from googleapiclient.discovery import build

YT_BUILDER = build('youtube', 'v3', developerKey=API_KEY_1)