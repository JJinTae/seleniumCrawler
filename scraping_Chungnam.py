import time
import selenium
from selenium import webdriver



def main():
    URL = "http://www.chungnam.go.kr/cnnet/board.do?"

    menuQuery = "mnu_cd=CNNMENU02362"
    pageQuery = "&pageNo=1"
    showQuery = "&showSplitNo=10"
    strdateQuery = "&srtdate=20200101"
    enddateQuery = "&enddate=20201231"

    URL = URL + menuQuery + pageQuery + showQuery + strdateQuery + enddateQuery
    print(URL)

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(time_to_wait=5) # 암묵적 대기 단위 초
    driver.get(url=URL)



if __name__ == '__main__':
    main()