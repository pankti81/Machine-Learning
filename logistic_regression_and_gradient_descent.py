# -*- coding: utf-8 -*-
"""Logistic Regression and Gradient Descent

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dXGTpt7za7CHSBqtkktNawVpR8eSSnIW

# Homework 3: Coding

**Due Monday October 5th, 11:59pm.**

**Submit hw3.ipynb file to Gradescope (you may submit as many times as you'd like before the deadline).**
"""

"""
Import libraries that you might require.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.linear_model import LogisticRegression

np.__version__

"""
FOR COLAB USERS ONLY

Run the following code to upload and unzip the data into the Colab environment.

"""
from google.colab import files
uploaded = files.upload()

!unzip hw3_q3.zip

"""# Question 3: Kernel Regression

In this question, you are going to implement a Kernel Regression model using Gaussian kernel method.

Given a training dataset $S=((\mathbf{x_1}, y_1), \ldots , (\mathbf{x_n}, y_n))$, and kernel function $K(\cdot,\cdot)$, the predicted value $\hat{y}$ of an input data $\mathbf{x}$ is:
$$\hat{y}(\mathbf{x}) = \frac{\sum_{i=1}^n K(\mathbf{x}, \mathbf{x_i}) y_i}{\sum_{i=1}^n K(\mathbf{x}, \mathbf{x_i}) }$$, where $K(\mathbf{x}, \mathbf{x_i}) = \text{exp}(\frac{-||\mathbf{x} - \mathbf{x_i}||_2^2}{\sigma^2})$

## Question 3.1 Build the model.
Fill in your code for function **GaussianKernel** and **kernelRegression**. For $\sigma = \{0.01, 0.05, 0.1, 0.15, 0.2, 0.5, 1.0\}$, fill in your code for function **evaluation** to compute the means squared error of the model for each $\sigma$ value.
"""

"""
Reads the data.
"""
# TODO your code here
X_test= pd.read_csv('X_test.txt', header=None).values
y_test = pd.read_csv('y_test.txt', header=None).values
X_train = pd.read_csv('X_train.txt', header=None).values
y_train = pd.read_csv('y_train.txt', header=None).values

y_test.shape

# build the model
def GaussianKernel(sigma, vec1, vec2):
    """
    Computes the gaussian kernel between two d-dim vectors
    Args:
        sigma: a single floating number
        vec1: (d,)-shape numpy vector
        vec2: (d,)-shape numpy vector
    Returns:
        distance: a single floating number
    """
    # TODO your code here: Question 3.1
    distance = np.exp(np.divide(np.negative(np.square(np.linalg.norm(vec1-vec2, 2))), np.square(sigma)))

    return distance

# print(GaussianKernel(2, np.array([0,2]), np.array([3,6])))

def kernelRegression(X_train, y_train, X_test, sigma):
    """
    Computes the predicted values for test set X_test based on kernel regression model
    Args:
        X_train: (n,p) feature matrix of training set
        y_train: truth value of training set
        X_test: feature matrix of test set
        sigma: hyperparameter for Gaussian kernel
    Returns:
        y_predict: list of predicted target values for X_test
    """
    # TODO your code here: Question 3.1
    # You need to call the function "GaussianKernel" here
    # y_predict = [0]*len(X_test)    # initialzation
    y_predict=[]
    for i in X_test:
      num=0
      den=0
      for idx,j in enumerate(X_train):
        num = num + GaussianKernel(sigma, i, j) * y_train[idx]
        den = den + GaussianKernel(sigma, i, j)
      y_predict.append(np.divide(num, den))
    return y_predict

# y_predict = kernelRegression(X_train, y_train, X_test, 2)
# print(len(y_predict))
# evaluate the model
def evaluation(y_predict, y_true):
    """
    Computes the mean squared error for regression task.
    
    Args:
        y_predict: list of predicted target values
        y_true: list or numpy array of true target values
    
    Returns:
        error: a floating point number representing the error for a validation or test set
    """    
    # TODO your code here: Question 3.1
    # you can use the sklearn libary mean_squared_error
    
    
    error = mean_squared_error(y_true, y_predict)
    return error
# print(evaluation(y_predict,y_test))

"""## Question 3.2 Analysis of the model.
Similar to what you did for HW2, plot a figure for each sigma value of predicted regression line and scatter plot of data points in the test set. Report the sigma value with the smallest MSE for the test set. How the value of sigma affects the kernel regression model? Compare the figures in this question with the figure in question 1.1 of HW2. Describe your findings based on the comparison.
"""

# plot the kernel regression result
def plotRegression(X_train, y_train, X_test, y_test, y_pred, sigma):
    """
    Plot the predicted regression line and scattor plot of data points in the test set
    Args:
        sigma: sigma value for Gqussian kernel
    Return:
        error: mean squared error of the model given the sigma
    """
    error = evaluation(y_pred, y_test)
    x = np.linspace(0,1,1000)
    y_regression = kernelRegression(X_train, y_train, x, sigma)
    
    plt.plot(x, y_regression, '-', color = 'red')
    plt.scatter(X_test, y_test, alpha = 0.75)
    plt.title('Gaussian kernel regression with sigma = ' + str(sigma) + '\n MSE = ' + str(error))
    plt.xlabel('feature value')
    plt.ylabel('target value')
    plt.show()

    
def main(X_train, y_train, X_test, y_test, sigma_set):
    """
    Build the Gaussian kernel regression for each sigma in sigma_set, and then plot the result
    """

    for sigma in sigma_set:
        y_pred = kernelRegression(X_train, y_train, X_test, sigma)
        plotRegression(X_train, y_train, X_test, y_test, y_pred, sigma)

""" 
Finally, we call the main function.
"""
sigma_set = [0.01, 0.05, 0.1, 0.15, 0.2, 0.5, 1.0]
main(X_train, y_train, X_test, y_test, sigma_set)

"""The answer for quesiton 3.2 should be written on the PDF file that you submit to Gradescope.

# Question 4: Logistic Regression and Gradient Descent
"""

"""
Import required libraries.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.linear_model import LogisticRegression

"""
FOR COLAB USERS ONLY

Run the following code to upload and unzip the data into the Colab environment.

"""
from google.colab import files
uploaded = files.upload()
! unzip hw3_house_sales.zip

"""Implement the following functions for question 1. Please use the sklearn implementation of linear regression or other imports beyond those listed above."""

"""
load data, a const dimension (for weight b) is already included in X.
"""
X_train = pd.read_csv('X_train.csv')
X_test = pd.read_csv('X_test.csv')
y_train = pd.read_csv('y_train.csv')
y_test = pd.read_csv('y_test.csv')

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

print(X_test.head(5))
print(y_test.head(5))

"""
Do some data preparation, convert dataframe to numpy array
"""
n_features = X_train.shape[1]

w = np.zeros((1, n_features))

# turn dataframe to np array
X_train = X_train.values
X_test = X_test.values

y_train = y_train.values
y_test = y_test.values

m_train =  X_train.shape[0]
m_test =  X_test.shape[0]

"""**Logistic regression with scikit** Fill in the logisticRegressionScikit() function. Report the weights, training accuracy, and the test accuracy. We will not use any penalty here, so set the parameters penalty = 'none', solver = 'saga'.Also, we will use 2000 iterations for a fair comparison to later algorithms, so also set the parameter max_iter=2000."""

def LogisticRegressionScikit(X_train, y_train, X_test, y_test):

    """
    Computes logistic regression with scikit-learn.
    
    Args:
        X_train: feature matrix of training set, np array of (n, p)
                 where n is the number of training observations, 
                 p is the number of features
        y_train: truth value of training set, np array of (n, 1)

        X_test: feature matrix of test set, np array of (m, p)
                 where m is the number of test observations,
                 p is the number of features
        y_test: truth value of test set, np array of (m, 1)

    Returns:  
        w: numpy array of learned coefficients
        y_pred: numpy array of predicted labels for the test data
        score: accuracy of test data
    """
    logreg= LogisticRegression(penalty = 'none', fit_intercept = False, solver= 'saga', max_iter=2000)
    logreg.fit(X_train, y_train)
    coef=logreg.coef_
    y_pred= logreg.predict(X_test)
    score=logreg.score(X_test, y_test)
    return coef, y_pred, score

"""
Results for logistic regression Scikit function
"""

coef_scikit, y_pred_scikit, acc_scikit = LogisticRegressionScikit(X_train, y_train, X_test, y_test)

print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(acc_scikit))
print('logistic regression coefficient:', coef_scikit)

"""**Logistic regression with simple gradient descent** Fill in the LogisticRegressionGD() function. To do that, two helper functions sigmoid_activation(), to calculate the sigmoid function result, and model_optimize(), to calculate the gradient of w, will be needed. Both helper functions can be used in the following AdaGrad optimization function. Use a learning rate of $10^{−4}$, run with 2000 iterations. Report the weights and accuracy. Keep track of the accuracy every 100 iterations in the training set. It will be used later."""

def sigmoid_activation(result):
    """
    Calculates the sigmoid function.
    
    Args:
        x: numpy array of input, of shape (1, n)
           where n is the number of observations
        
    Returns:
        final_result: numpy array of sigmoid result, of shape (1, n)
                      where n is the number of observations
    """
    final_result= 1 / ( 1 + np.exp(-result))
    return final_result

"""We add a predict() function here to threshold probability prediction into binary classification"""

def predict(final_pred, n):
    """
    Predict labels from probability to 0/1 label, threshold 0.5.
    
    Args:
        final_pred: numpy array of probabilty that each sample belonging to class 1, of shape (1, n)
                    where n is the number of observations 
        
    Returns:
        y_pred: numpy array of label of each sample, of shape (1, n)
                where n is the number of observations
    """
    y_pred = np.where(final_pred < 0.5, 0, 1)
    return y_pred

"""**Remember to derive the gradient, write down the weight update formula, and hand in them to the latex submission!**"""

def model_optimize(w, X, Y):
    
    """
    Calculates gradient of the weights.
    
    Args:
        X: numpy array of training samples of shape (n, p)
           where n is the number of observations
           p is the number of features
        Y: numpy array of training labels of shape (n, 1)
        w: numpy array of weights of shape (1, p)
    Returns:
        dw: the gradient of the weights of shape (1, p)
    """
    dw = np.dot(((sigmoid_activation(np.dot(X, w.T)))-Y).T, X) 
    # Y-(1/e^(-Xw.T).T* X)
    # nn_out= sigmoid_activation(np.dot(X, np.transpose(w)))
    # error = Y - nn_out
    # dw= np.dot(np.transpose(error), X)
    # print(w.shape, w.T.shape)
    return dw

def LogisticRegressionGD(w, X, Y, learning_rate, num_iterations):
    """
    Uses batch gradient descent to update weights for logistic regression.

    Args:       
        w: numpy array of initial weights of shape (1, p)
           where p is the number of features
        X: numpy array of training samples of shape (n, p)
           where n is the number of observations
        Y: numpy array of training labels of shape (n, 1)
        learning_rate: float number learning rate to update w
        num_iterations: int number of iterations to update w
    
    Returns:  
        coeff: numpy array of weights after optimization of shape (1, p)
        accuracies: a list of accuracy at each hundred's iteration. With 2000 iterations, 
                    accuracies should be a list of size 21 (starting from 0)
    """
    # print(w.shape,X.shape[1])
    accuracies=[0]
    for i in range(num_iterations):
      dw = model_optimize(w, X, Y)
      w = w - learning_rate * dw/X.shape[0]    
      # print(w.shape)
      if (i%100 == 0):
        final_pred = sigmoid_activation(np.dot(X,w.T))
        y_pred = predict(final_pred.T, 800)
        # print(y_pred.shape)
        accuracies.append(accuracy_score(Y, y_pred.T))
    return w, accuracies

