# -*- coding: utf-8 -*-
"""hw1-Kedar-Pankti.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WnxEp9Hplk7Fn6luZxbQM8yRVQy6Nwon

# Homework 1 (Coding)

**Due Sunday 19th September, 11:59pm**

**Submit a link to your completed Google Colab notebook to gradescope.**


If you are working in pairs make sure to add your team member’s name on Gradescope when submitting
"""

"""
Import libraries that you might require
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import operator
import pandas as pd
import io
import requests
from sklearn.metrics import accuracy_score

"""# Load Dataset"""

url="https://raw.githubusercontent.com/susanli2016/Machine-Learning-with-Python/master/diabetes.csv"
response = requests.get(url).content
diabetes = pd.read_csv(io.StringIO(response.decode('utf-8')))
diabetes.head()

# Split the data into training, validation and testing sets

from sklearn.model_selection import train_test_split

data = diabetes.to_numpy()
X, y = data[:, :-1], data[:, -1]

X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, stratify=y, test_size = 0.25, random_state=66)
X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size = 0.4, random_state=66)

"""# Question 3: KNN Classification

We will implement the KNN algorithm for the diabetes dataset. Refer to the pdf and the following functions for the instructions. Complete all the functions as indicated below.
"""

"""
Task 1: Classification

Please implement KNN for K: 3, 5, and 7 
with the following norms:
L1
L2
L-inf

"""

def distanceFunc(metric_type, vec1, vec2):
    """
    Computes the distance between two d-dim vectors
    Args:
        metric_type: String
        vec1 (numpy vector): Vector
        vec2 (numpy vector): Vector
    Returns:
        distance (float): distance between the two vectors
    """

    diff = vec1 - vec2
    if metric_type == "L1":
        distance = sum(abs(vec2-vec1))

    if metric_type == "L2":
        distance = np.sqrt(np.sum(np.power((vec2-vec1),2)))
        
    if metric_type == "L-inf":
        distance = max(abs(vec2-vec1))
        
    return distance

def computeDistancesNeighbors(K, metric_type, X_train, y_train, sample):
    """
    Compute the distances between every datapoint in the train_data and the 
    given sample. Then, find the k-nearest neighbors.
    Return a numpy array of the label of the k-nearest neighbors.
    
    Args:
        K (int): K-value
        metric_type (String): metric type
        X_train (numpy array): Training data
        y_train : Training labels
        sample (numpy vector): Sample whose distance is to computed with every entry in the dataset
        
    Returns:
        neighbors (list): K-nearest neighbors' labels
    """

    distanceArr = []

    for i in X_train:
      distanceArr.append(distanceFunc(metric_type, i, sample))

    distIndexSorted = np.argsort(np.array(distanceArr))
    neighbors = np.ndarray.tolist(y_train[distIndexSorted[1:(K+1)]])

    return neighbors


def Majority(neighbors):
    """
    Performs majority voting and returns the predicted value for the test sample
    Args:
        neighbors (list): K-nearest neighbors' labels
    Returns:
        predicted_value (int or float): predicted label for the given sample
    """
    
    predicted_value = max(set(neighbors), key = neighbors.count)

    return predicted_value


def KNN(K, metric_type, X_train, y_train, X_val):
    """
    Returns the predicted values for the entire validation or test set
    Args:
        K (int): K-value
        metric_type (String): metric type
        X_train (numpy array): Training data
        y_train : Training labels
        X_val or X_test (numpy array): Validation or test data
    Returns:
        predicted_values (list): output for every entry in validation/test dataset 
    """
    
    predictions = []

    for sample in X_val:
      neighbors = computeDistancesNeighbors(K, metric_type, X_train, y_train, sample)
      predictions.append(Majority(neighbors))
    
    return predictions


def evaluation(predicted_values, actual_values):
    """
    Computes the accuracy of the given datapoints.
    
    Args:
        predicted_values: vector
        actual_values: numpy vector
    
    Returns:
        accuracy (float): accuracy
    """
    
    return accuracy_score(predicted_values, actual_values)


def main():
    """
    Calls the above functions in order to implement the KNN algorithm.
    
    Test over the following range K = 3,5,7 and all three metrics. 
    In total you will have nine combinations to try.
    
    PRINTS out the accuracies for the nine combinations on the validation set,
    and the accuracy on the test set for the selected K value and appropriate norm.
    """
    K = [3,5,7]
    norm = ["L1", "L2", "L-inf"]
    
    print("<<<<VALIDATION DATA PREDICTIONS>>>>")

    # for k, metric in zip(K, norm):
    #   predictions = KNN(k, metric, X_train, y_train, X_val)
    #   print(evaluation(predictions, y_val))

    for k in K:
      for metric in norm:
        predictions = KNN(k, metric, X_train, y_train, X_val)
        print(k,metric,evaluation(predictions, y_val))

    print("<<<<TEST DATA PREDICTIONS>>>>")
    for k in K:
      for metric in norm:
        predictions = KNN(k, metric, X_train, y_train, X_test)
        print(k,metric,evaluation(predictions, y_test))

# Finally, call the main function
main()

"""# Question 4: Decision Tree Classification

### Helper functions
The block below contains helper functions for this task.
"""

import numpy as np
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

# Below are a list of helper functions to use to help you on this task

def train_decision_tree(X, y, depth=None, leaf_count=None):
  """
  Trains a decision tree classifier on the given X, y data with the specified 
  tree depth d and max leaf node count max_leaf_num.
  
  Args:
    X ((n,p) np.ndarray): The input Xs, which are in an n (number of samples) by
                          p (number of features) matrix
    y ((n,) np.ndarray): The input ys, which are in an n length array
    depth (int): The maximum depth of the tree. A value of None means no restrictions
             on the depth of the tree.
    leaf_count (int): The maximum leaf count of the tree's leaf nodes. A value of None means 
    no restrictions on the leaf count of the tree.
  
  Returns:
    clf(DecisionTreeClassifier): the trained decision tree classifier
  """
  clf = DecisionTreeClassifier(max_depth=depth, max_leaf_nodes=leaf_count, criterion="entropy", random_state=1)
  clf.fit(X,y)
  return clf

def predict(clf, X_test):
  """
  Uses a trained decision tree classifier to predict on a given test set.
  
  Args:
    clf (DecisionTreeClassifier): Trained Decision Tree Classifer
    X_test ((n,p) np.ndarray): The input Xs, which are in an n (number of samples) by
                               p (number of features) matrix
  
  Returns:
    y_pred ((n,) np.ndarray): The output predictions, which are in an n length array
  """
  y_pred = clf.predict(X_test)
  return y_pred

def evaluate(predicted_values, actual_values):
    """
    Computes the accuracy of the given datapoints.
    
    Args:
        predicted_values: numpy array
        actual_values: numpy array
    
    Returns:
        a floating point number representing the accuracy
    """
    from sklearn.metrics import accuracy_score
    return accuracy_score(predicted_values, actual_values)
  
def plot_line_graph(x_vals, y_vals_1, y_vals_2, y_vals_1_label, y_vals_2_label, x_axis_label, y_axis_label, title):
  """
  Plots a line graph of two lines of different values with common x-values
  
  Args:
    x_vals ((j,) list): Values to be displayed on horizontal axis, where j is number of values
    y_vals_1 ((j,) list): First set of values to be graphed on a line in respect to x_vals, where j is number of values
    y_vals_2 ((j,) list): Second set of values to be graphed on a line in respect to x_vals, where j is number of values
    y_vals_1_label (string): Label for first set of y values
    y_vals_2_label (string): Label for second set of y values
    x_axis_label (string): Label for x axis
    y_axis_label (string): Label for y axis
    title (string): Plot title
  """
  
  plt.plot(x_vals, y_vals_1, color='g', label=y_vals_1_label)
  plt.plot(x_vals, y_vals_2, color='orange', label=y_vals_2_label)
  plt.xlabel(x_axis_label)
  plt.ylabel(y_axis_label)
  plt.title(title)
  plt.legend(loc='upper right')
  plt.show()

"""### Compare Accuracy for full classification dataset as well as smaller classification dataset
We will be using the diabetes classification dataset. You are also given a smaller training dataset with the same data as the full dataset but with only half of the sample number. We will observe the performance changes when less data is available.

To start, uncomment the code below and run to create small dataset. 
"""

# We will also use the same diabetes classification dataset in Task 1.
# Let's create a smaller version of the training dataset using only half of the data available

train_sample_num_small = int(X_train.shape[0] / 2)
X_train_small, y_train_small = X_train[:train_sample_num_small], y_train[:train_sample_num_small]

