import time
from selenium import webdriver
import requests
import os
import csv

DATA_DIR = '../ScrapData'
CSV_POST = os.path.join(DATA_DIR, 'post.csv')

def main():

    URL = search_date(20200101, 20201231) # 수집할 보도자료 기간 ex) search_date(20200101, 20201231)
    list = get_list(URL)
    scrap_content(list)

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
                date = driver2.find_element_by_xpath(
                    "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[2]/td[1]").text
                department = driver2.find_element_by_xpath(
                    "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[6]/td[1]").text
                title = driver2.find_element_by_xpath(
                    "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[8]/td").text
                content = driver2.find_element_by_xpath(
                    "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[16]/td").text
                content = remove_whitespaces(content)
                # print("DATE : " + date + "\nDEPARTMENT : " + department + "\nTITLE : " + title + "\nCONTENT :" + content)
                row = [date, department, title, content]
                with open(CSV_POST, 'a', newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow(row)
            except:
                print("데이터가 비었습니다.")

        else:
            print("통과되었습니다.")
            flag = True



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

    menuQuery = "mnu_cd=CNNMENU02362"
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