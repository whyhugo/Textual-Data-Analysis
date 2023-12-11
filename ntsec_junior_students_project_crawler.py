#匯入所有爬蟲常用套件
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from lxml import etree
import time

#設置 webdriver
chrome_options = webdriver.ChromeOptions()
#關閉彈出視窗
chrome_options.add_argument('--headless')
#安全性關閉 sandbox mode
chrome_options.add_argument('--no-sandbox')

#讀取我的 chromedriver 的位置，並設置 webdriver
driver = webdriver.Chrome('/programing/swiftx/chromedriver-win64/chromedriver.exe', options=chrome_options)

#建立需使用的儲存容器
#用於儲存所有科展作品的作品名稱
titles_list = []
#用於儲存所有科展作品的作品摘要
contents_list = []

#由於頁碼與網址有關連性，用迴圈方式進行爬取
for page in range(1, 310): 
    #每一次迴圈換頁碼
    url = f'https://www.ntsec.edu.tw/science/list.aspx?a=21&cat=52&p={page}' 
    #獲取網頁 html 碼
    html = driver.get(url)
    #剖析網頁
    sp = soup(driver.page_source, 'lxml')

    #每次迴圈開始記錄下頁數，用於最後分隔各頁資料
    titles_list.append(f'第 {page} 頁') 
    #用於分隔各頁資料
    contents_list.append("") 

    #單一頁面結構整齊，直接使用 find_all() 爬取資料
    #爬取所有在 class 為 scient-item-title 的 <div> 中的作品標題
    titles = sp.find_all('div', class_='scient-item-title')
    #爬取所有在 class 為 normal-18 的 <p> 中的作品標題
    contents = sp.find_all('p', class_='normal-18')

    #把這一個頁面所有的作品名稱逐一存入 list 容器
    for title in titles:
        #須加上 .text 才能取出文字
        titles_list.append(title.text)

    #把這一個頁面所有的作品摘要逐一存入 list 容器
    for content in contents:
        #須加上 .text 才能取出文字
        contents_list.append(content.text)

    #每頁任務完成後輸出提示，方便觀察爬取進度
    print(f'Page {page} has done!')

    #每次換頁間隔 1.5 秒
    time.sleep(1.5) 

#把以下內容寫入 txt 檔案格式
with open('ntsec_junior_students_project_info.txt', 'w', encoding='utf-8') as file: 
    #寫入標題
    file.write(f"【全國中小學科展作品 國中組作品集 - 臺灣網路科教館】\n\n")
    #用迴圈讀取儲存資料的 list
    for i in range(len(titles_list)):
        #若是分隔頁的元素，寫入以下資訊，用於分隔各頁資料
        if titles_list[i][0] == "第" and titles_list[i][-1] == "頁": 
            file.write(f"------------------------------------------- {titles_list[i]} -------------------------------------------\n\n")
        else:
            #寫入已經存入 list 中的作品標題
            file.write(f"作品名稱：{titles_list[i]}\n")
            #寫入已經存入 list 中的作品摘要 
            file.write(f"摘要：{contents_list[i]}\n\n") 

#所有任務完成後輸出提示（若想更便利可放入 LINE Notify 通知）
print(f'All you need was right there~') 
