import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import time

from konlpy.tag import Okt
from collections import Counter


def main():
    wordPath = "data_file/SearchWords.xlsx"
    name = ['date', 'department', 'title', 'content'] # 칼럼 이름
    contents = pd.read_csv('ScrapData/post.csv', header=0, parse_dates=['department'], names=name)

    data_info(contents) # 불러온 csv파일의 정보 확인
    allDepartments = get_allDepartments(contents) # 데이터의 모든 부서 조회(중복O)
    departments_unique = get_unique(allDepartments) # 부서 중복 제거
    contents_Departments(len(contents), allDepartments, departments_unique)


    # 여기부터
    searchWord = load_searchWord(wordPath)

    # num_department = dict.fromkeys(departments_unique, dict()) # dic 리스트
    num_department = dict((key, dict()) for key in departments_unique)

    for i in contents.index:
        print(i)
        department = contents._get_value(i, 'department')
        content = contents._get_value(i, 'content')

        for word in searchWord:
            cntNum = content.count(word)
            if cntNum > 0:
                print(department, " : ", word, " : ", str(cntNum))
                if num_department[department].get(word):
                    num_department[department][word] += cntNum
                    print(" Add countNum :", word)
                else:
                    num_department[department][word] = cntNum
                    print(" New word in department ")

    for i in list(departments_unique):
        # print(i, " : ", num_department[i])
        res = sorted(num_department[i].items(), key=(lambda x:x[1]), reverse=True)
        print(i, " : ", res)





def load_searchWord(file_path):
    df = pd.read_excel(file_path, sheet_name=0)  # can also name of sheet
    my_list = df['단어/용어'].tolist()

    return my_list


def contents_Departments(contents_length, allDepartments, departments_unique):
    zero = np.zeros((contents_length, len(departments_unique)))

    dummy = DataFrame(zero, columns=departments_unique)

    for n, g in enumerate(allDepartments):
        dummy.loc[n, g] = 1

    TDM = dummy.T
    # print(dummy)
    # print(TDM)

    pd.set_option('display.max_rows', None)

    departments_counter = TDM.sum(axis=1)
    print("departments_counter")
    print(departments_counter.sort_values(ascending=False))

    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('font', family='New Gulim', size=5)

    # 내림차순 정렬
    departments_counter.sort_values().plot(kind='barh', title='Content department counter')

    plt.show()


def get_unique(departments):
    departments_unique = pd.unique(departments)

    print("부서 수(중복X) : ", len(departments_unique))
    print(departments_unique)

    return departments_unique


def get_allDepartments(contents):
    departments = []
    for i in contents.index:
        # departments.append(contents.loc[i, 'department'])
        val = contents._get_value(i, 'department')
        departments.append(val)

    print("부서 수 확인용(중복O) : ", len(departments))

    return departments


def data_info(contents):
    print(contents.info())
    print(contents.head())
    print("전체 글 수 : ", len(contents))


# COUNTER
"""

# xlrd 1.2.0 패키지 설치 필수
def load_searchWord():

    df = pd.read_excel("./data_file/SearchWords.xlsx", sheet_name=0)  # can also name of sheet
    my_list = df['단어/용어'].tolist()

    return my_list

f = open("./data_file/testFile.txt", mode='r', encoding='UTF8')
text = f.read()
print(text)

print(load_searchWord())



for i in load_searchWord():
    cntNum = text.count(i)
    if cntNum > 0:
        print(i + " : " + str(cntNum))
        
"""

if __name__ == '__main__':
    main()