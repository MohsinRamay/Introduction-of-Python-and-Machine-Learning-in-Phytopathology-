# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 09:35:49 2022

@author: Xing Wei and Marcela A. Johnson

# Version_031321: select the top wavelengths with custom distance apart
"""
# import libraries
import numpy as np
import pandas as pd

# define a function to filter out elements that were within the distance of an wavelength
def get_wl_range(wl_test, low_range, high_range):
    ## filters the list based on the condition
    new_list = list(filter(lambda x: int(float(x)) <= low_range or int(float(x)) >= high_range, wl_test))
    return new_list

# define the function of band_select_distance() to select wavelengths with custom distance apart
def band_select_distance(X, featureScores, distance, top_n_features):
    # sort the featureScores dataframe based on feature weight and ignore the original index
    feature_sorted = featureScores.sort_values(by = 'Score', ascending=False, ignore_index=True)
    # store the list of wavelengths after sorting based on their scores
    wl = feature_sorted['Wavelengths']
    
    # set the distance between each selected features
    distance = distance
    # set the number of top features to be selected
    top_n_features = top_n_features
    # intialize the final list
    wl_dist = wl
    
    # setup the loop to filter out elements based on the order of original list
    for j in range(len(wl_dist)):
        low_r = int(float(wl_dist[j]))- distance
        high_r = int(float(wl_dist[j]))+ distance
        x = get_wl_range(wl_dist, low_r, high_r)
        wl_dist = [wl_dist[j]] + x
        j += 1
        if j == len(wl_dist):
            break
    # the final list should be with the reversed order
    wl_dist = list(reversed(wl_dist))
                
    # build up the new dataset with spectral reflectance values from the selected wavelengths
    X_dist = []
    column_name = []
    for wl in wl_dist[0:top_n_features]:
        column_name.append(wl)
        X_dist.append(X[wl].values)
    
    # covert the X_dist from list to dataframe
    from pandas import DataFrame
    X_dist = DataFrame (X_dist)
    X_dist = X_dist.T
    X_dist.columns = column_name
    # return the new dataframe of top selected bands with custom distance and their reflectance values
    return X_dist