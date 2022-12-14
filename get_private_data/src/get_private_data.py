import argparse
import os
import pickle
from glob import glob
from pdb import set_trace as bp  # noqa

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import API_SERVICE_NAME
from config import API_VERSION
from config import CLIENT_SECRETS
from config import SCOPES
from utils import makedir
from utils import save_auth_pkl
from channel_video_loader import *


def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(**kwargs).execute()
    return response


def get_authentication():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
    auth = flow.run_local_server()
    return auth


# def query(credentials: object, channel_id: str) -> pd.DataFrame:
#     credentials.refresh(Request())
#     auth = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
#     result = execute_api_request(
#         auth.reports().query,
#         ids=f'channel=={channel_id}',
#         # filters='video==omyZccg4FzI',
#         startDate='2021-10-31',
#         endDate='2021-12-31',
#         metrics='estimatedMinutesWatched,views,likes,subscribersGained',
#         dimensions='day',
#         sort='day'
#     )
#     col = [v['name'] for v in result['columnHeaders']]
#     return pd.DataFrame(result['rows'], columns=col)

video_id = main(pool = 'potential',print_description = '')
print(video_id)
print(len(video_id))
video=[]
for i in range(len(video_id)):
    video.append(video_id[0][i])
print(video)



def query(credentials: object, channel_id: str, video) -> pd.DataFrame:
    credentials.refresh(Request())
    auth = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    result = execute_api_request(
    auth.reports().query,
        ids=f'channel=={channel_id}',
        filters='video=='+str(video),#ylDObM4-T2E,Lh1TyNDa7sU,R2MgFQEDPoU,5tsZw0twNJ4
        startDate='2020-10-31',
        endDate='2021-12-31',
        metrics='estimatedMinutesWatched,views,likes,subscribersGained,views,redViews,comments,likes,dislikes,shares,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,annotationClickThroughRate,annotationCloseRate,annotationImpressions,annotationClickableImpressions,cardClickRate,cardTeaserClickRate,cardImpressions,cardTeaserImpressions,cardClicks,cardTeaserClicks,subscribersGained,subscribersLost,estimatedRevenue,estimatedAdRevenue,grossRevenue,estimatedRedPartnerRevenue,monetizedPlaybacks,playbackBasedCpm,adImpressions,cpm',
        dimensions='day',
        sort='day'
    )
    col = [v['name'] for v in result['columnHeaders']]
    return pd.DataFrame(result['rows'], columns=col)


def main(args):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # mkdir
    data_dir = makedir(os.path.join('..', '/Users/johnsonhsiao/api-data-download/get_private_data/data'))

    # get auth path
    if args.auth is None:  # get auth again
        channel_id = input('input your channel id: ')
        auth = get_authentication(channel_id)
        paths = [save_auth_pkl(channel_id, auth)]
    elif os.path.isfile(args.auth):  # get auth from single pkl file
        paths = [args.auth]
    elif os.path.isdir(args.auth):  # get auths from dir
        paths = glob(os.path.join(args.auth, '*.pkl'))

    # get data
    for path in paths:
        auth = pickle.load(open(path, 'rb'))
        channel_id = os.path.basename(path).split('.')[0]
        for i in video:
            df = query(auth, channel_id,i)

            save_path = os.path.join(data_dir, f'{i}.csv')
            df.to_csv(save_path, index=False)
        print(f'{save_path} saved')
        # every video


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth', help='.pkl or dir or None', default=None)
    args = parser.parse_args()

    main(args)
