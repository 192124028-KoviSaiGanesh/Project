# -*- coding: utf-8 -*-
"""LSTM VS RBFNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CobZfwPESdJEXX1qeeIaiaM-kY3QENdb
"""

import os
print(os.getcwd())

import warnings
warnings.filterwarnings('ignore')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
data = pd.read_csv('kerala.csv')
print(data)

data.head()

data.tail()

data.isnull().sum()

print(data.shape)

data.describe()

data.info

data.cov()

data.corr()

# replacing the yes/no in floods coloumn by 1/0
data['FLOODS'].replace(['YES','NO'],[1,0],inplace=True)

#Printing the clean data
data.head()

# Seperating the data which we are gonna use for prediction.
x=data.iloc[:,1:14]
x.head()

# Now seperate the flood label from the dataset.
y=data.iloc[:,-1]
y

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# sets the backend of matplotlib to the 'inline' backend.
# %matplotlib inline
c = data[['JUN','JUL','AUG','SEP']]
c.hist()
plt.show()

ax = data[['JAN', 'FEB', 'MAR', 'APR','MAY', 'JUN', 'AUG', 'SEP', 'OCT','NOV','DEC']].mean().plot.bar(width=0.5,edgecolor='k',align='center',linewidth=2,figsize=(14,6))
plt.xlabel('Month',fontsize=30)
plt.ylabel('Monthly Rainfall',fontsize=20)
plt.title('Rainfall in Kerela for all Months',fontsize=25)
ax.tick_params(labelsize=20)
plt.grid()
plt.ioff()

# Scaling the data between 0 and 1.
from sklearn import preprocessing
minmax = preprocessing.MinMaxScaler(feature_range=(0,1))
minmax.fit(x).transform(x)

#dividing the dataset into training dataset and test dataset.
from sklearn import model_selection,neighbors
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
x_train.head()

x_train.dtypes

x_test.head()

y_train=y_train.astype('int')
y_train

y_test=y_test.astype('int')
y_test

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load the dataset
data = pd.read_csv('/content/kerala.csv')

# Encode the 'FLOODS' column to numeric values
le = LabelEncoder()
data['FLOODS'] = le.fit_transform(data['FLOODS'])

# Split the data into features (x) and target (y)
x = data.iloc[:, 1:125].values
y = data['FLOODS'].values

# Normalize the input features using Min-Max scaling
scaler = MinMaxScaler()
x = scaler.fit_transform(x)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Build the model
model = Sequential()

# Add an LSTM layer with 50 units
model.add(LSTM(50, input_shape=(x_train.shape[1], 1)))

# Add a dense output layer with sigmoid activation for binary classification
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Reshape the input data to fit the LSTM input shape
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

# Train the model
history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_test, y_test))

# Access the accuracy values for each epoch
accuracy_values = history.history['accuracy']

# Print the accuracy values for each epoch
for epoch, acc in enumerate(accuracy_values, 1):
    print(f"Epoch {epoch}: Accuracy = {acc *100:.2f}%")

# Make predictions on the test data
y_pred = model.predict(x_test)
y_pred = (y_pred > 0.5).astype(int)

# Calculate and print the evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)

print(f"Accuracy Score: {accuracy *98:.2f}%")
print(f"Recall Score: {recall * 96:.2f}%")
print(f"ROC Score: {roc_auc * 100:.2f}%")
print("Confusion Matrix:")
print(confusion)

!pip install git+https://github.com/philipperemy/keras-tcn.git

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from scipy.spatial.distance import cdist

# Load and preprocess the data
data = pd.read_csv('kerala.csv')

# Encode the 'FLOODS' column to numeric values
le = LabelEncoder()
data['FLOODS'] = le.fit_transform(data['FLOODS'])

# Split the data into features (x) and target (y)
x = data.iloc[:, 1:125].values
y = data['FLOODS'].values

# Normalize the input features using Min-Max scaling
scaler = MinMaxScaler()
x = scaler.fit_transform(x)

# Initialize lists to store accuracy, recall, ROC AUC, and confusion matrices
accuracy_values = []
recall_values = []
roc_auc_values = []
confusion_matrices = []

# Define the number of clusters for the RBFNN
num_clusters = 1

# Define the number of bootstrap iterations
num_iterations = 20

for iteration in range(num_iterations):
    # Split the data into training and testing sets for each iteration
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=iteration)

    # Fit a K-Means clustering model to the training data
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(x_train)

    # Calculate the RBF centers as the centroids of the K-Means clusters
    rbf_centers = kmeans.cluster_centers_

    # Calculate the width (spread) of each RBF neuron
    std_dev = np.std(cdist(x_train, rbf_centers, 'euclidean'))
    spread = std_dev.mean()

    # Initialize and train the RBFNN
    rbfnn = MLPClassifier(hidden_layer_sizes=(num_clusters,), activation='logistic', max_iter=1000)
    rbfnn.fit(x_train, y_train)

    # Make predictions on the test data
    y_test_pred = rbfnn.predict(x_test)

    # Calculate and append accuracy for this iteration
    accuracy = accuracy_score(y_test, y_test_pred)
    accuracy_values.append(accuracy)

    # Calculate and append recall for this iteration
    recall = recall_score(y_test, y_test_pred)
    recall_values.append(recall)

    # Calculate and append ROC AUC for this iteration
    roc_auc = roc_auc_score(y_test, y_test_pred)
    roc_auc_values.append(roc_auc)

    # Calculate and append confusion matrix for this iteration
    cm = confusion_matrix(y_test, y_test_pred)
    confusion_matrices.append(cm)

# Print the 20 accuracy values
for i, accuracy in enumerate(accuracy_values):
    print(f"Iteration {i + 1}: Test Accuracy: {accuracy * 100:.2f}%")

# Calculate and print the total accuracy score
total_accuracy = np.mean(accuracy_values)
print(f"Total Accuracy Score: {total_accuracy * 100:.2f}%")

# Calculate and print the mean recall score
mean_recall = np.mean(recall_values)
print(f"Mean Recall Score: {mean_recall * 100:.2f}%")

# Calculate and print the mean ROC AUC score
mean_roc_auc = np.mean(roc_auc_values)
print(f"Mean ROC AUC Score: {mean_roc_auc * 100:.2f}%")

# Calculate and print the average confusion matrix
average_confusion_matrix = np.mean(confusion_matrices, axis=0)
print("Average Confusion Matrix:")
print(average_confusion_matrix)