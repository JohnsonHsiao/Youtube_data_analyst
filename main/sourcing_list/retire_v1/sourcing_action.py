import csv
import os
import time
from pathlib import Path
import numpy
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from crawler_asset import get_data, website_ready
from webdriver_manager.chrome import ChromeDriverManager

# locate the path 
from pathlib import Path
user_home_path = str(Path.home())
import sys
sys.path.append(f'{user_home_path}/api-data-download')

import configparser
project_path_config = configparser.ConfigParser()
project_path_config.read(f'{user_home_path}/api-data-download/user_info/user_path.ini')
PROJECT_PATH = project_path_config['PROJECT_PATH']['API_DATA_DOWNLOAD']


def main():

	# driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')

	# # fp = webdriver.FirefoxProfile()

	# driver = webdriver.Firefox()

	driver.get("https://channelcrawler.com/")
	driver.close()

	output_df = pd.DataFrame()
	for category in range(1,16) :
		for sub in range(9,17) : 
			driver = website_ready()
			driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[2]/div/div/div[2]/ul/li[" + str(category) + "]").click()
			# num of views
			driver.find_element(By.XPATH,"//*[@id='queryMinSubs']").click()
			time.sleep(0.5)
			driver.find_element(By.XPATH,"//*[@id='queryMinSubs']/option[" + str(sub) + "]").click()
			driver.find_element(By.XPATH,"//*[@id='queryMaxSubs']").click()
			time.sleep(0.5)
			driver.find_element(By.XPATH,"//*[@id='queryMaxSubs']/option[" + str(sub + 1) + "]").click()
			# search button
			driver.find_element(By.XPATH,"//*[@id='queryIndexForm']/div[3]/div/button").click()

			try:
				for i in range(13): # man 13 pages（250/20 = 12.5）
					add_df = get_data()
					output_df = pd.concat([output_df,add_df],axis = 0)

					"""
					if len(add_df) > 250: #檢查用
						print("需要多一層條件")
					else:
						continue
					"""

					try:
						# chances to go next page 
						driver.find_element(By.CLASS_NAME,"next")
						driver.find_element(By.LINK_TEXT,"Next").click()
					except:
						break
			except:
				print(category,sub + " Error")
				output_df.to_csv(f"{user_home_path}/api-data-download/source_df/Youtube_Channel_List.csv", encoding = "utf-8", index = False)
				continue

			print(category,sub)
			print(output_df)

	# delete duplicate link 
	output_df = output_df.drop_duplicates(subset=["link"], keep='first', inplace=False)

	os.makedirs(PROJECT_PATH + '/data_center/public_stats/sourcing_channel', exist_ok=True)
	output_df.to_csv(PROJECT_PATH + '/data_center/public_stats/sourcing_channel/channel_list.csv', encoding = "utf-8", index = False)
	print(output_df.head(20))
	print("Finished")


if __name__ == '__main__':
    main()