"""### Base Metrics on Full and Partial Data
To start, you will be comparing the training and testing accuracies of both datasets given a vanilla decision tree.

Note: Make sure to create two separate classifiers for each dataset.
"""

def base_metrics(X_train, y_train, X_train_small, y_train_small, X_val, y_val, X_test, y_test):
  """
  Create a decision tree classifer on the full dataset and the partial dataset (only half of n).
    
  Args: (Note that n is not the same among train and test sets, but merely refers to sample size)
    X_train ((n,p) np.ndarray): Input feature matrix of full dataset for training/fitting
    y_train ((n,) np.ndarray): Input label array of full dataset for training/fitting
    X_train_small ((n,p) np.ndarray): Input feature matrix of partial/small dataset for training/fitting
    y_train_small ((n,) np.ndarray): Input label array of partial/small dataset for training/fitting
    X_val ((n,p) np.ndarray): Input feature matrix of full dataset for validation
    y_val ((n,) np.ndarray): Input label array of full dataset for validation
    X_test ((n,p) np.ndarray): Input feature matrix of full dataset for testing
    y_test ((n,) np.ndarray): Input label array of full dataset for testing    

  To observe:
    train_acc_full_set (float): Training accuracy using a model trained on the full dataset
    val_acc_full_set (float): Validation accuracy using a model trained on the full dataset
    test_acc_full_set (float): Test accuracy using a model trained on the full dataset
    train_acc_small_set (float): Training accuracy using a model trained on the small dataset
    val_acc_small_set (float): Validation accuracy using a model trained on the small dataset
    test_acc_small_set (float): Test accuracy using a model trained on the small dataset
  """
  
  # <---- Your code here ----->
  clfFull = train_decision_tree(X_train, y_train, depth=None, leaf_count=None)
  clfSmall = train_decision_tree(X_train_small, y_train_small, depth=None, leaf_count=None)

  
  trainFull = predict(clfFull, X_train)
  valFull = predict(clfFull, X_val)
  testFull = predict(clfFull, X_test)

  trainSmall = predict(clfSmall, X_train_small)
  valSmall = predict(clfSmall, X_val)
  testSmall = predict(clfSmall, X_test)

  train_acc_full_set = evaluate(trainFull, y_train)
  val_acc_full_set = evaluate(valFull, y_val)
  test_acc_full_set = evaluate(testFull, y_test)
  train_acc_small_set = evaluate(trainSmall, y_train_small)
  val_acc_small_set = evaluate(valSmall, y_val)
  test_acc_small_set = evaluate(testSmall, y_test)
  # <---- Your code ends here ----->
  
  print("Train Accuracy on Full Dataset: ", train_acc_full_set)
  print("Validation Accuracy on Full Dataset: ", val_acc_full_set)
  print("Test Accuracy on Full Dataset: ", test_acc_full_set)
  print("Train Accuracy on Small (Half) Dataset: ", train_acc_small_set)
  print("Validation Accuracy on Small (Half) Dataset: ", val_acc_small_set)
  print("Test Accuracy on Small (Half) Dataset: ", test_acc_small_set)
  
  return (train_acc_full_set, 
          val_acc_full_set, 
          test_acc_full_set,
          train_acc_small_set, 
          val_acc_small_set, 
          test_acc_small_set)

"""Uncomment the code below and run the code. """

base_metrics(X_train, y_train, X_train_small, y_train_small, X_val, y_val, X_test, y_test)

"""### Question 4.1 Report on LaTeX
Answer the following questions on LaTeX in the respective section.
1. Report the results of the accuracies on LateX 
2. Which dataset had a higher difference between training and test accuracy? Briefly explain why.

### Improving Decision Tree for Smaller Dataset by Tuning Hyperparameters
Classifiers often overfit on smaller datasets, so now, we will optimize hyperparameters on tree depth and max leaf count to improve the performance of our model. 

Fill out the helper functions below which will take an array of hyperparameter values for tree depth and an array of hyperparameter values for max leaf count. The helper function will return a training and validation accuracy scores for each pair of hyperparameter values. This is referred to as grid search for hyperparameter tuning.

At the end, the function identifies the best value of the tree depth and tree node count hyperparameters for a dataset, as well as the final training and testing scores.

Note: Use the highest validation score to choose the optimal hyperparameter combination. If there is a tie, use the lower hyperparameter value.
"""

