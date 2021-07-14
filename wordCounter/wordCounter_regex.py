# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import DataFrame
import re

from collections import Counter

def main():

    wordPath = "../data_file/FindMyWords.xlsx"
    name = ['date', 'department', 'title', 'content']  # 칼럼 이름
    contents = pd.read_csv('../ScrapData/post.csv', encoding='utf-8', header=0, parse_dates=['department'], names=name)

    data_info(contents)  # 불러온 csv파일의 정보 확인
    allDepartments = get_allDepartments(contents)  # 데이터의 모든 부서 조회(중복O)
    departments_unique = get_unique(allDepartments)  # 부서 중복 제거
    contents_Departments(len(contents), allDepartments, departments_unique)

    searchWord = load_searchWord(wordPath)

    num_department = dict((key, dict()) for key in departments_unique)

    for i in contents.index:
        print(i)
        department = contents._get_value(i, 'department')
        content = contents._get_value(i, 'content')

        for word in searchWord:
            listFind = re.findall(word, content)
            cntNum = len(listFind)

            if cntNum > 0:
                # print(department, " : ", word, " : ", str(len(listFind)))
                if num_department[department].get(word):
                    num_department[department][word] += cntNum
                    print(" Add countNum :", word)
                else:
                    num_department[department][word] = cntNum
                    print(" New word in department ")

    sort_length(num_department)
    deduplicate_word(num_department)
    view_count_department(num_department) # 부서 별 내림차순 정렬
    totalCount = count_total(num_department)
    print(totalCount)


def sort_length(dictList):
    for i in list(dictList):
        dictList[i] = dict(sorted(dictList[i].items(), key=lambda x: len(x[0]), reverse=True))


def view_count_department(dictList):
    for listUnique in list(dictList):
        # print(i, " : ", num_department[i])
        res = sorted(dictList[listUnique].items(), key=(lambda x:x[1]), reverse=True)
        print(listUnique, " : ", res)


def count_total(dictList : dict):
    totalCount = Counter()

    for listDict in dictList.values():
        totalCount = totalCount + Counter(listDict)

    return totalCount


# str.count() 중복 제거
def deduplicate_word(dictList : dict):

    for file in dictList:
        for i in dictList[file]:
            for j in dictList[file]:
                if i != j:
                    if i in j:
                        dictList[file][i] = dictList[file][i] - dictList[file][j]


def load_searchWord(file_path):
    df = pd.read_excel(file_path, sheet_name=0)  # can also name of sheet
    my_list = df['정규식'].tolist()

    return my_list


def contents_Departments(contents_length, allDepartments, departments_unique):
    zero = np.zeros((contents_length, len(departments_unique)))

    dummy = DataFrame(zero, columns=departments_unique)

    for n, g in enumerate(allDepartments):
        dummy.loc[n, g] = 1

    TDM = dummy.T

    pd.set_option('display.max_rows', None)

    departments_counter = TDM.sum(axis=1)
    print("departments_counter")
    print(departments_counter.sort_values(ascending=False))

    # plt.rcParams['axes.unicode_minus'] = False
    # plt.rc('font', family='New Gulim', size=5)
    # # 내림차순 정렬
    # departments_counter.sort_values().plot(kind='barh', title='Content department counter')
    # plt.show()


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



if __name__ == '__main__':
    main()