# -*- coding: utf-8 -*-
import time
from requests import get
import win32com.client as win32
from selenium import webdriver
import datetime
import re
import os
import csv

DATA_DIR = '../../ScrapData'
TEMP_DIR = os.path.join(os.getcwd(), "../temp/")
CSV_POST = os.path.join(DATA_DIR, 'post_cheonan.csv')
TEMP_TXT_FILE = "temp_cheonan.txt"
TEMP_HW_FILE = "temp_cheonan.hwp"

def main():
    get_list("20200101", "20201231") # 수집할 새소식 기간 ex) (20200101, 20201231)



def get_list(srtdate, enddate):
    start_date = datetime.date(int(srtdate[:4]), int(srtdate[4:6]), int(srtdate[6:8]))
    end_date = datetime.date(int(enddate[:4]), int(enddate[4:6]), int(enddate[6:8]))

    # 스크랩 기능 구현
    cols = ['date', 'department', 'title', 'content']
    count = 0

    if not os.path.exists(CSV_POST):
        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(cols)

    for i in range(181, 384):
        driver = webdriver.Chrome('chromedriver', options=driver_option())
        driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
        url = "https://www.cheonan.go.kr/cop/bbs/BBSMSTR_000000000472/selectBoardList.do?pageIndex=" + str(i)
        driver.get(url=url)
        tr = driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")

        for i in tr:
            td = i.find_elements_by_tag_name("td")
            date = td[4].text
            text_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

            if text_date <= end_date:
                if text_date < start_date:
                    break

                try:
                    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
                    driver2.implicitly_wait(time_to_wait=10)
                    driver2.get(url=td[2].find_element_by_tag_name("a").get_attribute("href"))
                    time.sleep(1)

                    count += 1
                    print(count)
                    xpathTitle = "/html/body/div/div[5]/div/div[2]/div/div[1]/table/tbody/tr[1]/td"

                    department = td[3].text
                    title = driver2.find_element_by_xpath(xpathTitle).text

                    content = driver2.find_element_by_class_name("bbs-view-content-skin05").text
                    content = remove_whitespaces(content)

                    print(
                        "DATE : " + date + "\nDEPARTMENT : " + department + "\nTITLE : " + title + "\nCONTENT :" + content)

                    if len(content) == 0:
                        content = "empty"

                    with open(CSV_POST, 'a', newline='', encoding='utf-8') as f:
                        row = [date, department, title, content]
                        w = csv.writer(f)
                        w.writerow(row)

                except Exception as e:
                    print(e)
                    print("데이터가 비었습니다.")

                driver2.close()

            if text_date < start_date:
                break
        driver.close()


def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    options.add_argument('headless')

    return options


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)


if __name__ == '__main__':
    main()