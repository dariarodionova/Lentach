import pyprind
import numpy as np
import pandas as pd
from pandas import read_csv
import re
import regex
from matplotlib import pyplot as plt
from difflib import SequenceMatcher


def Process(text):
    text = re.sub(r'([А-Я])', lambda pat: pat.group(1).lower(), text)  # Inline
    text = re.sub(r",", '', text)
    text = re.sub(r"\bна\b", '', text)
    text = re.sub(r"\d", '', text)
    text = regex.sub(r"\P{IsCyrillic}", ' ', text)
    # array[1, 0] = re.sub(r"http://.*/.*\b",'',array[1, 0])
    text = regex.sub(r"\b[а-яА-Я]\b", ' ', text)
    text = regex.sub(
        r"(\bп..\b|\bпо\b|\bкотор..\b|\bкотор..\b|\b..\b|\bмлрд\b|\bгод.?\b|\bравно\b|\bтеперь\b|\bНов...?\b|\bнов...?\b|\bэт..?.?\b|\bпосле\b|\bкотор...?\b|"
        r"\bч?Ч?то\b|\bн?их\b|\bне..?\b"
        r"|\bдаже\b|\bвот\b|\bедва\b|\bначал\b|\bКак\b|\bвам.\b|\bтот\b|\bт.\b|\bкак..\b|\bещеb|\bт.же\b|\b...\b|\bдругие\b|\bчасу\b|\bновости\b|\bесть\b|\bчтобы\b|\bод..\b"
        r"|\bбыло\b|\bкогда\b|\bтаки\b|\bсебя\b|\меня\b|\bболее\b|\bодного\b|\bпока\b|\bсейчас\b|\bбуд.т\b|\bлишь\b|\bочень\b|\bчего\b|\bбыл.?\b|\bnтого\b|\bсегодня\b|\bесли\b|\bтого\b|\bбыть\b)",
        ' ', text)
    text = regex.sub(r"автомобил.?.?.?.?.?.?", "автомобиль ", text)
    text = regex.sub(r"яхт..?.?", "яхта ", text)
    wordArray = np.array(re.findall(r'(?u)\w+', text), dtype=object).flatten()
    return wordArray


# --------Import raw data
RawData = np.array(read_csv("Lentach_data2.csv", dtype=object).values)
#RawData = RawData[0:int(RawData.size / 10)]
print(RawData.shape)


# --------Remove empty cells
RawData = RawData[~pd.isnull(RawData[:, 0])]
print(RawData.shape)


# --------Get number of examples and get likes
m = RawData.shape[0]

# --------Remove prepositions and empty entries
keep = np.ones((m), dtype=bool)
for i in range( m):
    processed = Process(RawData[i, 0])
    if processed.shape[0] != 0 or processed.shape[0] != 1:
        if processed.size != 0:
            RawData[i, 0] = processed
        else:
            keep[i] = False
    else:
        keep[i] = False

RawData = RawData[keep, :]
m = RawData.shape[0]
print(RawData.shape)

'''
# -------Create list of all words
wordList = np.empty((1, 1), dtype=object)
bar = pyprind.ProgBar(m, monitor=True, title=" Progress:")

for i in range(0, m):
    for j in range(0, RawData[i, 0].shape[0]):
        wordList = np.append(wordList, RawData[i, 0][j])
    bar.update()
print("\n", bar)
wordList = wordList[1:]
print(wordList)

# --------Leave only unique words
UniqueWordList = np.unique(wordList)
m = UniqueWordList.shape[0]

# --------Save to file
data = pd.DataFrame(UniqueWordList)
data.to_csv("data/UniqueWordsList.csv", encoding='UTF-8')


# --------Calculate likeness
bar2 = pyprind.ProgBar(m, monitor=True, title="Counting likeness:")

likenessMatrix = np.zeros((UniqueWordList.shape[0], UniqueWordList.shape[0]))
for i in range(0, m):
    for j in range(0, m):
        likeness = round(SequenceMatcher(lambda x: x == "", UniqueWordList[i], UniqueWordList[j]).ratio(),1)
        if likeness != 0:
            likenessMatrix[i, j] = likeness
    bar2.update()

print(bar2)
print(likenessMatrix)
np.savetxt("data/likeness.csv", likenessMatrix, fmt='%1.1f')
'''

#--------load likenessMatrix
print("\nLoading data on likeness...")
likenessMatrix = pd.read_csv("data/likeness.csv",dtype=np.float, delimiter=" ", header=None).values
print(likenessMatrix)

print("\nLoading data on words...")
UniqueWordsList = pd.read_csv("data/UniqueWordsList.csv").values[:, 1]
m = UniqueWordsList.shape[0]
print(UniqueWordsList)


#--------Group by likeness
print("\nStart grouping by likeness...")

groupBar = pyprind.ProgBar(m, monitor=True)
groups = np.empty((m,30), dtype=object)
print("Groups shape: ", groups.shape)

for i in range(likenessMatrix.shape[0]):
    line = UniqueWordsList[likenessMatrix[i, :] > 0.8]
    for j in range(line.shape[0]):
        groups[i,j] = line[j]
    groupBar.update()

print(groupBar)

groupsFull = pd.DataFrame(groups)
groupsFull.to_csv("data/groupsFull.csv", encoding='UTF-8')

groups = groups[:,0]
groups = np.unique(groups)


#-------Create group value list
numofGroups = groups.shape[0]
valueList = np.zeros((groups.shape[0],1))
mentionsList = np.zeros((groups.shape[0],1))

#-------Calculate value for every group
print("\nStart calculating group values...")
m = RawData.shape[0]

for i in range(numofGroups):
    for j in range(m):
        if np.any(groups[i]==RawData[j,0]):
            #print(groups[i,0], " match at: ", j)
            valueList[i] += float(RawData[j,1])
            mentionsList[i] +=1

groupsWithValue = np.column_stack((groups[:],valueList,mentionsList))

print(groups[:50])
print(groupsWithValue[:50])
sortedValuedGroups = groupsWithValue[groupsWithValue[:,1].argsort()]

data = pd.DataFrame(sortedValuedGroups)
data.to_csv("data/results.csv", sep=",", encoding='UTF-8')