# -*- coding: utf-8 -*-
import time
import selenium
from requests import get
import win32com.client as win32
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import re
import requests
import os
import csv

DATA_DIR = 'ScrapData'
TEMP_DIR = 'D:/Source_code/TestSchoolProject/seleniumCrawler/temp/'
CSV_POST = os.path.join(DATA_DIR, 'post_news.csv')

def main():
    URL = search_date()
    list = get_list(URL, "20200101", "20201231") # 수집할 새소식 기간 ex) (20200101, 20201231)
    scrap_content(list)

def scrap_content(list):
    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
    driver2.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초

    cols = ['date', 'department', 'title', 'content']

    if not os.path.exists(CSV_POST):
        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(cols)
    count = 0
    for post in list:
        count = count + 1
        print(count)
        #print(i.get_attribute("href"))
        driver2.get(url=post.get_attribute("href"))
        time.sleep(1)
        try:
            xpathDate = "/html/body/div[1]/div/section/div[2]/div[2]/form[1]/table/tbody/tr[1]/td[3]"
            xpathDepartment = "/html/body/div[1]/div/section/div[2]/div[2]/form[1]/table/tbody/tr[1]/td[1]"
            xpathTitle = "/html/body/div[1]/div/section/div[2]/div[2]/form[1]/table/thead/tr/th"
            xpathContent = "/html/body/div[1]/div/section/div[2]/div[2]/form[1]/table/tbody/tr[4]/td"
            xpathDownload = "/html/body/div[1]/div/section/div[2]/div[2]/form[1]/table/tbody/tr[3]/td"

            date = driver2.find_element_by_xpath(xpathDate).text
            department = driver2.find_element_by_xpath(xpathDepartment).text
            title = driver2.find_element_by_xpath(xpathTitle).text
            content = driver2.find_element_by_xpath(xpathContent).text

            # hwp 파일 txt로 불러와서 저장
            try:
                downList = driver2.find_element_by_xpath(xpathDownload).find_elements_by_tag_name("a")
                set_empty = True
                for i in downList:
                    print(i.text)
                    if re.match(r".*hwp", i.text):
                        if set_empty:
                            content = ""
                            set_empty = False
                        url = i.get_attribute("href")
                        download_hwp(url)
                        hwp_to_txt(TEMP_DIR)
                        content = content + get_text_file()
            except Exception as e:
                print(e)
                print("Hwp 파일이 없습니다. Content만 저장합니다.")

            print(
                "DATE : " + date + "\nDEPARTMENT : " + department + "\nTITLE : " + title + "\nCONTENT :" + content)
            content = remove_whitespaces(content)
            if len(content) == 0:
                content = "empty"
            row = [date, department, title, content]
            with open(CSV_POST, 'a', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(row)
        except:
            print("데이터가 비었습니다.")



def get_text_file():
    f = open("temp/temp_news.txt", mode='r')
    return f.read()


def hwp_to_txt(path):
    # hwp_to_txt()에 넘겨줄 hwpDispatch 사용이 끝난 후 hwp.Quit() 선언 필수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(path + "temp_news.hwp", "HWP", "forceopen:true")
    hwp.SaveAs(path + "temp_news.txt", "TEXT")
    hwp.Quit()


def download_hwp(url):
    hwpPath = "temp/temp_news.hwp"
    with open(hwpPath, "wb") as file:
        response = get(url)
        file.write(response.content)
        file.close()


def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    options.add_argument('headless')

    return options


def get_list(url, srtdate, enddate):
    driver = webdriver.Chrome('chromedriver', options=driver_option())
    driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
    driver.get(url=url)

    postList = []

    start_date = datetime.date(int(srtdate[:4]), int(srtdate[4:6]), int(srtdate[6:8]))
    end_date = datetime.date(int(enddate[:4]), int(enddate[4:6]), int(enddate[6:8]))

    dateList = driver.find_element_by_css_selector("tbody").find_elements_by_class_name("tb_writer")
    for i in dateList:
        text_date = datetime.datetime.strptime(i.text, '%Y-%m-%d').date()
        if text_date <= end_date:
            if text_date < start_date:
                break
            postList.append(i.find_element_by_xpath("preceding-sibling::td[@class='title_comm']//a"))
    print(len(postList))

    return postList


def read_html(url):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    html = requests.get(url=url, headers=headers)

    return html


def search_date():
    URL = "http://www.chungnam.go.kr/cnnet/board.do?"

    menuQuery = "mnu_cd=CNNMENU00148"
    pageQuery = "&pageNo=1"
    showQuery = "&showSplitNo=100000"

    URL = URL + menuQuery + pageQuery + showQuery
    print("Page 탐색 URL : " + URL)

    return URL


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)


if __name__ == '__main__':
    main()