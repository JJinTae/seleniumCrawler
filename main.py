import selenium
from selenium import webdriver
# from selenium.webdriver import ActionChains

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support.ui import WebDriverWait



def main():
    URL = "https://www.mcst.go.kr/kor/s_notice/press/pressView.jsp?pSeq=17732"

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(time_to_wait=3) # 암묵적 대기 단위 초
    driver.get(url=URL)

    post_title = driver.find_element_by_class_name('view_title')
    post_date = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/dl/dd[1]')
    post_department = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/dl/dd[3]')
    post_content = driver.find_element_by_class_name('viewWarp')


    # 이전 페이지로 넘어가는 방법
    btn_prePage = driver.find_element_by_class_name('ico_arrow_top')
    btn_prePage.click()


    driver.close()



if __name__ == '__main__':
    main()