import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import numpy
import time

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

	#先抓標題
	for i in title:
		if i.get_text().strip() == "Export":
			break
		else:
			title_list.append(i.get_text().strip())

	#抓+處理content、category
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

	#抓Youtube頻道超連結
	process_list=[]
	for links in soup.find_all("a",{'target':'_blank'}):
		process_list.append(links.get('href'))
	for i in range(len(process_list)):
		if process_list[i][0:5] == "/eng/":
			break
		else:
			link.append(process_list[i])
	link = numpy.unique(link).tolist()

	#把輸出變成dataframe
	data_df = pd.DataFrame(title_list, columns = ["title"])
	data_df = pd.concat([data_df,pd.DataFrame(link, columns = ["link"]),pd.DataFrame(category, columns = ["category"]),pd.DataFrame(subs, columns = ["subs"]),pd.DataFrame(videos, columns = ["videos"]),pd.DataFrame(views, columns = ["views"]),pd.DataFrame(latest_video, columns = ["latest_video"])],axis = 1)

	return data_df

def website_ready(): #把網頁準備好，並輸入固定參數（語言、地區）
	options = Options()
	chromedriver_path = r"/Users/chouwilliam/OrbitNext/api-data-download/research/sourcing_list/driver_data/chromedriver/chromedriver.exe"
	driver = webdriver.Chrome(executable_path = chromedriver_path, chrome_options = options)
	driver.get("https://channelcrawler.com/")

	#先選語言、地區(由下往上選，不然會有問題)
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[4]/div/div/div[1]/div/span/input").click()
	time.sleep(0.5)
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[4]/div/div/div[2]/ul/li[221]").click()

	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[3]/div/div/div[1]/div/span/input").click()
	time.sleep(0.5)
	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[3]/div/div/div[2]/ul/li[35]").click()

	driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[2]/div/div/div[1]/div/span/input").click()

	return driver

output_df = pd.DataFrame()
for category in range(1,16) :
	for sub in range(9,17) : 
		driver = website_ready()
		driver.find_element(By.XPATH,"//*[@id='collapseOne']/div/div/div[1]/div[2]/div/div/div[2]/ul/li[" + str(category) + "]").click()
		#觀看數
		driver.find_element(By.XPATH,"//*[@id='queryMinSubs']").click()
		time.sleep(0.5)
		driver.find_element(By.XPATH,"//*[@id='queryMinSubs']/option[" + str(sub) + "]").click()

		driver.find_element(By.XPATH,"//*[@id='queryMaxSubs']").click()
		time.sleep(0.5)
		driver.find_element(By.XPATH,"//*[@id='queryMaxSubs']/option[" + str(sub + 1) + "]").click()
		#查詢
		driver.find_element(By.XPATH,"//*[@id='queryIndexForm']/div[3]/div/button").click()

		#結果頁爬取資料
		try:
			for i in range(13): #設13是因為最多13頁（250/20 = 12.5）
				add_df = get_data()
				output_df = pd.concat([output_df,add_df],axis = 0)

				'''if len(add_df) > 250: #檢查用
					print("需要多一層條件")
				else:
					continue'''

				try:
					#看能不能按下一頁
					driver.find_element(By.CLASS_NAME,"next")
					driver.find_element(By.LINK_TEXT,"Next").click()
				except:
					break
		except:
			print(category,sub + " Error")
			output_df.to_csv("C:/Users/user/Desktop/Youtube_Channel_List.csv", encoding = "utf-8", index = False)
			continue

		print(category,sub)
		print(output_df)

#刪除重複的title並把dataframe存成一個CSV檔
output_df = output_df.drop_duplicates(subset=["link"], keep='first', inplace=False)
output_df.to_csv("C:/Users/user/Desktop/Youtube_Channel_List.csv", encoding = "utf-8", index = False)
print(output_df)
print("Finished")