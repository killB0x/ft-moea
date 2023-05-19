#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on Mon Sep 27GENERATE FAILURE DATA SETS VIA MONTE CARLO METHODThis files generates the failure data set from the string of a fault tree via the Monte Carlo method. The input variables are:    - save_folder: Specify the path where the failure data set is     going to be saved in a .mat file.        - fts_string: Write a fault tree model in an string form, as an example     the string 'AND(BE1,OR(BE3,BE4))' is a fault tree with AND gate on the top     event, an OR gate is connected to the top event. There are in total three    basic events, but the failure data set will have four basic events, where     BE2 is spurious.    three basic events        - n: The number of samples from the Monte Carlo simulation.        - fp: the failure probability assigned for all the basic events.    The function  genFailureDataSet outputs the variable "data", which correspondsto the failure data set. And if the user provides a path in the variable save_folder,the variable 'data' is saved in a .mat file in the indicated path. This informationcan be used to input the FT-MOEA@author: Lisandro A. Jimenez Roa"""import numpy as npfrom ft_moea import str2ft, table_to_input_ft, savematdef genFailureDataSet(fts_string,n,fp):    #%% Generate failure data via de Monte Calor Method    fti = str2ft(fts_string)        # Creating the statistcally independent dataset.    data = np.random.binomial(1, fp,int(n))    max_be = max([int(i[2:]) for i in fti.flattened_representation[1]])    for i in range(0,max_be-1):        data = np.vstack((data,np.random.binomial(1, fp,int(n))))    data = data.reshape((n,max_be))        _, dataset = table_to_input_ft(data)    T = []    for i in dataset:        if fti.valuate(i):            T.append(1)        else:            T.append(0)    #%%    MyList = np.vstack((data.T.tolist(),np.array(T))).T.tolist()    unique, counts = np.unique(np.array(MyList), axis=0, return_counts=True)    data = np.hstack((unique.reshape((len(counts),unique.shape[1])),counts.reshape((len(counts),1))))    return data#%% Input variables# Specify the path where the failure data set is going to be saved in a .mat file.save_folder = ''# Fault tree stringfts_string = 'AND(BE1,OR(BE3,BE4))'# Number of data points in your Monte Carlo simulationn = 250000 # Total number of data points.# Failure probability in the BEs (equal for all of them) fp = 0.2# Generate the failure data set:data = genFailureDataSet(fts_string,n,fp)#%% Save the dataset:if save_folder != '':    mdic = {'dataset': data}    savemat(save_folder + '.mat', mdic)