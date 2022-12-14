import os
import pickle

from config import AUTH_DIR


def save_auth_pkl(channel_id: str, auth: object):
    makedir(AUTH_DIR)
    path = os.path.join(AUTH_DIR, f'{channel_id}.pkl')
    pickle.dump(auth, open(path, 'wb'))
    return path


def makedir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
    return path