def grid_search_depth_and_leaf_count(depth_search_space, leaf_count_search_space, X_train, y_train, X_val, y_val):
  """
  Perform a decision tree hyperparameter grid search on tree depth and leaf count given training and validation data.
    
  Args:
    depth_search_space ((d,) list): Tree depth values to search over, i.e. [1, 3, 6, 10, 30]
    leaf_count_search_space ((l,) list): Max leaf count values to search over, i.e. [2, 3, 4, 5, 6]
    X_train ((n, p) np.ndarray): The input feature matrix for training
    y_train ((n, p) np.ndarray): The input ys for training
    X_val ((n, p) np.ndarray): The input feature matrix that will be used to validate accuracy scores
    y_val ((n, p) np.ndarray): The input ys that will be used to validate accuracy scores
    
  To return:
    best_depth (int): The depth count in the hyperparameter combination with the largest validation score
    best_leaf_count (int): The leaf count in the hyperparameter combination with the largest validation score
  """
  accuracy = []
  # <---- Your code here ----->
  for a in depth_search_space:
    for b in  leaf_count_search_space:
      clf = train_decision_tree(X_train, y_train, depth = a, leaf_count = b)
      pred = predict(clf, X_val)

      accuracy.append(evaluate(pred, y_val))

  import itertools
  from itertools import permutations
  index = np.argmax(accuracy)
  best_depth, best_leaf_count = list(itertools.product(depth_search_space,leaf_count_search_space))[index]
  # <---- Your code ends here ----->

  print("Chosen Depth: ", best_depth)
  print("Chosen Leaf: ", best_leaf_count)
  
  return best_depth, best_leaf_count

"""Uncomment and run the code below to and record the best depth and best leaf count hyperparameters on LaTeX in the respective section."""

# Search spaces for grid search to tune tree depth and leaf count hyperparameters
depth_search_space = [1, 3, 6, 10, 30]
leaf_count_search_space = [2, 3, 4, 5, 6]

print("FULL DATASET")
grid_search_depth_and_leaf_count(depth_search_space, 
                                 leaf_count_search_space, 
                                 X_train, 
                                 y_train, 
                                 X_val, 
                                 y_val)

print("\nSMALL DATASET")
grid_search_depth_and_leaf_count(depth_search_space, 
                                 leaf_count_search_space, 
                                 X_train_small, 
                                 y_train_small, 
                                 X_val,
                                 y_val)

"""### Question 4.2 Report on LaTeX
Answer the following questions on LaTeX in the respective section.
1. Report the chosen hyperparameters for both the complete set and the partial set.
2. Did the small dataset have higher or lower chosen hyperparameter values than the full dataset? Briefly explain why.

### Retrain Decision Tree and Plot Hyperparameter Search
Now retrain your decision tree with the optimal hyperparameters. Report training, validation, and testing error for the small dataset.

Also for the small dataset, create a graph plotting the training and validation scores for each leaf node hyperparameter value, holding the tree depth hyperparameter consistent at the chosen value.
"""

