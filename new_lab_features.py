import pandas as pd
import numpy as np

def main():
	df = []
	print 'in main'
	for id in range(3594):
		print id+1
		dlabi = pd.read_csv("./lab_seperated_train/%d.csv"%(id+1))
		dvitpi = pd.read_csv("./vitals_seperated_train/%d.csv"%(id+1))
		timestamps = pd.np.array(dvitpi.TIME[dvitpi.ICU == 1])
		for timestamp in timestamps:
			try:
				f1 = featurize(dlabi, dvitpi, timestamp)
				df.append(f1)
			except:
				f1 = np.zeros(31)
			print "feature made for id: %d and timestamp: %d"%(id+1,timestamp)

		print "***********************feature made for id: %d *********************************"%(id+1)

	df = pd.DataFrame(df)
	df.to_csv("lab_std_new.csv")

def featurize(dlabi, dvitpi, timestamp):
	features = np.zeros(31)
	
	#count of all lab tests
	dlabstd = dlabi[dlabi['TIME'] <= timestamp].std().values
	dvitstd = dvitpi[dvitpi['TIME'] <= timestamp].std().values
	features[0:25] = dlabstd
	features[25:31] = dvitstd
	return features


if __name__ == "__main__":
	main()
