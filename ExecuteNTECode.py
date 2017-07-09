# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 13:06:35 2017

@author: rhmorgan
"""
#import sys
#sys.path.insert(0, 'C:/Users/rhmorgan/Desktop/Sabre/SabreProject/Credentials')

##import file
#import SabreCreditials
#import SabreProject
#import Credentials.SabreCredentials

import Code.GetKey
import pandas as pd
import os.path
import Code.ProduceNTEFares
import json



filetoload = "\ResultFiles\import_file.csv"
DepartureDateString = "2017-08-10"
ReturnDateString = "2017-08-17"
number_itineraries = 50
#Class


my_path = os.path.abspath(os.path.dirname(__file__))
#path = os.path.join(my_path, "../ResultFiles/import_file.csv")
datafile = my_path+filetoload
key = Code.GetKey.GetSabreKey()


#import os
#script_dir = os.path.dirname(__file__)
#file_path = os.path.join(my_path, 'Code/airports.json')
#print(file_path)
#with open(file_path, 'r') as json_data:
#    data = json.load(json_data)

#filetoload1 = "\Code\" + "airports.json"
#script_dir = my_path+filetoload1
#print(script_dir)
#file_path = os.path.join(script_dir, '\Code\airports.json')
#with open(script_dir, 'r') as json_data:
#    data = json.load(json_data)


#with open(my_path+'\Code\airports.json') as json_data:
#    data = json.load(json_data)

#Load List with just US airports
us_airports = []
country = 'US'
for sublist in data:
    if sublist['iso'] == country:
        us_airports.extend([sublist])


ServiceClass = "Y"
Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass)

ServiceClass = "C"
Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass)


#data1 = pd.read_csv(path)
#print(path)

#dir_path = os.path.dirname(os.path.realpath(__file__))
#dir_path2 = dir_path + 'ResultFiles\import_file.csv'
#dir_path3 = os.path.join(dir_path2)
#print(Credentials.SabreCredentials.Username)
#print(Code.GetKey.hirhodri())
#print(Code.GetKey.GetSabreKey())
#print(sys.path)
#datafile = os.path.join('/ResultFiles/import_file.csv')
#print(datafile)
#print