def retrain_decision_tree(X_train, y_train, X_val, y_val, X_test, y_test):
  
  """
  Perform a decision tree hyperparameter grid search given training and validation data and search values for
  tree depth and leaf node count.
    
  Args: (Note that n is not the same among train and test sets, but merely refers to sample size)
    X_train ((n,p) np.ndarray)
    y_train ((n,) np.ndarray)
    X_val ((n,p) np.ndarray)
    y_val ((n,) np.ndarray)
    X_test ((n,p) np.ndarray)
    y_test ((n,) np.ndarray)

  To return:
    train_acc (float): Optimal Hyperparameters Train Accuracy
    val_acc (float): Optimal Hyperparameters Train Accuracy
    test_acc (float): Optimal Hyperparameters Train Accuracy
    
    leaf_count_train_scores (list): Report training scores for max leaf count search space
    leaf_count_val_scores (list): Report validation scores for max leaf count search space
  """
  # Select best hyperparameters
  depth_search_space = [2, 4, 6, 8, 10, 16, 20]
  leaf_count_search_space = [2, 3, 4, 5, 6, 7, 8, 9, 10] 

  chosen_depth, chosen_leaf_count = grid_search_depth_and_leaf_count(depth_search_space, 
                                                                     leaf_count_search_space, 
                                                                     X_train, 
                                                                     y_train, 
                                                                     X_val, 
                                                                     y_val)
  
  # <---- Your code here ----->          
  clf = train_decision_tree(X_train, y_train, depth = chosen_depth, leaf_count = chosen_leaf_count)
  predTrain = predict(clf, X_train)
  predVal = predict(clf, X_val)
  predTest = predict(clf, X_test)

  train_acc = evaluate(predTrain, y_train)
  val_acc = evaluate(predVal, y_val)
  test_acc = evaluate(predTest, y_test)

  leaf_count_train_scores = []
  leaf_count_val_scores = []

  for leaf_count in leaf_count_search_space:
    clf = train_decision_tree(X_train, y_train, depth = chosen_depth, leaf_count = leaf_count )
    predTrain = predict(clf, X_train)
    predVal = predict(clf, X_val)

    leaf_count_train_scores.append(evaluate(predTrain, y_train))
    leaf_count_val_scores.append(evaluate(predVal, y_val))

  plot_line_graph(leaf_count_search_space, leaf_count_train_scores, leaf_count_val_scores, "Training Score", "Validation Score", "Leaf Count", "Scores", "Hyperparameter Tuning")
  
  # <---- Your code ends here ----->
  
  print("Optimal Hyperparameters Train Accuracy: ", train_acc)
  print("Optimal Hyperparameters Validation Accuracy: ", val_acc)
  print("Optimal Hyperparameters Test Accuracy: ", test_acc)
  
  print("Training Scores per Max Leaf Node Count:", leaf_count_train_scores)
  print("Validation Scores per Max Leaf Node Count:", leaf_count_val_scores)
  
  return (train_acc, val_acc, test_acc, leaf_count_train_scores, leaf_count_val_scores)

"""Run the code above for the small dataset and by uncommenting code below. Report all necessary values and both graphs on Latex."""

retrain_decision_tree(X_train_small, y_train_small, X_val, y_val, X_test, y_test)

"""### Question 4.3 Report on LaTeX
Answer the following question on LaTeX in the respective section.
1. Report the values on LaTeX.
2. How did the training accuracy and testing accuracy change after tuning compared to before? Briefly explain why.
3. Paste the plot and explain any trends or patterns with the plot within validation and training scores and briefly explain why.

## Additional Exercise (Ungraded)

This section is ungraded. You can try it out for fun. sklearn's [DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) used in this homework has a parameter called **min_samples_split**. Try playing around with it's values to see if you can get better accuracy for the X_train_small dataset. 

You don't need to add results of this section in your submission. It is for you to try out.

# Question 5: Feature Scaling Effects on KNNs and DTs

### Observing effects of standardizing features

Up until now, we have not been using standardized features. Let's observe the effects of standardized features with decision trees and KNNs.

Standardization, or feature scaling / data normalization, is a common preprocessing step for data within machine learning. We will see why it's important.

Here is a definition taken from SK-Learn's website on Standardization:

*Standardization of datasets is a common requirement for many machine learning estimators implemented in scikit-learn; they might behave badly if the individual features do not more or less look like standard normally distributed data: Gaussian with zero mean and unit variance.*

*In practice we often ignore the shape of the distribution and just transform the data to center it by removing the mean value of each feature, then scale it by dividing non-constant features by their standard deviation.*

Learn More: https://scikit-learn.org/stable/modules/preprocessing.html

To start, uncomment the code below and run to retrieve the data. (Recomment before submission.)
"""

# We will use the same data as the previous tasks
# Normalize data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

"""### Helper Functions
  
We implemented above the KNN algorithm. Sci-kit learn also has their own version of the KNN algorithm which we will use in this following task. Use the two helper functions below in this next task.
"""

from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

def train_KNN(X, y, norm=2, K=5):
  """
  Trains a KNN classifier on the given X, y data with the specified 
  norm and K.
  
  Args:
    X ((n,p) np.ndarray): The input Xs, which are in an n (number of samples) by
                          p (number of features) matrix
    y ((n,) np.ndarray): The input ys, which are in an n length array
    norm (int): The number form of the norm. Note that sklearn only allows L1 and L2 norms,
                (norm would be 1 and 2 respectively). Default is 2.
    K (int): The value of K for the KNN algorithm. Default is 5.
  
  Returns:
    clf(KNeighborsClassifier): the trained KNN model
  """
  
  clf = KNeighborsClassifier(n_neighbors=K, p=norm)
  clf.fit(X,y)
  return clf

