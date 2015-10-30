import pandas as pd
import numpy as np

import dynamic_features as dynft
import Gaurav_run_fully_optimized1 as hdk
import new_lab_features as nwlft
import fix_labs as fixlb
import dora

def main():
	print 'starting XRCI challenge...'
	#clip the values of lab results of training and testing data
	#fixlb.fixlab('../data/id_time_labs_train.csv')
	#fixlb.fixlab('../data/id_time_labs_test.csv')

	#separaring and filling NA values in vitals and labs of testing and training data
	#dynft.sep_fill('train')
	#dynft.sep_fill('test')

	#creating 1st set features for training data
	feat_tr = dynft.main('train', 0, 3594)

	#creating 2nd set of features for training data
	feat2_tr = hdk.main('test', 4793, 5990)

	#creating 1st set features for testing data
	feat_te = dynft.main('test', 0, 3594)

	#creating 2nd set of features for testing data
	feat2_tr = hdk.main('test', 4793, 5990)
	
	## append the 2 features files in excel to form the final set of features
	##remove any extra rows and columns from the above generated files using excel and name them as directed in the README file :)

	#training the classifier
	import Classifier_Model as model

	#the output file created by the above script needs to be clipped manually using excel to retain the required columns 

if __name__ == "__main__":
	main()
