from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


data = pd.read_csv("data/results.csv").values
print(data.shape)
data = data[:,1:]
ranges=(27000,22000,19000,15000,10000,5000,2000,1000)

data[:, 1] = data[:, 1]/data[:, 2]
data[:, 1] = np.around(data[:, 1].astype(np.float))

data = data[:,:2]
data = data[data[:,1].argsort()]

n=6

groups = [[] for _ in range(8)]

for i in range (data.shape[0]):
    if data[i, 1] >= ranges[0] and len(groups[0])<n:
        groups[0].append(data[i, 0])
    if ranges[1] <= data[i, 1] < ranges[0] and len(groups[1])<n:
        groups[1].append(data[i, 0])
    if ranges[2] <= data[i, 1] < ranges[1] and len(groups[2])<n:
        groups[2].append(data[i, 0])
    if ranges[3] <= data[i, 1] < ranges[2] and len(groups[3])<n:
        groups[3].append(data[i, 0])
    if ranges[4] <= data[i, 1] < ranges[3] and len(groups[4])<n:
        groups[4].append(data[i, 0])
    if ranges[5] <= data[i, 1] < ranges[4] and len(groups[5])<n:
        groups[5].append(data[i, 0])
    if ranges[6] <= data[i,1] < ranges[5] and len(groups[6])<n:
        groups[6].append(data[i, 0])
    if data[i,1] <ranges[6] and len(groups[7])<n:
        groups[7].append(data[i, 0])

amounts = []
for i in range (len(groups)):
    amounts.append((np.size(groups[i])))

for i, group in enumerate(groups):
    groups[i] = group[:5]

y = ranges

for i, group in enumerate(groups):
    groups[i] = sorted(group)

x = np.linspace(0,100, num=np.size(amounts))

fig = plt.figure()
plt1 = fig.add_subplot(111)
for i in range(8):
    plt1.text(x[i],y[i],"\n".join(groups[i]), size = 10, horizontalalignment = 'center', verticalalignment = 'center')
area = np.multiply(y,1.5)

plt1.scatter(x,y,s = area, c = -x, alpha=0.8)
plt1.axes.set_xlim(-15,110)
plt1.axes.set_ylim(-10000,45000)

plt.show()
