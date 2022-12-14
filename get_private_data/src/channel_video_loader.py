import os
import pandas as pd
import itertools
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
user_home_path = str(Path.home())

import sys
sys.path.append(f'{user_home_path}/api-data-download')

import configparser
project_path_config = configparser.ConfigParser()
project_path_config.read(f'{user_home_path}/api-data-download/user_info/user_path.ini')
PROJECT_PATH = project_path_config['PROJECT_PATH']['API_DATA_DOWNLOAD']

from tabulate import tabulate
from tqdm import tqdm
import click

from main.channel_pool import *
from main.channel_video_stats import *
from main.youtube_build import YT_BUILDER, PROJECT_PATH
from main.utils import unname_df_column_remove

# @click.command()
# @click.option('--pool', 'pool', type=str, help='Pool Type', required=True)
# @click.option('--print_description', 'print_description', help='whether print messy description data', default=False, show_default=True)
def main(pool, print_description):

    if pool == ChannelPool.POPULAR:
        pool = popular_channel
    elif pool == ChannelPool.POTENTIAL:
        pool = potential_channel
    elif pool == ChannelPool.EXAMPLE:
        pool = example_channel
    else:
        raise(ValueError('pool is not define!'))

    all_channel_stats = pd.DataFrame()
    all_channel_description = pd.DataFrame(columns=['channel_name'])
    all_channel_playlistId_data = pd.DataFrame(columns=['channel_name'])

    for key, group in itertools.groupby(pool, lambda x: x[0] + '|' + x[1]):
        channel_id, channel_name = key.split('|')
        pool = list(group)
        for i in tqdm(range(len(pool))):
            single_channel_id = [x[i] for x in pool]
            each_channel_stats, eac_channel_description, eac_channel_playlistId= get_channel_stats(YT_BUILDER, single_channel_id)
            all_channel_stats = all_channel_stats.append(each_channel_stats)
            all_channel_description = all_channel_description.append(eac_channel_description)
            all_channel_playlistId_data = all_channel_playlistId_data.append(eac_channel_playlistId)
    print(tabulate(all_channel_stats, headers='keys', tablefmt='grid'))
    print(tabulate(all_channel_playlistId_data, headers='keys', tablefmt='grid'))
    # too messy to print
    if print_description:
        print(tabulate(all_channel_description, headers='channel_name', tablefmt='grid'))

    all_channel_stats = unname_df_column_remove(all_channel_stats)
    os.makedirs(PROJECT_PATH + '/data_center/public_stats/channel_stats', exist_ok=True)
    all_channel_stats.to_csv(PROJECT_PATH + '/data_center/public_stats/channel_stats/' + '/channel_stats.csv')

    all_channel_description = unname_df_column_remove(all_channel_description)
    os.makedirs(PROJECT_PATH + '/data_center/public_stats/channel_description', exist_ok=True)
    all_channel_description.to_csv(PROJECT_PATH + '/data_center/public_stats/channel_description' + '/channel_description.csv')

    all_channel_playlistId_data = unname_df_column_remove(all_channel_playlistId_data)
    playist_id_df = unname_df_column_remove(all_channel_playlistId_data)

    os.makedirs(PROJECT_PATH + '/data_center/public_stats/playist_id', exist_ok=True)
    playist_id_df.to_csv(PROJECT_PATH + '/data_center/public_stats/playist_id' + '/playist_id.csv')
    print(f'channel playlistId data saved at {PROJECT_PATH}' + '/data_center/public_stats/playist_id/playist_id.csv')

    # get all channel video id
    all_videoId = []
    all_video_details = []

    for i in tqdm(playist_id_df['playlist_id']):
        video_ids = get_video_ids(YT_BUILDER, playlist_id=i)
        all_videoId.append(video_ids)
    # print(all_videoId)
    for i in tqdm(range(len(all_videoId))):
        a = get_video_details_list(YT_BUILDER, all_videoId[i])
        all_video_details.append(a)
    # use itertools to merge speprated lists 
    all_video_details = list(itertools.chain(*all_video_details))
    all_video_details_df = pd.DataFrame(all_video_details)
    
    print(tabulate(all_video_details_df, headers='keys', tablefmt='grid'))
    # all video id df
    os.makedirs(PROJECT_PATH + '/data_center/public_stats/video_details', exist_ok=True)
    all_videoId_df = pd.DataFrame(all_videoId)
    all_videoId_df = all_videoId_df.T
    all_videoId_df.to_csv(PROJECT_PATH + '/data_center/public_stats/video_details/all_videoId_df.csv') 
    
    # all video detail
    os.makedirs(PROJECT_PATH + '/data_center/public_stats/video_details', exist_ok=True)
    all_video_details_df.to_csv(PROJECT_PATH + '/data_center/public_stats/video_details/all_video_details_df.csv') # to-do handle the stats list in the column   
    return all_videoId_df
    
if __name__ == '__main__':
    main()