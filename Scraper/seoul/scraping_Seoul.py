# -*- coding: utf-8 -*-
import time
from selenium.webdriver.support import expected_conditions as EC

from requests import get
import win32com.client as win32
from selenium import webdriver
import re
import requests
import os
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

DATA_DIR = '../../ScrapData'
TEMP_DIR = os.path.join(os.getcwd(), "../temp/")
CSV_POST = os.path.join(DATA_DIR, 'post_seoul_problem.csv')
TEMP_TXT_FILE = "temp_seoul.txt"
TEMP_HW_FILE = "temp_seoul.hwp"

def main():
    URL = search_date(20200101, 20200131) # 수집할 공고고시 기간 ex) search_date(20200101, 20201231)
    list = get_list(URL)
    scrap_content(list)

def scrap_content(list):
    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
    driver2.implicitly_wait(time_to_wait=10)  # 암묵적 대기 단위 초

    cols = ['date', 'department', 'title', 'content']
    count = 0

    if not os.path.exists(CSV_POST):
        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(cols)

    for post in list:
        driver2 = webdriver.Chrome('chromedriver', options=driver_option())
        driver2.implicitly_wait(time_to_wait=10)  # 암묵적 대기 단위 초

        print("들어왔습니다.")
        count += 1
        print(count)
        print(post)
        #print(i.get_attribute("href"))
        driver2.get(url="https://www.seoul.go.kr/news/news_report.do#view/" + post)

        element_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/thead/tr[1]/th/p[1]"))

        WebDriverWait(driver2, 10).until(
            element_present
            # EC.invisibility_of_element((By.ID, "scrabArea"))
            # EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sib-viw-type-basic-subject-name"))
        )

        time.sleep(1)

        try:
            xpathDate = "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/thead/tr[1]/th/p[3]/span[1]"
            xpathDepartment1 = "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/thead/tr[1]/th/p[2]/span[2]"
            xpathDepartment2 = "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/thead/tr[1]/th/p[3]/span[2]"
            xpathTitle = "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/thead/tr[1]/th/p[1]"
            xpathContent = "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/tbody/tr/td"
            #xpathDownload = "/html/body/div[2]/section/div/div[2]/div[2]/div/div[1]/table/thead/tr[4]/td/p"

            date = driver2.find_element_by_xpath(xpathDate).text
            department = driver2.find_element_by_xpath(xpathDepartment1).text + " " + driver2.find_element_by_xpath(xpathDepartment2).text
            title = driver2.find_element_by_xpath(xpathTitle).text
            content = driver2.find_element_by_xpath(xpathContent).text

            # hwp 파일 txt로 불러와서 저장
            try:
                downList = driver2.find_element_by_class_name("sib-viw-type-basic-file").find_elements_by_tag_name("p")
                set_empty = True
                print(downList[0].get_attribute("data-fileno"))
                print("downList ", len(downList))

                #한 게시글에 파일이 두 개 이상 존재할 경우
                if len(downList) > 1:
                    print("파일이 두 개 이상 존재합니다.")

                for i in downList:
                    print(i.text)
                    if re.match(r".*(hwp|hwpx)", i.text):
                        if set_empty:
                            content = ""
                            set_empty = False
                        #url = i.get_attribute("href")
                        url = "https://seoulboard.seoul.go.kr/comm/getFile?srvcId=BBSTY1&upperNo="+post+"&fileTy=ATTACH&fileNo="+i.get_attribute("data-fileno")+"&bbsNo=158"
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
        except Exception as e:
            print("데이터가 비었습니다.")
            print(e)

        driver2.close()


def get_text_file():
    f = open(TEMP_DIR + TEMP_TXT_FILE, mode='r')
    return f.read()


def hwp_to_txt(path):
    # hwp_to_txt()에 넘겨줄 hwpDispatch 사용이 끝난 후 hwp.Quit() 선언 필수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(path + TEMP_HW_FILE, "HWP", "forceopen:true")
    hwp.SaveAs(path + TEMP_TXT_FILE, "TEXT")
    hwp.Quit()


def download_hwp(url):
    hwpPath = TEMP_DIR + TEMP_HW_FILE
    with open(hwpPath, "wb") as file:
        response = get(url)
        file.write(response.content)
        file.close()


def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    # options.add_argument('headless')

    return options


def get_list(url):
    driver = webdriver.Chrome('chromedriver', options=driver_option())
    driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
    driver.get(url=url)
    time.sleep(10)

    postList = []

    tempList = driver.find_elements_by_class_name('sib-lst-type-basic-subject')
    for td in tempList :
        postList.append(td.find_element_by_tag_name('a').get_attribute('data-code'))

    print(len(postList))

    return postList


def read_html(url):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    html = requests.get(url=url, headers=headers)

    return html


def search_date(srtdate, enddate):
    URL = "https://www.seoul.go.kr/"

    menuQuery = "news/news_report.do"
    pageQuery = "#list/1/"
    strdateQuery = "&srchBeginDt=" + str(srtdate)
    enddateQuery = "&srchEndDt=" + str(enddate)
    showQuery = "&cntPerPage=100"

    URL = URL + menuQuery + pageQuery + strdateQuery + enddateQuery + showQuery
    print("Page 탐색 URL : " + URL)

    return URL


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)



if __name__ == '__main__':
    main()