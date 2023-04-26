import joblib
import cv2
import numpy as np
import os
import pandas as pd
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.feature import local_binary_pattern
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def predict(file):
    model = joblib.load('./model/modelGray3.pkl')
    radius = 1
    n_points = 8 * radius
    METHOD = 'uniform'

    # Load the new image and convert it to grayscale
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Preprocess the image
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # lower_bound = 100
    # upper_bound = 200
    # mask = cv2.inRange(grayscale, lower_bound, upper_bound)
    # grayscale = cv2.bitwise_and(grayscale, grayscale, mask=mask)

    # Extract the LBP features
    lbp = local_binary_pattern(gray, n_points, radius, METHOD)
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    hist = hist.astype('float')
    hist /= (hist.sum() + 1e-7)
    prediction = model.predict([hist])

    # Print the predicted class label
    if prediction[0] == "parkinson":
        return 'You may be Diagnosed with Parkinson'
    else:
        return 'You are Healthy!!'
