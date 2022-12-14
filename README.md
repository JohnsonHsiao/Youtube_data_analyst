# api-data-download
## Installation
Use `conda` to build your environment and install requirement pakages.
### Create conda env and activate
```bash
conda create --name orbitnext python=3.9
conda activate orbitnext
```
### Install pakages
```bash
conda install pandas=1.4.3
pip install tabulate==0.8.10
pip install tqdm==4.64.0
pip install google-api-python-client
pip install click
pip install jupyter notebook
```

## Tutorial
### Get public channel status
```bash
python initiate_load/public_access/load_channel_stats.py --pool <pool_name>
```

## First-time users
## Setting up
- Create `user_path.ini` file to store this project path
- Create `confidential.ini` file to store the private key

## Grab Public Data
 ```bash
python initiate_load/public_access/channel_video_loader.py --pool <pool_name>
```

## Grab Private Data
 ```bash
python initiate_load/private_access/private_analyzer.py --channel_id MINE

python initiate_load/private_access/private_analyzer.py --channel_id <Channel_Id>
```

Pool name choises
* example
* potential
* popular

Find more details in `main/channel_pool.py`.
