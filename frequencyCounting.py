# -*- coding: utf-8 -*-

import pandas as pd
from collections import Counter

from konlpy.tag import Okt
from konlpy.tag import Komoran

def main():

    STOPWORDS_TXT = open('data_file/stopwords.txt', 'r', encoding='utf-8')
    stopwords = STOPWORDS_TXT.readlines()
    for i in range(len(stopwords)):
        stopwords[i] = stopwords[i].strip()

    df = pd.read_csv('ScrapData/post.csv')  # can also name of sheet
    content = ''.join(df['content'])

    nlpy = Okt()
    nouns = nlpy.nouns(content)

    count = Counter(nouns)

    tag_count = []
    tags = []

    for n, c in count.most_common(1000):
        dics = {'tag' : n, 'count':c}
        if len(dics['tag']) >=2 and len(tags) <= 30:
            if n not in stopwords:
                tag_count.append(dics)
                tags.append(dics['tag'])

    for tag in tag_count:
        print(" {:<14}".format(tag['tag']), end='\t')
        print("{}".format(tag['count']))

if __name__ == '__main__':
    main()