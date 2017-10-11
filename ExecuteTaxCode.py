# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 22:00:37 2017

@author: Morgan_Win7
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 13:06:35 2017

@author: rhmorgan
"""

import Code.GetKey
import os.path
import Code.ProduceCityPareFaresTaxes
#import Code.CreateMasterNTE

#Set your major parameters here
DepartureDateString = "2017-12-01"
#filetoload = "\ResultFiles\import_file.csv"
filetoload = "\ResultFiles\import_file-taxes.csv"
number_itineraries = 200
#CreateMonthlyNTEFile = "N" #If this is set to true it will produce 2 files (a business and a coach class file)


my_path = os.path.abspath(os.path.dirname(__file__))
datafile = my_path+filetoload
key = Code.GetKey.GetSabreKey()

Code.ProduceCityPareFaresTaxes.ProduceCityPareTaxFile(datafile, DepartureDateString,  number_itineraries, key)
