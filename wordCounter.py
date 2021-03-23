import pandas as pd

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