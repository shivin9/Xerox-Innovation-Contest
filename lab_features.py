import pandas as pd
import os
import numpy as np
import matplotlib.pyplot
print 'reading lab records...'
labs = pd.read_csv('../data/id_time_labs_train.csv')
print 'reading vitals records...'
vitals = pd.read_csv('../data/id_time_vitals_train.csv')
vitals = vitals[['ID','TIME','ICU']]
vitals_icu = vitals[vitals['ICU'] == 1]
count = 0
os.chdir('../data/vectors')
time = []

for id in range(3594):
    id = id+1
    vid = vitals_icu[vitals_icu['ID'] == id]
    print len(vid)
    time.append(vid['TIME'].irow(len(vid) - 1) - vid['TIME'].irow(0))
    lid = labs[labs['ID'] == id]
    test = vid.index.values
    test = [test[i] - count for i in range(len(test))]
    count = count + len(vitals[vitals['ID'] == id])
    vec = lid.irow(test).notnull().sum()
    vec = np.array(vec)
    vec = vec.astype(int)

    print vec
    print 'writing file' + str(id)
    np.savetxt("vector%d"%(id), vec)

time = np.array(time)
np.savetxt("time", time)
