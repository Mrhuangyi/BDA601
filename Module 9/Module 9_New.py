#!/usr/bin/env python
# coding: utf-8

# In[12]:

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale  
#Scale here is use for normalization
import random
import numpy as np  
import pandas as pd


# In[13]:


#Create fake income/age clusters for N people in K clusters ( Because we do not have any data here)
#This is a function that it plays like .CSV , we do not have a data here, for this reason we should create Fake data set

# we use def for defining function in python,createClusteredData is the name of our function
#N is total number of data points and K is the number cluster that we want this data have it
#the output of this function will be a data set, we define function here and later on we use it in order to produce data

def createClusteredData(N, k): 
    #here we will say for each cluster how many number points we should have 
    pointsPerCluster = float(N)/k 
    #centroidpoint here find the centerelize points in our data set based on the number of Cluster that we have
    centroidpoints = []
    
    # for number of cluster that we have to find incomeCentroid between 20000.0, 200000.0 
    # Samples are uniformly distributed over the half-open interval [low, high) (includes low, but excludes high)
    # We do the same way for age as well with different rang
    # append here add all centeroid points that we found add to the end of list in our array
    
    for i in range (k): 
        incomeCentroid = random.uniform(20000.0, 200000.0)  
        ageCentroid = random.uniform(20.0, 70.0)
        centroidpoints.append([incomeCentroid, ageCentroid])
        
        
#For i ... here we recognized the number of centroid points
#For J... here create points around centroid points
#np.random.normal it produce data as normal around our centroid point
        
        
        for j in range(int(pointsPerCluster) - 1):
            centroidpoints.append([np.random.normal(loc=incomeCentroid, scale=20000.0), np.random.normal(loc=ageCentroid, scale=2.0)])
            
    centroidpoints = np.array(centroidpoints)
    return centroidpoints


# ## Why we should scale data ?
# If you have two features, one where the differences between cases is large and the other small, are you prepared to have the former as almost the only driver of distance?
# 
# So for example if you clustered people on their weights in kilograms and heights in metres, is a 1kg difference as significant as a 1m difference in height? Does it matter that you would get different clusterings on weights in kilograms and heights in centimetres? If your answers are "no" and "yes" respectively then you should probably scale.

# In[14]:


#here we create data with using above function ( we defind function first , here we use it in order to produce data)
# 100 n , 5 K
data = createClusteredData(100, 5)
#For finding constant range for each parameter we will use scale
#Because Age and income do not have same unit
scaled_data = scale(data)

fig, ax = plt.subplots(1, 2, figsize=(15, 5))
ax[0].scatter(data[:, 0], data[:, 1])
ax[0].set(xlabel='Income', ylabel='Age', title="Bank Data")

ax[1].scatter(scaled_data[:, 0], scaled_data[:, 1])
ax[1].set(xlabel='income', ylabel='Age', title="Scaled Bank Data")

plt.show()


# ## What is Inertia ? 
# Inertia is the sum of squared distance of samples to their closest cluster center. We would like this number to be as small as possible. But, if we choose K that is equal to the number of samples we will get inertia=0

# In[15]:


#we use here for demonstrating elbow curve
#SSE it store inertia for each number of cluster that we want to calculate
SSE = []
#it defind the rang of cluster between 1 to 20 as an example
#SSE.append(model.inertia_) append add intertia number of current model for the range of 1 to 20 at the end the array SSE
for cluster in range(1,20):
    model = KMeans(n_clusters = cluster, init='k-means++')
    model.fit(scaled_data)
    SSE.append(model.inertia_)

#here we want to demonstrate Elbow curve
#first we will create data frame
frame = pd.DataFrame({'Cluster':range(1,20), 'SSE':SSE})
plt.figure(figsize=(12,6))
plt.plot(frame['Cluster'], frame['SSE'], marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')


# In[17]:


#here we found initial cluster number from elbow curve so we do not need to use ++kmean
# 4 here comes from above elbow curve

model = KMeans(n_clusters=4)

# Note I'm scaling the data to normalize it! Important for good results.

model = model.fit(scaled_data)

# print(scale(data))
# print(data)

# We can look at the clusters each data point was assigned to
# These numbers demonstrate cluster with numbers ( 1 belong to one cluser , 2 is belong to another)
print(model.labels_)

# And we'll visualize it:
plt.figure(figsize=(8, 6))
plt.scatter(data[:, 0], data[:, 1], c=model.labels_.astype(np.int))
plt.show()


# In[ ]:




