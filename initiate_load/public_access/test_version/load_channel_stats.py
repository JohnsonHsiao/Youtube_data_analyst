import sys
from pathlib import Path
sys.path.append(".")

import configparser
import pandas as pd
import itertools
import warnings
import argparse
warnings.filterwarnings("ignore")
from tabulate import tabulate
from tqdm import tqdm
import click

PROJECT_PATH = Path(".")

config = configparser.ConfigParser()
config.read("key/confidential.ini")
API_KEY = config['PUBLIC_API_KEY']['API_KEY_3']

from main.channel_pool import *
from main.channel_video_stats import *
from main.youtube_build import youtube_builder
from main.utils import unname_df_column_remove


@click.command()
@click.option('--pool', 'pool', type=str, help='Pool Type', required=True)
@click.option('--print_description', 'print_description', help='whether print messy description data', default=False, show_default=True)
def main(pool, print_description):

    if pool == ChannelPool.POPULAR:
        channel_lst = popular_channel
    elif pool == ChannelPool.POTENTIAL:
        channel_lst = potential_channel
    elif pool == ChannelPool.EXAMPLE:
        channel_lst = example_channel
    else:
        raise(ValueError("pool is not define!"))

    all_channel_stats = pd.DataFrame()
    all_channel_description = pd.DataFrame(columns=['channel_name'])
    all_channel_playlistId_data = pd.DataFrame(columns=['channel_name'])
    
    print('Channnel data load...')
    for key, group in itertools.groupby(channel_lst, lambda x: x[0] + '|' + x[1]):
        channel_id, channel_name = key.split('|')
        pool = list(group)
        for i in tqdm(range(len(pool))):
            single_channel_id = [x[i] for x in pool]
            each_channel_stats, eac_channel_description, eac_channel_playlistId= get_channel_stats(youtube_builder, single_channel_id)
            all_channel_stats = all_channel_stats.append(each_channel_stats)
            all_channel_description = all_channel_description.append(eac_channel_description)
            all_channel_playlistId_data = all_channel_playlistId_data.append(eac_channel_playlistId)

    print(tabulate(all_channel_stats, headers='keys', tablefmt='grid'))
    print(tabulate(all_channel_playlistId_data, headers='keys', tablefmt='grid'))
    # too messy to print
    if print_description:
        print(tabulate(all_channel_description, headers='channel_name', tablefmt='grid'))

    # create file 
    (PROJECT_PATH / "data_center/public_stats/channel_stats").mkdir(parents=True, exist_ok=True)
    (PROJECT_PATH / "data_center/public_stats/channel_description").mkdir(parents=True, exist_ok=True)
    (PROJECT_PATH / "data_center/public_stats/playist_id").mkdir(parents=True, exist_ok=True)

    # path_fix 
    all_channel_stats = unname_df_column_remove(all_channel_stats)
    all_channel_stats.to_csv(PROJECT_PATH / 'data_center/public_stats/channel_stats/channel_stats.csv')
    print('channel stats data saved!')
    all_channel_description = unname_df_column_remove(all_channel_description)
    all_channel_description.to_csv(PROJECT_PATH / 'data_center/public_stats/channel_description/channel_description.csv')
    print('channel description data saved!')
    all_channel_playlistId_data = unname_df_column_remove(all_channel_playlistId_data)
    all_channel_playlistId_data.to_csv(PROJECT_PATH / 'data_center/public_stats/playist_id/playist_id.csv')
    print('channel playlistId data saved!')

if __name__ == '__main__':
    main()
