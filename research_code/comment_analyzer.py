from core.public_asset import *

# this is the on dealing with comment 
pyscriptVidId = 'Qo8dXyKXyME'
channelId = 'UCBJycsmduvYEL83R_U4JriQ' # MKBHDs

# response = search_result("pyscript")
response_stats = channel_stats(channelId) 
response = comment_threads(pyscriptVidId, to_csv=True)

# to-do and fix tonight

print(response)