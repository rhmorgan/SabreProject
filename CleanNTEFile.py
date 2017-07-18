# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 06:46:54 2017
This code is used to add entries to the NTE file and remove any duplicates

@author: rhmorgan
"""

import os.path
import Code.CreateMasterNTE

#Enter the file you want to combine here
filetoload = "\ResultFiles\import_file.csv"

my_path = os.path.abspath(os.path.dirname(__file__))
datafile = my_path+filetoload

Code.CreateMasterNTE.CreateMasterNTEList(NewDatafile=datafile, PathtoMasterNTEFile=my_path)