"""**Logistic regression with AdaGrad** Fill in the LogisticRegressionAda() function. Use a learning rate of $10^{−4}$, run with 2000 iterations. Report the weights and accuracy. Keep track of the accuracy every 100 iterations in the training set. It will be used later."""

def LogisticRegressionAda(w, X, Y, learning_rate, num_iterations):

    """
    Use AdaGrad to update weights.
    
    Args:       
        w: numpy array of initial weights of shape (1, p)
           where p is the number of features
        X: numpy array of training samples of shape (n, p)
           where n is the number of observations
        Y: numpy array of training labels of shape (n, 1)
        learning_rate: float number learning rate to update w
        num_iterations: int number of iterations to update w
    
    Returns:  
        coeff: numpy array of weights after optimization of shape (1, p)
        accuracies: a list of accuracy at each hundred's iteration. With 2000 iterations, 
                    accuracies should be a list of size 21 (starting from 0)
    """

    accuracies = [0]

    G = 0
    for i in range(num_iterations):
        dw = model_optimize(w, X, Y)   
        G = G + dw**2      
        w = w - (learning_rate/np.sqrt(G)) * dw
        if (i%100 == 0):
          final_pred= sigmoid_activation(np.dot(X,np.transpose(w)))
          y_pred= predict(np.transpose(final_pred),final_pred.shape[0])
          # print(y_pred.shape)
          accuracies.append(accuracy_score(Y,np.transpose(y_pred)))
    return w, accuracies

"""Now we start to use our dataset and construct model.

Model construction for GD logistic regression.
"""

"""
Results for gradient descent weight update
"""

# Gradient Descent
coeff_GD, acc_GD = LogisticRegressionGD(w, X_train, y_train, learning_rate=0.0001,num_iterations=2000)

# predict probability
final_train_pred_GD = sigmoid_activation(np.dot(coeff_GD, X_train.T) )
final_test_pred_GD = sigmoid_activation(np.dot(coeff_GD, X_test.T) )
# predict label
y_train_pred_GD = predict(final_train_pred_GD, m_train)
y_test_pred_GD = predict(final_test_pred_GD, m_test)

print('Optimized weights for GD', coeff_GD)

print('Training Accuracy for GD', accuracy_score(y_train_pred_GD.T, y_train))
print('Test Accuracy for GD', accuracy_score(y_test_pred_GD.T, y_test))

"""Model construction for AdaGrad logistic regression."""

"""
Results for AdaGrad Descent weight update
Please comment out these statements before converting to .py file and submitting.
"""
coeff_Ada, acc_Ada = LogisticRegressionAda(w, X_train, y_train, learning_rate=0.0001, num_iterations=2000)

# predict probability
final_train_pred_Ada = sigmoid_activation(np.dot(coeff_Ada, X_train.T) )
final_test_pred_Ada = sigmoid_activation(np.dot(coeff_Ada, X_test.T) )

# predict label
y_train_pred_Ada = predict(final_train_pred_Ada, m_train)
y_test_pred_Ada = predict(final_test_pred_Ada, m_test)

print('Optimized weights for Ada', coeff_Ada)

print('Training Accuracy for Ada', accuracy_score(y_train_pred_Ada.T, y_train))
print('Test Accuracy for Ada', accuracy_score(y_test_pred_Ada.T, y_test))

"""Plot accuracy vs iteration for GD and AdaGrad. Compare the performance difference. Briefly explain the reason."""

"""
Plot accuracy vs iteration for GD and AdaGrad
"""
plt.plot(acc_GD, label='GD')
plt.plot(acc_Ada, label='AdaGrad')
plt.ylabel('Accuracy')
plt.xlabel('iterations (per hundreds)')
plt.title('Accuracy improvement over time')
plt.legend(loc='lower right')
plt.show()

