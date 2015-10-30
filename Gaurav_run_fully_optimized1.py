import pandas as pd
import numpy as np
import math
import os
#import time


 ## will be the main file
 ## three dataframes
# dage = input("enter age csv name: ")
# dlab = input("enter lab time series csv: ")
# dvit = input("enter vitals time series csv: ")
#start = time.time()
"""
try:
	dage = pd.read_csv("id_age_test.csv")
	dlab = pd.read_csv("id_time_labs_test.csv")
 	dvit = pd.read_csv("id_time_vitals_test.csv")
except:
	print "verify filenames"
#TOT_READINGS = dage.AGE.count()
os.makedirs("lab_seperated_test")
os.makedirs("vitals_seperated_test")
os.makedirs("lab_processed_test")
os.makedirs("vitals_processed_test")

# #fill lab_data for separate patients
for i in range(4792,5990):
	dfi = dlab.loc[dlab["ID"]==(i+1)]
	dfi.to_csv('lab_seperated_test/' + str(i+1) + '.csv')
# #fill vitals_data for separate patients
for i in range(4792,5990):
    dfi = dvit.loc[dvit["ID"]==(i+1)]
    dfi.to_csv('vitals_seperated_test/' + str(i+1) + '.csv')

# #fill vitals_filled_data
span = 12 # more span, more smoothened
for i in range(4792,5990):
	dfi = pd.read_csv("vitals_seperated_test/%d.csv"%(i+1))
 	for j in range(1,7):
 		dfi["V%d"%j] = pd.ewma(dfi["V%d"%j],span = span)
 	dfi = dfi.fillna(dfi.median())
 	dfi.to_csv("vitals_processed_test/%d.csv"%(i+1))

#fill labs_filled_data
for i in range(4792,5990):
 	dfi = pd.read_csv("lab_seperated_test/%d.csv"%(i+1))
 	dfi = dfi.fillna(method="pad")
 	dfi = dfi.fillna(method="bfill")
 	dfi = dfi.fillna(0)
 	dfi.to_csv("lab_processed_test/%d.csv"%(i+1))

# del dlab
# del dvit

#mid = time.time()
#print "time to create folders: " + str(mid-start)
### [total_tests, no. of V1, ......, no. of V6], [no. of L1, ......, no. of L25],
### [Age], [time_diff_mean, time_diff_std], [V1,V2,V3,V4,V5,V6], [L1,L2,...,L25]
### [dvitcount, dlabcount, dagei, dtimediff, dnetvit, dnetlab]
"""
def main(tort, r1, r2):
	df = []
	for id in range(r1, r2):
		
		dviti = pd.read_csv("vitals_seperated_"+tort+"/%d.csv"%(id+1))
		dlabi = pd.read_csv("lab_seperated_"+tort+"/%d.csv"%(id+1))
		dvitpi = pd.read_csv("vitals_processed_"+tort+"/%d.csv"%(id+1))
		dlabpi = pd.read_csv("lab_processed_"+tort+"/%d.csv"%(id+1))
		
		'''
		dviti = dvit[dvit.ID==(id+1)]
		dlabi = dlab[dlab.ID==(id+1)]
		
		span = 12
		dvitpi= dviti
		for j in range(1,7):
			dvitpi["V%d"%j] = pd.ewma(dvitpi["V%d"%j],span = span)

		dvitpi = dvitpi.fillna(method = 'bfill')
		
		dlabpi= dlabi
 		dlabpi = dlabpi.fillna(method='ffill')
 		dlabpi = dlabpi.fillna(method = 'bfill')
 		dlabpi = dlabpi.fillna(0)
		'''
		timestamps = pd.np.array(dviti.TIME[dviti.ICU == 1])
		#dagei = dage.AGE[id+1]
		prev = np.zeros(63)
		for timestamp in timestamps:
			f1 = featurize(dviti, dlabi, dvitpi, dlabpi, prev, timestamp)
			#f = pd.np.array(f)
			#f= f.reshape(f.shape[0])
			df.append(f1)
			print f1
			prev = f1
			print "feature made for id: %d and timestamp: %d"%(id,timestamp)
			
	df = pd.DataFrame(df)
	return df
	df.to_csv("feature_final_"+tort+".csv")

