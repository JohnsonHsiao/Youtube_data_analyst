import os
import sys
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/OrbitNext/api-data-download")

import pandas as pd
from tabulate import tabulate
import itertools
import argparse
import configparser

user_pthe_config = configparser.ConfigParser()
user_pthe_config.read(f"{user_home_path}/OrbitNext/api-data-download/user_info/user_path.ini")
PROJECT_PATH = user_pthe_config['project_path']['API_DATA_DOWNLOAD']

config = configparser.ConfigParser()
config.read(f"{user_home_path}/OrbitNext/api-data-download/key/confidential.ini")
API_KEY = config['PUBLIC_API_KEY']['API_KEY_3']

from research_code.channel_hunter import ChannelHunter
from main.channel_pool import *

yt = ChannelHunter(API_KEY, channel_id='UCBJycsmduvYEL83R_U4JriQ') #MKBHD
yt.download_channel_and_video_stats()


# for channel_tuple in common_channel:
#         channel_id = channel_tuple[0]
#         channel_name = channel_tuple[1]

# yt = YoutubeStats(API_KEY, channel_id)
# yt.extract_all()
# yt.data_dump() 
