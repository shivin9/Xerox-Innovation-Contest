# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 05:57:08 2015
For: Xerox Innovation Contest
Author: Gaurav_Shrivastava and Hardik_Malhotra
"""

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import math
import os

def sine(x, amp, freq, base):
	return base + amp*np.sin(freq*x)

def sep_fill(tort):
	## will be the main file
	## three dataframes
	print 'reading vitals...'
	
	dvit = pd.read_csv('../data/id_time_vitals_'+tort+'.csv')
	dage = pd.read_csv('../data/id_age_'+tort+'.csv')

	TOT_READINGS = dage.AGE.count()
	print 'making folders for ' + tort
	os.makedirs("lab_seperated_"+tort)
	os.makedirs("vitals_seperated_"+tort)
	os.makedirs("lab_processed_"+tort)
	os.makedirs("vitals_processed_"+tort)

	#fill vitals_data for separate patients
	print 'filling vitals data for patients'
	for i in range(TOT_READINGS):
	    dfi = dvit.loc[dvit["ID"]==(i+1)]
	    dfi.to_csv('vitals_seperated_'+tort+'/' + str(i+1) + '.csv')

	#fill vitals_filled_data
	span = 20 # more span, more smoothened
	print 'fillingna for vitals data for patients'
	for i in range(TOT_READINGS):
		dfi = pd.read_csv("vitals_seperated_"+tort+"/%d.csv"%(i+1))
		dfi = dfi.fillna(method = 'ffill')
		dfi = dfi.fillna(0)
		for j in range(1,7):
			dfi["V%d"%j] = pd.ewma(dfi["V%d"%j],span = span)
		dfi.to_csv("vitals_processed_"+tort+"/%d.csv"%(i+1))

	del dvit

	#now reading lab data
	dlab = pd.read_csv('id_time_labs_'+tort+'.csv')

	#fill lab_data for separate patients
	print 'seperating lab data for patients'
	for i in range(TOT_READINGS):
		dfi = dlab.loc[dlab["ID"]==(i+1)]
		dfi.to_csv('lab_seperated_'+tort+'/' + str(i+1) + '.csv')

	#no need to fill labs_filled_data
	for i in range(TOT_READINGS):
	 	dfi = pd.read_csv("lab_seperated_"+tort+"/%d.csv"%(i+1))
	 	dfi = dfi.fillna(method="pad")
	 	dfi = dfi.fillna(dfi.median())
	 	dfi = dfi.fillna(0)
	 	dfi.to_csv("lab_processed_"+tort+"/%d.csv"%(i+1))

	del dlab

def main(tort, r1, r2):
	df = []
	print 'in main'	
	dage = pd.read_csv('id_age_'+tort+'.csv')
	for id in range(3594):
		print id+1
		dlabi = pd.read_csv("lab_seperated_"+tort+"/%d.csv"%(id+1))
		dvitpi = pd.read_csv("vitals_processed_"+tort+"/%d.csv"%(id+1))

		dagei = dage.AGE[id]
		## past => labcnt, dviti_time dataframe, diff array
		dvitip = pd.DataFrame()
		past = [0, dvitip]
		timestamps = pd.np.array(dvitpi.TIME[dvitpi.ICU == 1])
		diff = np.array([0])
		dvitpi['V7'] = dvitpi['V1'] - dvitpi['V2']

		#cols = dvitpi.columns.tolist()
		#cols.sort()
		#dvitpi = dvitpi[cols]

		for timestamp in timestamps:
			try:
				f1, past, diff = featurize(dlabi, dvitpi, dagei, past, diff, timestamp)
				df.append(f1)
			except:
				f1 = np.zeros(40)
			#print "feature made for id: %d and timestamp: %d"%(id+1,timestamp)

		print "***************************feature made for id: %d ***************************"%(id+1)

	df = pd.DataFrame(df)
	return df
	df.to_csv("40_feature_final.csv")

def featurize(dlabi, dvitpi, dagei, past, diff, timestamp):
	features = np.zeros(40)

	## append new values to the dvitpi dataframe
	new = dvitpi[dvitpi['TIME'] == timestamp]
	dvitpi = past[1].append(new)
	curr = len(dvitpi)
	past[1] = dvitpi

	#count of all lab tests
	dlabcount = dlabi[dlabi['TIME'] == timestamp].describe().iloc[0].values
	features[0] = sum(dlabcount[3:]) + past[0]
	past[0] = features[0]

	# time difference mean and std
	if(curr > 1):
		diff = np.append(diff, [dvitpi.irow(curr-1).TIME - dvitpi.irow(curr - 2).TIME])

	features[1] = diff.std()

	##fit the diff in a sine curve
	x = [i for i in range(len(dvitpi))]
	x = np.array(x)
	'''print 'popt '
	print popt
	print 'cov'
	print pcov'''

	try:
		popt, pcov = curve_fit(sine, x, diff, maxfev=5000)
	except:
		popt = np.array([0, 0, 0])

	features[2:5] = popt

	##cubic curve for all vitals
	x = [i for i in range(len(dvitpi))]
	x = np.array(x)

	y = dvitpi[['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7']]
	try:
		coeff = np.polyfit(x, y, 3)
		coeff = coeff.T
	except:
		coeff = np.zeros(28)

	features[5:33] = coeff.ravel()

	#age of patient
	features[33:39] = new[[4, 5, 6, 7, 8, 9]]
	features[39] = dagei
	return features, past, diff


if __name__ == "__main__":
	main()