def featurize(dviti, dlabi, dvitpi, dlabpi, prev, timestamp):
	#count of time and vitals
	## ith person, jth timestamp
	###dvitcount = []
	## count of vital tests
	## (total_tests, no. of V1, ......, no. of V6)		##f = 7
	if sum(prev)!= 0:
		### optimized
		features = np.zeros(63)
		'''#get number of all valid tests
		dvitcount = dviti_j.describe().iloc[0].values
		###dvitcount = np.array(dvitcount)
		#extract the conts for all vital tests and ICU's
		dvitcount = dvitcount[2:9] #numpy array'''

		dviti_j = dviti[dviti.TIME == timestamp]
		dvitcount = dviti_j.describe().iloc[0].values
		
		features[0:7] = prev[0:7] + dvitcount[2:9]
		#count of lab tests
		## ith person, jth timestamp

		## count of lab tests
		## (no. of L1, ......, no. of L25)	##f = 25
		dlabi_j = dlabi[dlabi.TIME == timestamp]
		dlabcount = dlabi_j.describe().iloc[0].values
		
		features[7:32] = prev[7:32] + dlabcount[3:]

		# time difference mean and std
		# dtimediff = [mean, std]	##f = 2
		# a vector representing accumulated value of vitals of patient i at time j
		# dnetvit = [V1,V2,V3,V4,V5,V6] ##f = 6

		alph = 0.25
		dvitpi_j = dvitpi[dvitpi.TIME == timestamp]

		dnetvit = dvitpi_j[[4,5,6,7,8,9]]
		dnetvit = pd.np.array(dnetvit)
		features[32:38] = alph*dnetvit + (1-alph)*prev[32:38]

		'''for i in range(len(dnetvit)-1):
			dnetvit[i+1] = alph*dnetvit[i+1] + (1-alph)*dnetvit[i]

		dnetvit = dnetvit[-1]

		dnetvit = pd.DataFrame(dnetvit)'''

		# a vector representing accumulated value of labs of patient i at time j
		# dnetlab = [L1,L2,...,L25]  ##f = 25

		dlabpi_j = dlabpi[dlabpi.TIME == timestamp]

		dnetlab = dlabpi_j[[x for x in range(4,29)]]
		dnetlab = pd.np.array(dnetlab)
		'''featuresor i in range(len(dnetlab)-1):
		dnetlab[i+1] = alph*dnetlab[i+1] + (1-alph)*dnetlab[i]'''

		features[38:63] = alph*dnetlab + (1-alph)*prev[38:63]
		'''dnetlab = dnetlab[-1]

		dnetlab = pd.DataFrame(dnetlab)

		features = pd.concat([dvitcount,dlabcount,dtimediff,dnetvit, dnetlab])'''
		#final
		return features
	
	else:
	## count of vital tests
	## (total_tests, no. of V1, ......, no. of V6)		##f = 7

		features = np.zeros(63)
		dviti_j = dviti[dviti.TIME <= timestamp]
		dvitcount = (dviti_j.describe().iloc[0].values)
		dvitcount = np.array(dvitcount)
		features[0:7] = dvitcount[2:9]
	#count of lab tests
	## ith person, jth timestamp


	## count of lab tests
	## (no. of L1, ......, no. of L25)	##f = 25
		dlabi_j = dlabi[dlabi.TIME<= timestamp]
		dlabcount = (dlabi_j.describe().iloc[0].values)
		dlabcount = np.array(dlabcount)
		features[7:32] = dlabcount[3:]

		# time difference mean and std
		# dtimediff = [mean, std]	##f = 2
	# a vector representing accumulated value of vitals of patient i at time j
	# dnetvit = [V1,V2,V3,V4,V5,V6] ##f = 6

		alph = 0.25
		dvitpi_j = dvitpi[dvitpi.TIME<= timestamp]

		dnetvit = dvitpi_j[[4,5,6,7,8,9]]
		dnetvit = pd.np.array(dnetvit)
		for i in range(len(dnetvit)-1):
			dnetvit[i+1] = alph*dnetvit[i+1] + (1-alph)*dnetvit[i]
	
		dnetvit = np.array(dnetvit[-1])

		features[32:38] = dnetvit
	# a vector representing accumulated value of labs of patient i at time j
	# dnetlab = [L1,L2,...,L25]  ##f = 25
		alph = 0.25


		dlabpi_j = dlabpi[dlabpi.TIME<= timestamp]

		dnetlab = dlabpi_j[[x for x in range(4,29)]]
		dnetlab = pd.np.array(dnetlab)
		for i in range(len(dnetlab)-1):
			dnetlab[i+1] = alph*dnetlab[i+1] + (1-alph)*dnetlab[i]
	
		dnetlab = np.array(dnetlab[-1])

		features[38:63] = dnetlab

		return features




if __name__ == "__main__":
	main()
