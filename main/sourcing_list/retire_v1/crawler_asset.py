import time
import numpy
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def get_data():
	soup = BeautifulSoup(driver.page_source, "html.parser")
	title = soup.find_all("h4")
	content = soup.find_all("small")
	process_list = []
	content_list = []
	title_list = []
	subs = []
	videos = []
	views = []
	latest_video = []
	category = []
	link = []
	# get title
	for i in title:
		if i.get_text().strip() == "Export":
			break
		else:
			title_list.append(i.get_text().strip())
	# get ontent、category
	for i in content:
		process_list.append(i.get_text().strip().replace("\t",""))
	for j in range(len(process_list)-1):
		if process_list[j+1][0:13] == "Example Video":
			content_list.append(process_list[j].split("\n"))
			category.append(process_list[j-1])
		else:
			pass
	for k in content_list:
		subs.append(k[0])
		videos.append(k[1])
		views.append(k[2])
		latest_video.append(k[3])
	# channel link grab
	process_list=[]
	for links in soup.find_all("a",{'target':'_blank'}):
		process_list.append(links.get('href'))
	for i in range(len(process_list)):
		if process_list[i][0:5] == "/eng/":
			break
		else:
			link.append(process_list[i])
	link = numpy.unique(link).tolist()
	data_df = pd.DataFrame(title_list, columns = ["title"])
	data_df = pd.concat([data_df,pd.DataFrame(link, columns = ["link"]),pd.DataFrame(category, columns = ["category"]),pd.DataFrame(subs, columns = ["subs"]),pd.DataFrame(videos, columns = ["videos"]),pd.DataFrame(views, columns = ["views"]),pd.DataFrame(latest_video, columns = ["latest_video"])],axis = 1)

	return data_df

def website_ready(): # get web ready : https://channelcrawler.com/
	options = Options()
	# to-fix 
	chromedriver_path = "/Users/chouwilliam/OrbitNext/api-data-download/research/sourcing_list/geckodriver.exe"
	# driver = webdriver.Chrome(executable_path = chromedriver_path, chrome_options = options)
	driver = webdriver.Firefox(executable_path = chromedriver_path, chrome_options = options)
	print("1111")
	driver.get("https://channelcrawler.com/") # this is a target web 
	print("2222")
	# irst language and region 
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[4]/div/div/div[1]/div/span/input").click()
	time.sleep(0.5)
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[4]/div/div/div[2]/ul/li[221]").click()
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[3]/div/div/div[1]/div/span/input").click()
	time.sleep(0.5)
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[3]/div/div/div[2]/ul/li[35]").click()
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[2]/div/div/div[1]/div/span/input").click()

	return driver
