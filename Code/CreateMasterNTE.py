# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 06:46:54 2017

@author: rhmorgan
"""
import pandas as pd
import datetime

def CreateMasterNTEList(NewDatafile, PathtoMasterNTEFile):    
    #Identify Any airports to exclude from listing.    
    ExcludeAirport = ['BWU', 'ISM', 'ILG', 'PFN', 'OFR', 'CIA', 'SDV']
    #print(data1[data1['Destination Airport Code'].isin(ExcludeAirport)==False])

    #Open Master NTEFile file
    NTEFileName = "\ResultFiles\MasterNTEFile"
    
    NTEFilePath = PathtoMasterNTEFile+NTEFileName+'.csv'
    NTEFileBKName = NTEFileName+'-BK-'+str(datetime.datetime.now()).replace(":",".")        
    NTEFileBKPath = NTEFilePath.replace(NTEFileName,NTEFileBKName) 
    print(NTEFilePath)
    
    MasterNTEFile = pd.read_csv(NTEFilePath)    
    MasterNTEFile = MasterNTEFile.dropna(axis=0, how='all') 
    
    NewDataFile = pd.read_csv(NewDatafile)    
    NewDataFile = NewDataFile.dropna(axis=0, how='all')
    
    #Create Backup
    MasterNTEFile.to_csv(NTEFileBKPath, sep=',')
    
    #AppendAllRows
    rowcnt = len(MasterNTEFile.index)+1
    
    #Add rows from newfile    
    for index, row in NewDataFile .iterrows():
        MasterNTEFile.loc[rowcnt, ['Destination Airport Code', 'Departure Airport Code']] = [row['Destination Airport Code'],row['Departure Airport Code']]
        rowcnt=rowcnt+1

    MasterNTEFile['SortList']=""
    #Create list for each Departure/Destination combo and sort. This will get unique combos either way they are entered
    for index, row in MasterNTEFile.iterrows():
        MasterNTEFile['SortList'][index] = [
            MasterNTEFile['Destination Airport Code'][index], MasterNTEFile['Departure Airport Code'][index]
            ]
        MasterNTEFile['SortList'][index].sort()    
    
        #Break out dest and arrival
        MasterNTEFile.loc[[index], ['Departure Airport Code']] = MasterNTEFile['SortList'][index][0]    
        MasterNTEFile.loc[[index], ['Destination Airport Code']] = MasterNTEFile['SortList'][index][1]    
        if len(str(MasterNTEFile['Create_Date'][index]))<4: MasterNTEFile.loc[[index], ['Create_Date']] = "|"+str(datetime.datetime.now())    
    
    #Remove duplicates
    MasterNTEFile.drop_duplicates(['Departure Airport Code','Destination Airport Code'], keep='first', inplace=True)

    #Remove Excluded Airports
    MasterNTEFile = MasterNTEFile[MasterNTEFile['Destination Airport Code'].isin(ExcludeAirport)==False]
    MasterNTEFile = MasterNTEFile[MasterNTEFile['Departure Airport Code'].isin(ExcludeAirport)==False]
        
    #Create the final version of the file    
    header = ['Departure Airport Code', 'Destination Airport Code', 'Create_Date', 'Comments']
    MasterNTEFile.to_csv(NTEFilePath, sep= ',', columns=header )    