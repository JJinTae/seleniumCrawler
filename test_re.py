import os
import re

def main():
    # PATH = "./data_Text/*"
    PATH = "./data_Text/"
    wordPATH = "data_file/SearchWords.xlsx"

    text = open(PATH+"text4.txt", 'rt', encoding='utf8').read()
    print("------본문------\n", text, "\n---------------")

    listFind = re.findall('\d+\s매|\d+매', text)
    print(listFind)
    print("검색 수: ", len(listFind))



if __name__ == '__main__':
    main()