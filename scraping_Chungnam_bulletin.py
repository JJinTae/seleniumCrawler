# -*- coding: utf-8 -*-
import time
import selenium
from requests import get
import win32com.client as win32
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import os
import csv

DATA_DIR = 'ScrapData'
TEMP_DIR = 'D:/Source_code/TestSchoolProject/seleniumCrawler/temp/'
CSV_POST = os.path.join(DATA_DIR, 'post_bulletin.csv')

def main():
    URL = search_date(20201202, 20201202) # 수집할 공고고시 기간 ex) search_date(20200101, 20201231)
    list = get_list(URL)
    scrap_content(list)



    """
    for url in list:
        html = read_html(url)
        soup = BeautifulSoup(html.text, "html.parser")
        date = soup.select("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[2]/td[1]")
        department = 1
        title = 1
        content = 1
    """

    # driver.execute_script("window.history.go(-1)") 뒤로가기
    """
    page_bar = driver.find_elements_by_css_selector("div.pagination > *")
    for i in page_bar:
        print(i.text)
    """

def scrap_content(list):
    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
    driver2.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초



    cols = ['date', 'department', 'title', 'content']
    count = 0
    flag = False

    if not os.path.exists(CSV_POST):
        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(cols)

    for post in list:
        if(flag):
            print("들어왔습니다.")
            count += 1
            flag = False
            print(count)
            #print(i.get_attribute("href"))
            driver2.get(url=post.get_attribute("href"))
            time.sleep(1)
            try:
                xpathDate = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[14]/td"
                xpathDepartment = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[6]/td"
                xpathTitle = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[8]/td"
                xpathContent = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[12]/td"
                xpathDownload = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/table/tbody/tr[16]/td/table"

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
                        if re.match(r".*(hwp)$", i.text):
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

        else:
            print("통과되었습니다.")
            flag = True





def get_text_file():
    f = open("temp/temp_bulletin.txt", mode='r')
    return f.read()


def hwp_to_txt(path):
    # hwp_to_txt()에 넘겨줄 hwpDispatch 사용이 끝난 후 hwp.Quit() 선언 필수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(path + "temp_bulletin.hwp", "HWP", "forceopen:true")
    hwp.SaveAs(path + "temp_bulletin.txt", "TEXT")
    hwp.Quit()


def download_hwp(url):
    hwpPath = "temp/temp_bulletin.hwp"
    with open(hwpPath, "wb") as file:
        response = get(url)
        file.write(response.content)
        file.close()


def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    options.add_argument('headless')

    return options


def get_list(url):
    driver = webdriver.Chrome('chromedriver', options=driver_option())
    driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
    driver.get(url=url)

    postList = driver.find_element_by_css_selector("tbody").find_elements_by_tag_name("a")
    print(len(postList))

    return postList


def read_html(url):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    html = requests.get(url=url, headers=headers)

    return html


def search_date(srtdate, enddate):
    URL = "http://www.chungnam.go.kr/cnnet/board.do?"

    menuQuery = "mnu_cd=CNNMENU02364"
    pageQuery = "&pageNo=1"
    showQuery = "&showSplitNo=100000"
    strdateQuery = "&srtdate=" + str(srtdate)
    enddateQuery = "&enddate=" + str(enddate)

    URL = URL + menuQuery + pageQuery + showQuery + strdateQuery + enddateQuery
    print("Page 탐색 URL : " + URL)

    return URL


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)



if __name__ == '__main__':
    main()