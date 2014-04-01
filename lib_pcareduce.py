import numpy as np
import csv as csv
from matplotlib.mlab import PCA

def lib_pca_file(filename):
	"""
	performs a PCA reduction on a matrix of data using SVD techniques 

	preprocessing
	"""
	
	data = np.genfromtxt(filename,dtype=str, delimiter=',')
	data = data.T

	#delete first column of string labels
	data = np.delete(data, 0, 0)
	labels = data[:,0]
	data = np.delete(data, 0, 1) 
	data = data.astype(float)
	data = data.T

	"""
	main anaylysis
	"""
	pca = PCA(data)
	singular_values = pca.fracs
	singular_values =  singular_values.T
	print "Singular Values" + str(singular_values)
	# singular_values = np.column_stack(["singular_values", singular_values]) 
	lib_data = pca.Y
	truncated_v = pca.Wt.T

	f_name = filename.split("/")	
	name = filename.split(".")[0].split("/")[len(f_name)-1] + "_vectors.csv"
	# white_space = np.linspace(0, len)
	data = np.column_stack((labels, truncated_v))
	# data = np.column_stack((data.T, singular_values))


	output_name = filename + " PCA data.csv"
	mywriter = csv.writer(open(output_name, 'wb'), dialect='excel')
	mywriter.writerows(data)
	mywriter.writerows(lib_data)
	# mywriter.writerows(singular_values.T)


	return lib_data

"""
Unit tests
"""
if __name__ == "__main__":
	lib_pca_file("data/SNL cr filled in.csv")