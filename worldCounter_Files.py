from collections import Counter

import pandas as pd
import os


def main():
    # PATH = "./data_Text/*"
    PATH = "./data_Text/"
    wordPATH = "data_file/SearchWords.xlsx"

    list_file = dict((key, dict()) for key in os.listdir(PATH))
    searchWord = load_searchWord(wordPATH)

    print(list_file)

    for file_path in list_file.keys():
        text = open(PATH+file_path, 'rt', encoding='utf8').read()

        for word in searchWord:
            cntNum = text.count(word)

            if cntNum > 0:
                if list_file[file_path].get(word):
                    list_file[file_path][word] += cntNum
                    print(" Add countNum :", word, " : ", cntNum)
                else:
                    list_file[file_path][word] = cntNum
                    print(" New word in department : ", word, " : ", cntNum)

    for i in list(list_file):
        # print(i, " : ", num_department[i])
        res = sorted(list_file[i].items(), key=(lambda x: x[1]), reverse=True)
        print(i, " : ", res)

    count_all(list_file)

def count_all(dictList : dict):

    totalCount = Counter()

    for listDict in dictList.values():
        totalCount = totalCount + Counter(listDict)

    print(totalCount)


def load_searchWord(file_path):
    df = pd.read_excel(file_path, sheet_name=0)  # can also name of sheet
    my_list = df['단어/용어'].tolist()

    return my_list


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)



if __name__ == '__main__':
    main()