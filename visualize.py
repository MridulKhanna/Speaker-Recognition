import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

from sklearn.decomposition import PCA as sklearnPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.datasets.samples_generator import make_blobs

from pandas.tools.plotting import parallel_coordinates

labels = []
for i in xrange(25):
	labels.append("feature_"+str(i+1))
labels.append("class")
data = pd.read_csv('datarand.csv', names=labels)


#data = np.array(data).astype("float")
data.hist()
plt.show()

'''
data.plot(kind='density', subplots=True, layout=(5,6), sharex=False)
plt.show()
'''

reader = csv.reader(open("datarand.csv", "rb"), delimiter=",")
x = list(reader)
result = np.array(x).astype("float")

x = result[:,0:25]
y = result[:,25]

x_norm = (x - x.min())/(x.max()-x.min())
print(x.shape,y.shape,x_norm.shape)
#x_norm = x

#LDA begin
lda = LDA(n_components=3) #2-dimensional LDA
lda_transformed = pd.DataFrame(lda.fit_transform(x_norm, y))

# Plot all three series
plt.scatter(lda_transformed[y==4][0], lda_transformed[y==4][1], label='Speaker 1', c='red')
plt.scatter(lda_transformed[y==5][0], lda_transformed[y==5][1], label='Speaker 2', c='blue')
plt.scatter(lda_transformed[y==6][0], lda_transformed[y==6][1], label='Speaker 3', c='lightgreen')

# Display legend and show plot
plt.legend(loc=3)
plt.show()
#LDA end


#PCA begin
pca = sklearnPCA(n_components=2) #2-dimensional PCA
transformed = pd.DataFrame(pca.fit_transform(x_norm))

plt.scatter(transformed[y==7][0], transformed[y==7][1], label='Speaker 1', c='red')
plt.scatter(transformed[y==8][0], transformed[y==8][1], label='Speaker 2', c='blue')
plt.scatter(transformed[y==1][0], transformed[y==1][1], label='Speaker 3', c='lightgreen')

plt.legend()
plt.show()
#PCA end
