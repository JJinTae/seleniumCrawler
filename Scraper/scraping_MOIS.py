# -*- coding: utf-8 -*-
import time
from requests import get
import win32com.client as win32
from selenium import webdriver
import datetime
import re
import os
import csv

DATA_DIR = '../ScrapData'
TEMP_DIR = os.path.join(os.getcwd(), "temp/")
CSV_POST = os.path.join(DATA_DIR, 'post_mois.csv')

def main():
    get_list("20210725", "20210726") # 수집할 새소식 기간 ex) (20200101, 20201231)


def get_text_file():
    f = open("temp/temp_mois.txt", mode='r')
    return f.read()


def hwp_to_txt(path):
    # hwp_to_txt()에 넘겨줄 hwpDispatch 사용이 끝난 후 hwp.Quit() 선언 필수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    hwp.Open(path + "temp_mois.hwp", "HWP", "forceopen:true")
    hwp.SaveAs(path + "temp_mois.txt", "TEXT")
    hwp.Quit()


def download_hwp(url):
    hwpPath = "temp/temp_mois.hwp"
    with open(hwpPath, "wb") as file:
        response = get(url)
        file.write(response.content)
        file.close()


def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    # options.add_argument('headless')

    return options


def get_list(srtdate, enddate):
    start_date = datetime.date(int(srtdate[:4]), int(srtdate[4:6]), int(srtdate[6:8]))
    end_date = datetime.date(int(enddate[:4]), int(enddate[4:6]), int(enddate[6:8]))

    postList = []

    for i in range(1, 3):
        driver = webdriver.Chrome('chromedriver', options=driver_option())
        driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
        url = "https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008&pageIndex=" + str(i)
        driver.get(url=url)
        tr = driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")

        for i in tr:
            td = i.find_elements_by_tag_name("td")
            date = td[4].text
            text_date = datetime.datetime.strptime(date, '%Y.%m.%d.').date()

            if text_date <= end_date:
                if text_date < start_date:
                    break
                try:
                    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
                    driver2.implicitly_wait(time_to_wait=10)
                    driver2.get(url=td[1].find_element_by_tag_name("a").get_attribute("href"))
                    time.sleep(1)

                    # 스크랩 기능 구현
                    cols = ['date', 'department', 'title', 'content']

                    if not os.path.exists(CSV_POST):
                        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
                            w = csv.writer(f)
                            w.writerow(cols)

                    xpathContent = "/html/body/div/div[5]/div/div[2]/div[4]/form/div/div[3]"
                    xpathDownload = "/html/body/div/div[5]/div/div[2]/div[4]/form/div/dl[1]/dd/div/ul"

                    department = td[3].text
                    title = td[1].text
                    content = driver2.find_element_by_xpath(xpathContent).text

                    # hwp 파일 txt로 불러와서 저장
                    try:
                        downList = []
                        fileList = driver2.find_element_by_xpath(xpathDownload).find_elements_by_tag_name("li")
                        for li in fileList:
                            downList.append(li.find_element_by_tag_name("a"))
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

                    with open(CSV_POST, 'a', newline='', encoding='utf-8') as f:
                        row = [date, department, title, content]
                        w = csv.writer(f)
                        w.writerow(row)

                except:
                    print("데이터가 비었습니다.")

                driver2.close()

            if text_date < start_date:
                break

        driver.close()

    return postList


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)


if __name__ == '__main__':
    main()