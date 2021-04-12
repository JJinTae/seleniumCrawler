import os
import time
from selenium import webdriver

DATA_DIR = 'ScrapData'
CSV_POST = os.path.join(DATA_DIR, 'localLaws.csv')

def main():
    URL = "http://www.elis.go.kr/newlaib/renew_laibLaws/h1126/laws_new.jsp?regionId=44000"
    get_list(url=URL)




def driver_option():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    # options.add_argument('headless')

    return options


def get_list(url):
    driver = webdriver.Chrome('chromedriver', options=driver_option())
    driver.implicitly_wait(time_to_wait=10)  # 암묵적 대기 단위 초
    driver.get(url=url)

    listHtml = []
    # postList = driver.find_element_by_css_selector("tbody").find_elements_by_tag_name("a")
    # postList = driver.find_element_by_css_selector("div.raw_sort")
    driver.switch_to.frame("lawsif")
    driver.switch_to.frame("left")
    driver.switch_to.frame("index2if")
    postList = driver.find_element_by_css_selector("div.raw_sort").find_elements_by_css_selector("ul.tree3")
    for i in postList:
        for html in i.find_elements_by_tag_name("a"):
            listHtml.append(html.get_attribute("html"))






    time.sleep(10)
    # return postList


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)

if __name__ == '__main__':
    main()