import pandas as pd

def fixlab(filename):
	print 'fixing lab ' + filename	
	labs = pd.read_csv(filename)

	labs['L1'].loc[labs['L1'] > 8] = 8
	labs['L1'].loc[labs['L1'] < 6] = 6

	labs['L2'].loc[labs['L2'] > 50] = 50
	labs['L2'].loc[labs['L2'] < 30] = 30

	labs['L3'].loc[labs['L3'] > 200] = 200
	labs['L3'].loc[labs['L3'] < 30] = 30

	labs['L4'].loc[labs['L4'] > 180] = 180
	labs['L4'].loc[labs['L4'] < 125] = 125

	labs['L5'].loc[labs['L5'] > 8] = 8
	labs['L5'].loc[labs['L5'] < 3] = 3

	labs['L6'].loc[labs['L6'] > 50] = 50
	labs['L6'].loc[labs['L6'] < 22] = 22

	labs['L7'].loc[labs['L7'] > 50] = 50
	labs['L7'].loc[labs['L7'] < 4] = 4

	labs['L8'].loc[labs['L8'] > 3] = 3
	labs['L8'].loc[labs['L8'] < 0.35] = 0.35

	labs['L9'].loc[labs['L9'] > 50] = 50
	labs['L9'].loc[labs['L9'] < 0.35] = 0.35

	##L10 is all right

	labs['L11'].loc[labs['L11'] > 650] = 650
	labs['L11'].loc[labs['L11'] < 150] = 150

	labs['L12'].loc[labs['L12'] > 5] = 5
	labs['L12'].loc[labs['L12'] < 0.3] = 0.3

	labs['L13'].loc[labs['L13'] > 2000] = 2000
	labs['L13'].loc[labs['L13'] < 800] = 800

	labs['L14'].loc[labs['L14'] > 190] = 190
	labs['L14'].loc[labs['L14'] < 50] = 50

	labs['L15'].loc[labs['L15'] > 2.2] = 2.2
	labs['L15'].loc[labs['L15'] < 0.5] = 0.5

	labs['L16'].loc[labs['L16'] > 1] = 1
	labs['L16'].loc[labs['L16'] < 0.01] = 0.01

	labs['L17'].loc[labs['L17'] > 1] = 1
	labs['L17'].loc[labs['L17'] < 0.01] = 0.01

	labs['L18'].loc[labs['L18'] > 300] = 300
	labs['L18'].loc[labs['L18'] < 125] = 125

	labs['L19'].loc[labs['L19'] > 200] = 200
	labs['L19'].loc[labs['L19'] < 70] = 70

	labs['L20'].loc[labs['L20'] > 85] = 85
	labs['L20'].loc[labs['L20'] < 10] = 10

	labs['L21'].loc[labs['L21'] > 5.4] = 5.4
	labs['L21'].loc[labs['L21'] < 3.4] = 3.4

	labs['L22'].loc[labs['L22'] > 350] = 350
	labs['L22'].loc[labs['L22'] < 44] = 44

	labs['L23'].loc[labs['L23'] > 80] = 80
	labs['L23'].loc[labs['L23'] < 35] = 35

	labs['L24'].loc[labs['L24'] > 200] = 200
	labs['L24'].loc[labs['L24'] < 70] = 70

	labs['L25'].loc[labs['L25'] > 4] = 4
	labs['L25'].loc[labs['L25'] < 1] = 1

	labs.to_csv(filename)


