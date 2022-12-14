import argparse
import json

from google.oauth2.credentials import Credentials

from utils import save_auth_pkl


def json2pickle(path):
    auth = json.load(open(path, 'r'))
    save_auth_pkl('test', Credentials(**auth))


def main(args):
    json2pickle(args.json_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', help='path of json file')
    args = parser.parse_args()

    main(args)