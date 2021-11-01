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
CSV_POST = os.path.join(DATA_DIR, 'post_munche_problem.csv')
TEMP_TXT_FILE = "temp_munche.txt"
TEMP_HW_FILE = "temp_munche.hwp"

def main():
    get_list("20211025", "20211025") # 수집할 새소식 기간 ex) (20200101, 20201231)



def get_list(srtdate, enddate):
    start_date = datetime.date(int(srtdate[:4]), int(srtdate[4:6]), int(srtdate[6:8]))
    end_date = datetime.date(int(enddate[:4]), int(enddate[4:6]), int(enddate[6:8]))

    # 스크랩 기능 구현
    cols = ['date', 'department', 'title', 'content']
    postList = []

    if not os.path.exists(CSV_POST):
        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(cols)

    for i in range(2, 3):
        driver = webdriver.Chrome('chromedriver', options=driver_option())
        driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
        url = "https://www.mcst.go.kr/kor/s_notice/press/pressList.jsp?pCurrentPage=" + str(i)
        driver.get(url=url)
        tr = driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")

        for i in tr:
            td = i.find_elements_by_tag_name("td")
            date = td[2].text
            date = date.replace(" ", "")
            text_date = datetime.datetime.strptime(date, '%Y.%m.%d.').date()

            if text_date <= end_date:
                if text_date < start_date:
                    break

                try:
                    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
                    driver2.implicitly_wait(time_to_wait=10)
                    driver2.get(url=td[1].find_element_by_tag_name("a").get_attribute("href"))
                    time.sleep(1)

                    xpathDepartment = "/html/body/div/div[3]/div/div[2]/div[2]/dl/dd[3]"

                    department = driver2.find_element_by_xpath(xpathDepartment).text
                    department = department.split("(")[0]
                    title = td[1].find_element_by_tag_name("a").text
                    content = ""

                    # hwp 파일 txt로 불러와서 저장
                    try:
                        downList = driver2.find_elements_by_class_name("add_file")

                        for add_file in downList:
                            text = add_file.find_element_by_tag_name("a").get_attribute("onclick")
                            if ".hwp" in text:
                                result = re.split(r"['-']", text)
                                pFileName = result[1]
                                pRealName = result[3]
                                pPath = result[5]
                                downloadUrl = "https://www.mcst.go.kr/servlets/eduport/front/upload/UplDownloadFile?pFileName=" \
                                              + pFileName + "&pRealName=" + pRealName + "&pPath=" + pPath + "&pFlag="
                                download_hwp(downloadUrl)
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

                except Exception as e:
                    print(e)
                    print("데이터가 비었습니다.")

                driver2.close()

            if text_date < start_date:
                break
        driver.close()


def get_text_file():
    f = open(TEMP_DIR + TEMP_TXT_FILE, mode='r')
    return f.read()


def hwp_to_txt(path):
    # hwp_to_txt()에 넘겨줄 hwpDispatch 사용이 끝난 후 hwp.Quit() 선언 필수
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "AutomationModule")
    # hwp.SetMessageBoxMode(0x00000020)
    hwp.Open(path + TEMP_HW_FILE, "HWP", "forceopen:true")
    time.sleep(10)
    # hwp.SetMessageBoxMode(0x00010000)
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


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)


if __name__ == '__main__':
    main()