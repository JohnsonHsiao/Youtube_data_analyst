import sys
import os
from pathlib import Path

user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/OrbitNext/api-data-download")

import pandas as pd
import itertools
import argparse
import configparser
import warnings
warnings.filterwarnings("ignore")
from tabulate import tabulate

user_pthe_config = configparser.ConfigParser()
user_pthe_config.read(f"{user_home_path}/OrbitNext/api-data-download/user_info/user_path.ini")
PROJECT_PATH = user_pthe_config['project_path']['API_DATA_DOWNLOAD']

config = configparser.ConfigParser()
config.read(f"{user_home_path}/OrbitNext/api-data-download/key/confidential.ini")
API_KEY = config['PUBLIC_API_KEY']['API_KEY_1']

from main.channel_pool import *
from main.channel_video_stats import *
from main.youtube_build import youtube_builder
from main.utils import unname_df_column_remove
from tqdm import tqdm

def main():

    parser = argparse.ArgumentParser(description='channel pool id')
    parser.add_argument('--pool', help="Pool Type", required=True)
    args = parser.parse_args()
    pool = args.pool

    if pool == ChannelPool.POPULAR:
        channel_lst = popular_channel
    elif pool == ChannelPool.POTENTIAL:
        channel_lst = potential_channel
    elif pool == ChannelPool.EXAMPLE:
        channel_lst = example_channel
    else:
        raise(ValueError("pool is not define!"))
    # import the playist_id_df
    playist_id_df = pd.read_csv(f'{user_home_path}/OrbitNext/api-data-download/data_center/public_stats/playist_id/playist_id.csv')
    playist_id_df = unname_df_column_remove(playist_id_df)
    print(tabulate(playist_id_df, headers='keys', tablefmt='grid'))

    # get all channel video id
    all_videoId = []
    all_video_details = []
    for i in tqdm(playist_id_df['playlist_id']):
        video_ids = get_video_ids(youtube_builder, playlist_id=i)
        all_videoId.append(video_ids)
    print(all_videoId)

    for i in tqdm(all_videoId):
        all_video_details_df = get_video_details(youtube_builder, i)
        all_video_details.append(all_video_details_df)
    
    # all video Id df
    # to-do
    # try to add the relate column with channel name 
    os.makedirs(PROJECT_PATH + "/data_center/public_stats/video_details", exist_ok=True)
    all_videoId_df = pd.DataFrame(all_videoId)
    all_videoId_df = all_videoId_df.T
    all_videoId_df.to_csv(PROJECT_PATH + "/data_center/public_stats/video_details/all_videoId_df.csv")
    
    # all video detail
    # to-do
    # 2. handle the stats list in the column
    os.makedirs(PROJECT_PATH + "/data_center/public_stats/video_details", exist_ok=True)
    print(tabulate(all_video_details, headers='keys', tablefmt='simple'))
    all_video_details_df.to_csv(PROJECT_PATH + "/data_center/public_stats/video_details/all_video_details_df.csv")



if __name__ == '__main__':
    main()