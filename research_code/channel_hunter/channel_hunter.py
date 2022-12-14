import json
import sys
import os
import configparser
from pathlib import Path
user_home_path = str(Path.home())
sys.path.append(f"{user_home_path}/OrbitNext/api-data-download")

import requests
from tqdm import tqdm
import pandas as pd

user_pthe_config = configparser.ConfigParser()
user_pthe_config.read(f"{user_home_path}/OrbitNext/api-data-download/user_info/user_path.ini")
PROJECT_PATH = user_pthe_config['project_path']['API_DATA_DOWNLOAD']


class ChannelHunter:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_stats = None
        self.video_data = None

    def extract_all(self):
        self.get_channel_stats()
        self.get_channel_video_data()

    def download_channel_and_video_stats(self):
        self.get_channel_stats_and_download()
        self.get_channel_video_data_and_download()
    
    def get_channel_stats_and_download(self):
        channel_stats_data = self.get_channel_stats()
        channel_stats_df = pd.DataFrame({'value': [k for k in channel_stats_data.values()]}, index=[k for k in channel_stats_data.keys()])
        print('-----------')
        print(channel_stats_df.head(5))
        print('-----------')
        os.makedirs(PROJECT_PATH + '/data_center/public_stats/channel_stats_2', exist_ok=True)
        channel_stats_df.to_csv(PROJECT_PATH + '/data_center/public_stats/channel_stats_2/channel_stats_2.csv')
    
    def get_channel_video_data_and_download(self):
        channel_videos_data = self.get_channel_video_data()
        channel_videos_df = pd.DataFrame({'value': [k for k in channel_videos_data.values()]}, index=[k for k in channel_videos_data.keys()])
        print('-----------')
        print(channel_videos_df.head(5))
        print('-----------')
        os.makedirs(PROJECT_PATH + "/data_center/public_stats/video", exist_ok=True)
        channel_videos_df.to_csv(PROJECT_PATH + "/data_center/public_stats/video" + '/video_stats.csv')
    
    def get_channel_stats(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        """
        {
        "kind": "youtube#channelListResponse",
        "etag": "JUtr6KZNxSnQKpPovsZSMux8kVU",
        "pageInfo": {
            "totalResults": 1,
            "resultsPerPage": 5
        },
        "items": [
            {
            "kind": "youtube#channel",
            "etag": "VkHg0iMtTxvZDLbrxBpNGWUNK1M",
            "id": "UCMUnInmOkrWN4gof9KlhNmQ",
            "statistics": {
                "viewCount": "1358449507",
                "subscriberCount": "5030000",
                "hiddenSubscriberCount": false,
                "videoCount": "251"
            }
            }
        ]
        }
        """

        try: 
            data = data["items"][0]["statistics"]
        except:
            data = None
        self.channel_stats = data

        return data
    
    # def get_channel_video_data(self):
    #     # get video id
    #     print('get video data...')
    #     channel_videos = self._get_channel_videos(limit=50)
    #     print(channel_videos)
    #     print(f"Video Num ; {len(channel_videos)}")
    #     # get video stats
    #     parts = ["snippet", "statistics", "contentDetails"]

    #     for video_id in tqdm(channel_videos):
    #         for part in parts:
    #             data = self._get_single_video_data(video_id, part)
    #             channel_videos[video_id].update(data)
        
    #     self.video_data = channel_videos
    #     return channel_videos
    
    def get_channel_video_data(self, youtube, playlist_id):

        requests = youtube.playlistItems().list(
                part = "contentDetails", 
                playlistId = playlist_id,
                maxResults = 50
            )
        response = requests.execute()
        video_ids = []
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])
        next_page_token = response.get('nextPageToken')
        more_pages = True

        while more_pages:
            if next_page_token is None:
                more_pages = False
            else:
                requests = youtube.playlistItems().list(
                        part = "contentDetails", 
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token
                    )
                response = requests.execute()

                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])
                next_page_token = response.get('nextPageToken')

            return video_ids
        
    
    def _get_single_video_data(self, video_id, part):
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]

        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        
        return data

    def _get_channel_videos(self, limit=None):
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelID={self.channel_id}&part=id&order=date"

        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        vid, npt = self._get_channel_videos_per_page(url)
        idx = 0
        while(npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            next_vid, npt = self._get_channel_videos_per_page(nexturl)
            vid.update(next_vid) # dict append
            idx += 1 
        return vid
    
    def _get_channel_videos_per_page(self, url):

        """
        Extract all videos and playlists per page
        return channel_videos, channel_playlists, nextPageToken
        """
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()

        if "items" not in data:
            print('Error! Could not get correct channel data!\n', data)
            return channel_videos, None
        
        nextPageToken = data.get("nextPageToken", None)
        item_data = data["items"]
        
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == "youtube#video":
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError:
                print("Error!!")
        
        return channel_videos, nextPageToken

    def data_dump(self):
        if self.channel_stats is None or self.video_data is None:
            print('Data is None!!!')
            return
        
        agg_data = {self.channel_id: {"channel_stats": self.channel_stats, "video_data": self.video_data}}
        
        channel_title = self.video_data.popitem()[1].get("channelTitle", self.channel_id)

        channel_title = channel_title.replace(" ", "_").lower()
        file_name = channel_title + '.json'
        with open(file_name, 'w') as f:
            json.dump(agg_data, f, indent=4)
        print(f'file dump to {file_name}')
