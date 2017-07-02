import numpy as np
import pandas
from pandas import read_csv
import re
import regex
text = read_csv("Lentach_data.csv", dtype = object)
import pyprind
import psutil

import collections


array = np.array(text.values)
array = array[~pandas.isnull(array[:,0])]
m = int(array.shape[0])

lines = np.chararray((1,300))

def Process(test):
    test = re.sub(r'([А-Я])', lambda pat: pat.group(1).lower(), test) # Inline
    test = re.sub(r",",'',test)
    test = re.sub(r"\bна\b",'',test)
    test = re.sub(r"\d",'',test)
    test = regex.sub(r"\P{IsCyrillic}",' ',test)
    #array[1, 0] = re.sub(r"http://.*/.*\b",'',array[1, 0])
    test = regex.sub(r"\b[а-яА-Я]\b",' ',test)
    test = regex.sub(r"(\bп..\b|\bпо\b|\bкотор..\b|\bкотор..\b|\b..\b|\bмлрд\b|\bгод.?\b|\bравно\b|\bтеперь\b|\bНов...?\b|\bнов...?\b|\bэт..?.?\b|\bпосле\b|\bкотор...?\b|"
                 r"\bч?Ч?то\b|\bн?их\b|\bне..?\b"
                 r"|\bдаже\b|\bвот\b|\bедва\b|\bначал\b|\bКак\b|\bвам.\b|\bтот\b|\bт.\b|\bкак..\b|\bещеb|\bт.же\b|\b...\b|\bдругие\b|\bчасу\b|\bновости\b|\bесть\b|\bчтобы\b|\bод..\b"
                     r"|\bбыло\b|\bкогда\b|\bпока\b|\bсейчас\b|\bбуд.т\b|\bлишь\b|\bочень\b|\bчего\b|\bбыл.?\b|\bnтого\b|\bсегодня\b|\bесли\b|\bтого\b|\bбыть\b)",' ',test)
    test = regex.sub(r"автомобил.?.?.?.?.?.?", "автомобиль ", test)
    test = regex.sub(r"яхт..?.?", "яхта ", test)
    wordArray = np.array(re.findall(r'(?u)\w+', test), dtype=object).flatten()
    return wordArray


comments = array[:,0].copy()

wordList = np.empty((1,1), dtype=object)

bar = pyprind.ProgBar(m, monitor=True)



for j in range(0,m):
    resultLine = Process(comments[j])
    for i in range (0,resultLine.shape[0]):
        wordList = np.append(wordList,resultLine[i])
    bar.update()


print(wordList.size)
wordList = np.delete(wordList, 0)
wordListUnique = np.unique(wordList)


unique, counts = np.unique(wordList, return_counts=True)
counts =np.array(counts)
unique = np.array(unique)
new = np.column_stack((unique,counts))

new = pandas.DataFrame(new)
new.to_csv("data/AllWordsCount.txt", encoding='UTF-8')
#print(wordListUnique.size)
dF = pandas.DataFrame(wordListUnique)
dF.to_csv("data/UniqueWords.txt", encoding='UTF-8')