import time
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import csv


def main():
    URL = search_date(20200101, 20201231) # 수집할 보도자료 기간 ex) search_date(20200101, 20201231)
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

    count = 0
    flag = False

    for post in list:
        if(flag):
            print("들어왔습니다.")
            count += 1
            flag = False
            print(count)
            #print(i.get_attribute("href"))
            driver2.get(url=post.get_attribute("href"))
            time.sleep(1)
            date = driver2.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[2]/td[1]").text
            department = driver2.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[6]/td[1]").text
            title = driver2.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[8]/td").text
            content = driver2.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/div[1]/table/tbody/tr[16]/td").text
            content = remove_whitespaces(content)
            #print("DATE : " + date + "\nDEPARTMENT : " + department + "\nTITLE : " + title + "\nCONTENT :" + content)
        else:
            print("통과되었습니다.")
            flag = True



def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')

    return options

def get_list(url):
    driver = webdriver.Chrome('chromedriver', options=driver_option())
    driver.implicitly_wait(time_to_wait=5)  # 암묵적 대기 단위 초
    driver.get(url=url)

    list = driver.find_element_by_css_selector("tbody").find_elements_by_tag_name("a")
    print(len(list))

    return list

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