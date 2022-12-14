# get private data
## Installation
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## First-time users
```bash
mkdir key
cp [YOUR_SECREY_KEY.json] key/[YOUR_SECREY_KEY.json]
```

## Tutorial
### Get data from pickle
```bash
python src/get_private_data.py --auth ../auths/[PICKLE_FILE]
```

### Host web server
```bash
python src/server.py
```
You can change config of YouTube API, ip, port in config.py.
