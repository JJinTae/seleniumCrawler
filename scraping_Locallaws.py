import csv
import os
import time
from selenium import webdriver

DATA_DIR = 'ScrapData'
CSV_POST = os.path.join(DATA_DIR, 'localLaws.csv')

def main():
    # listURL 해당지역 자치법규 목록 검색구분
    listURL = "http://www.elis.go.kr/newlaib/renew_laibLaws/h1126/print_index_new.jsp?region=44000&gubun=2"
    homeURL = "http://www.elis.go.kr/newlaib/renew_laibLaws/h1126/laws_new.jsp?regionId=44000"

    cols = ['index', 'department', 'title', 'content']

    if not os.path.exists(CSV_POST):
        with open(CSV_POST, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(cols)

    get_list(listURL, homeURL)



def get_list(listURL, homeURL):
    driver = webdriver.Chrome('chromedriver', options=driver_option())
    driver.implicitly_wait(time_to_wait=10)  # 암묵적 대기 단위 초
    driver.get(url=listURL)

    driver2 = webdriver.Chrome('chromedriver', options=driver_option())
    driver2.implicitly_wait(time_to_wait=10)
    driver2.get(url=homeURL)
    driver2.switch_to.frame("lawsif")

    index = 1
    linkList = driver.find_element_by_css_selector("tbody").find_elements_by_class_name("title")

    for i in linkList:
        link = i.find_element_by_tag_name("a").get_attribute("href").replace("javascript:goViewlaws", "goLaws")
        print(index) # index
        print(i.find_element_by_xpath("following-sibling::td").text) # department
        print(i.text)  # title
        print(i.find_element_by_tag_name("a").get_attribute("href").replace("javascript:goViewlaws", "goLaws")) # link
        print(remove_whitespaces(get_content(driver2, link)))  # content

        department = i.find_element_by_xpath("following-sibling::td").text
        title = i.text
        content = remove_whitespaces(get_content(driver2, link))

        row = [index, department, title, content]
        with open(CSV_POST, 'a', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(row)

        index = index + 1



def get_content(driver, link):

    driver.switch_to.frame("left")
    driver.switch_to.frame("index2if")
    driver.execute_script(link)
    time.sleep(1)
    driver.switch_to.parent_frame()
    driver.switch_to.parent_frame()
    driver.switch_to.frame("right")
    content = driver.find_element_by_class_name("rightview").text
    driver.switch_to.parent_frame()

    return content



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