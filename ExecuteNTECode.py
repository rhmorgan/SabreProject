# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 13:06:35 2017

@author: rhmorgan
"""

import Code.GetKey
import os.path
import Code.ProduceNTEFares

#Set your major parameters here
DepartureDateString = "2017-08-12"
ReturnDateString = "2017-08-20"
filetoload = "\ResultFiles\import_file.csv"
number_itineraries = 200
CreateCoachAndBusiness = "N"


my_path = os.path.abspath(os.path.dirname(__file__))
datafile = my_path+filetoload
key = Code.GetKey.GetSabreKey()

if CreateCoachAndBusiness == "Y":
    #Create a file for Coach Class("Y")
    ServiceClass = "Y"
    Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass)

    #Create a file for Business Class("C")
    ServiceClass = "C"
    Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass)
else:
    #Create a file for Coach Class("Y")
    ServiceClass = "Y"
    Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass)
