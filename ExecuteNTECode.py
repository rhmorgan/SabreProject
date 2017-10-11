# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 13:06:35 2017

@author: rhmorgan
"""

import Code.GetKey
import os.path
import Code.ProduceNTEFares
import Code.CreateMasterNTE

#Set your major parameters here
DepartureDateString = "2017-12-23"
ReturnDateString = "2018-01-07"
#filetoload = "\ResultFiles\import_file.csv"
filetoload = "\ResultFiles\import_file.csv"
number_itineraries = 200
CreateMonthlyNTEFileInd = "N" #If this is set to true it will produce 2 files (a business and a coach class file)
GenerateReverseInd = "Y" #This will get the reverse for the One way Fare. For example, if going to DCA to IND it will get IND to DCA.
DaysToTry = 5 #It will increment the date up to this many times if the code does not find a fare.
HoursBtwnMinFlight = 7 #Use will disregard itineraries that exceed the most direct route by this many hours 
#END PARAMETERS: DON'T touch anything after this point.





my_path = os.path.abspath(os.path.dirname(__file__))
datafile = my_path+filetoload
key = Code.GetKey.GetSabreKey()

filetoload = "\ResultFiles\CPaward2018.csv"
CpFile = my_path+filetoload

if CreateMonthlyNTEFileInd == "Y":
    #Create a file for Coach Class("Y")
    ServiceClass = "Y"
    Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass, GenerateReverseInd, DaysToTry, HoursBtwnMinFlight, CpFile)

    #Create a file for Business Class("C")
    ServiceClass = "C"
    Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass, GenerateReverseInd, DaysToTry, HoursBtwnMinFlight, CpFile)
else:
    #Create a file for Coach Class("Y")
    ServiceClass = "Y"
    Code.ProduceNTEFares.ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key,ServiceClass, GenerateReverseInd, DaysToTry, HoursBtwnMinFlight, CpFile)

#Add new entries to NTE Masterfile
Code.CreateMasterNTE.CreateMasterNTEList(NewDatafile=datafile, PathtoMasterNTEFile=my_path)