def train_decision_tree(X, y, depth=None, leaf_count=None):
  """
  This helper function is defined again from a previous section. 
  
  Trains a decision tree classifier on the given X, y data with the specified 
  tree depth d and max leaf node count max_leaf_num.
  
  Args:
    X ((n,p) np.ndarray): The input Xs, which are in an n (number of samples) by
                          p (number of features) matrix
    y ((n,) np.ndarray): The input ys, which are in an n length array
    depth (int): The maximum depth of the tree. A value of None means no restrictions
             on the depth of the tree.
    leaf_count (int): The maximum leaf count of the tree's leaf nodes. A value of None means 
    no restrictions on the leaf count of the tree.
  
  Returns:
    clf(DecisionTreeClassifier): the trained decision tree
  """
  clf = DecisionTreeClassifier(max_depth=depth, max_leaf_nodes=leaf_count, criterion="entropy", random_state=1)
  clf.fit(X,y)
  return clf

def predict(clf, X_test):
  """
  This helper function is defined again from a previous section. 
  
  Uses a trained model to predict on a given test set.
  
  Args:
    clf (Classifier): Trained classifier such as KNN or Decision Tree
    X_test ((n,p) np.ndarray): The input Xs, which are in an n (number of samples) by
                               p (number of features) matrix
  
  Returns:
    y_pred ((n,) np.ndarray): The output predictions, which are in an n length array
  """
  y_pred = clf.predict(X_test)
  return y_pred

def evaluate(predicted_values, actual_values):
    """
    This helper function is defined again from a previous section. 
    
    Computes the accuracy of the given datapoints.
    
    Args:
        predicted_values: numpy array
        actual_values: numpy array
    
    Returns:
        a floating point number representing the accuracy
    """
    return accuracy_score(predicted_values, actual_values)

"""### Retrieving Metrics for Unstandardized Data
Fill out this function to retrieve training and test accuracies for both KNN and decision tree models. Use default hyperparameters.
"""

def get_classifier_metrics(X_train, y_train, X_test, y_test):
  """
  Create a decision tree and KNN classifer on the normal dataset.
    
  Args: (Note that n is not the same among train and test sets, 
         but merely refers to sample size)
    X_train ((n,p) np.ndarray)
    y_train ((n,) np.ndarray)
    X_test ((n,p) np.ndarray)
    y_test ((n,) np.ndarray)

  To return:
    knn_train_accuracy (float): Accuracy of KNN for train set
    knn_test_accuracy (float): Accuracy of KNN for test set
    dt_train_accuracy (float): Accuracy of DT for train set
    dt_test_accuracy (float): Accuracy of DT for test set    
  """
  
  # <---- Your code here ----->
  clfKNN = train_KNN(X_train, y_train)
  clfDT = train_decision_tree(X_train, y_train)

  predictKNNTrain = predict(clfKNN, X_train)
  predictKNNTest = predict(clfKNN, X_test)

  predictDTTrain = predict(clfDT, X_train)
  predictDTTest = predict(clfDT, X_test)

  knn_train_accuracy = evaluate(predictKNNTrain, y_train)
  knn_test_accuracy = evaluate(predictKNNTest, y_test)

  dt_train_accuracy = evaluate(predictDTTrain, y_train)
  dt_test_accuracy = evaluate(predictDTTest, y_test)
  # <---- Your code ends here ----->
  
  print("knn_train_accuracy: ", knn_train_accuracy)
  print("knn_test_accuracy: ", knn_test_accuracy)
  print("dt_train_accuracy: ", dt_train_accuracy)
  print("dt_test_accuracy: ", dt_test_accuracy)
  
  return knn_train_accuracy, knn_test_accuracy, dt_train_accuracy, dt_test_accuracy

"""Uncomment the code below and run the code."""

print("FOR UNSTANDARDIZED DATA")
get_classifier_metrics(X_train, y_train, X_test, y_test)

print("\nFOR STANDARDIZED DATA")
get_classifier_metrics(X_train_scaled, y_train, X_test_scaled, y_test)

"""### Question 5 Report on LaTex
Answer the following question on LaTeX in the respective section.
1. Report the values on LaTeX.
2. What happens to performance when we use standardization for data with decision trees? What about KNN? Briefly explain why each happened.

# Submission

**Due Sunday 19th September, 11:59pm**

**Submit a link to your completed Google Colab notebook to gradescope.**

If you are working in pairs make sure to add your team member’s name on Gradescope when submitting
"""