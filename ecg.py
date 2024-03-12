# -*- coding: utf-8 -*-
"""ECG.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ICMf9c0RjODOvh8G6OXY3-3MEP-3MF8b
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from imblearn.under_sampling import NearMiss
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import seaborn as sns

train_data = pd.read_csv('/content/drive/MyDrive/ML in Medicine/Lab1/mitbih_test.csv', header = None)
test_data = pd.read_csv('/content/drive/MyDrive/ML in Medicine/Lab1/mitbih_train.csv', header = None)

train_data

print('train shape:', train_data.shape,
      'test shape: ', test_data.shape)

ecg_signal = train_data.iloc[0, :-1]  # Assuming the last column is not the signal

# Plot the ECG signal
plt.plot(ecg_signal)
plt.xlabel('Time (samples)')
plt.ylabel('Voltage (mV)')
plt.title('ECG Signal')
plt.grid(True)
plt.show()

train_label = train_data[187].astype(int)
test_label = test_data[187].astype(int)
train_info = train_data.iloc[:,:187]
test_info = test_data.iloc[:,:187]

# Count the occurrences of each class
unique_classes, class_counts = np.unique(train_label, return_counts=True)

# Plotting the histogram with count values on top of each bar
plt.bar(unique_classes, class_counts, align='center', alpha=0.7,color='red')
plt.xlabel('Class Labels')
plt.ylabel('Count')
plt.title('Ratio of Training Class Labels',fontstyle='oblique')

# Adding count values on top of each bar
for i, count in zip(unique_classes, class_counts):
    plt.text(i, count + 0.1, str(count), ha='center', va='bottom')

plt.show()

nm = SMOTE(k_neighbors=5)  # Different versions available
X_resampled, y_resampled = nm.fit_resample(train_info, train_label)

unique_classes, class_counts = np.unique(y_resampled, return_counts=True)

# Plotting the histogram with count values on top of each bar
plt.bar(unique_classes, class_counts, align='center', alpha=0.7,color='purple')
plt.xlabel('Class Labels')
plt.ylabel('Count')
plt.title('Histogram of Class Labels after using SMOTE',fontstyle='oblique')

# Adding count values on top of each bar
for i, count in zip(unique_classes, class_counts):
    plt.text(i, count + 0.1, str(count), ha='center', va='bottom')

plt.show()

MLP = MLPClassifier(hidden_layer_sizes=(100, ), activation='relu', solver='adam', max_iter=200,  random_state=42)
MLP

MLP.fit(X_resampled,y_resampled)

y_pred=MLP.predict(test_info)

cm2 = confusion_matrix(test_label, y_pred)
disp=ConfusionMatrixDisplay(confusion_matrix=cm2,display_labels=unique_classes)
fig, ax = plt.subplots()
disp.plot(ax=ax)
cmap = plt.cm.viridis
cmap.set_bad('lightgray')
ax.imshow(cm2, cmap=cmap)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
plt.show()

from sklearn.metrics import roc_auc_score,roc_curve
from sklearn.datasets import make_classification

y_pred_proba = MLP.predict_proba(test_info)[:, 1]

from sklearn.metrics import classification_report
acc_multi1 = classification_report(y_pred, test_label)

print(acc_multi1)