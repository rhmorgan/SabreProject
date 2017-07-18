# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 15:51:03 2017

@author: rhmorgan
"""

import json
import Code.SabreAPICall
import os
import datetime
import pandas as pd
from bs4 import BeautifulSoup

def ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key, ServiceClass):

    #Load List with American Flagged Carriers
    us_airlines = []
    us_airlines = ['AS', 'AA','DL','F9','HA', 'B6','WN','NK','UA','VX','3M']

    #Load List with all of the worlds airports    
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'airports.json')
    with open(file_path, 'r') as json_data:
        data = json.load(json_data)
        
    #Load List with just US airports
    us_airports = []
    country = 'US'
    for sublist in data:
        if sublist['iso'] == country:
            us_airports.extend([sublist])


    print("start:" + str(datetime.datetime.now()))
    data1 = pd.read_csv(datafile)
    data1 =data1.dropna(axis=0, how='all')
    requestData = data1
    
    #Add any new columns to the file
    requestData['Service Class'] = ""    
    requestData['OW Trip Begin Date'] = ""
    requestData['OW Fare'] =0
    requestData['OW Passenger Type']=""
    requestData['OW Fare Calc']=""
    requestData['OW Routing']=""
    requestData['OW Fare Basis']=""
    requestData['RT Trip Begin Date'] = ""
    requestData['RT Return Date']=""
    requestData['RT Fare'] =0
    requestData['RT Passenger Type']=""
    requestData['RT Fare Calc']=""
    requestData['RT Routing']=""
    requestData['RT Fare Basis']=""
    requestData['OW Raw Itinerary'] = ""#requestData.apply(Code.SabreAPICall.apiCall(us_airports, us_airlines, "LON", "IAD", "OneWay", DepartureDateString, ReturnDateString, number_itineraries, key), axis=1)
    requestData['RT Raw Itinerary'] = ""#requestData.apply(Code.SabreAPICall.apiCall(us_airports, us_airlines, "LON", "IAD" , "RoundTrip", DepartureDateString, ReturnDateString, number_itineraries, key), axis=1)
    if 'u_depart_date' not in requestData.columns: requestData['u_depart_date'] = ""        
    if 'u_return_date' not in requestData.columns: requestData['u_return_date'] = ""        
    if 'u_business_class_indicator' not in requestData.columns: requestData['u_business_class_indicator'] = ""        
    
    #Use API to pull lowest price itenerary and load it into datatable
    requestData['OW Raw Itinerary']  = requestData['OW Raw Itinerary'].astype(object)
    requestData['RT Raw Itinerary']  = requestData['OW Raw Itinerary'].astype(object)
    for index, row in requestData.iterrows():
        
        #Code checks the format of the date
        strDepartDate = str(requestData['u_depart_date'][index])
        if len(strDepartDate)>3:
            if '/' in strDepartDate[-4:]:
                DepartureDate = pd.to_datetime(requestData['u_depart_date'][index], format='%m/%d/%y')
                DepartureDate = str(DepartureDate)[0:10]
            else:
                DepartureDate = pd.to_datetime(requestData['u_depart_date'][index], format='%m/%d/%Y')
                DepartureDate = str(DepartureDate)[0:10]
        else: DepartureDate = DepartureDateString

        #Code checks the format of the date
        strReturnDate = str(requestData['u_return_date'][index])
        if len(strReturnDate)>3:
            if '/' in strReturnDate[-4:]:
                ReturnDate  = pd.to_datetime(requestData['u_return_date'][index], format='%m/%d/%y')
                ReturnDate  = str(ReturnDate)[0:10]
            else:
                ReturnDate  = pd.to_datetime(requestData['u_return_date'][index], format='%m/%d/%Y')
                ReturnDate  = str(ReturnDate)[0:10]
        else: ReturnDate  = ReturnDateString
                    
        if len(str(requestData['u_business_class_indicator'][index]))!=3:
                if requestData['u_business_class_indicator'][index].upper() in ('BUSINESS', 'C'):
                    varServiceClass = "C"
                else: varServiceClass = "Y"
        else: varServiceClass = ServiceClass
        requestData.loc[[index], ['Service Class']]= varServiceClass


        apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Departure Airport Code'][index]), str(requestData['Destination Airport Code'][index]), "OneWay", DepartureDate, ReturnDate, number_itineraries, key, varServiceClass)
        #requestData['OW Raw Itinerary'][index] = apiResults 
        requestData.loc[[index], ['OW Raw Itinerary']]= str(apiResults)             
#        requestData.loc[index:index:,('OW Raw Itinerary')]=apiResults 
        apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Departure Airport Code'][index]), str(requestData['Destination Airport Code'][index]), "RoundTrip", DepartureDate, ReturnDate, number_itineraries, key, varServiceClass)
        #requestData['RT Raw Itinerary'][index] = apiResults 
        requestData.loc[[index], ['RT Raw Itinerary']]= str(apiResults)                        
        print('CLASS:'+varServiceClass+' ORG:'+str(requestData['Departure Airport Code'][index])+' DES:'+str(requestData['Destination Airport Code'][index])+' '+str(((index+1)/len(requestData.index))*100)+'% Complete')


    #Export the raw itenerary table in case there is a problem
    file_name = str(datetime.datetime.now()).replace(":",".")+"-"+ServiceClass+' Sabre_Tool_raw.csv'    
    file_path = os.path.join(script_dir, file_name)
    file_path = file_path.replace("Code", "ResultFiles") 
    requestData.to_csv(file_path, sep=',')
    

    #Pull out the relavent ifnromation for one way fares an place it into appropriate columns        
    for index, row in requestData.iterrows():
        if len(str(requestData['OW Raw Itinerary'][index])) > 2:
            itinerary_soup = BeautifulSoup(str(requestData['OW Raw Itinerary'][index]), 'html.parser')
            requestData.loc[index:index:,('OW Trip Begin Date')]= itinerary_soup .find('flightsegment'.lower())['departuredatetime']
            requestData.loc[index:index:,('OW Fare')] = float(itinerary_soup.find('TotalFare'.lower(), decimalplaces=True)['amount'])
            requestData.loc[index:index:,('OW Passenger Type')] = itinerary_soup.find('PassengerTypeQuantity'.lower())['code']
            requestData.loc[index:index:,('OW Fare Calc')] = itinerary_soup.find('FareCalcLine'.lower())['info']
            routing = ""
            for elem in itinerary_soup.find_all('flightsegment'.lower()):
                routing = routing + (elem.find('departureairport')['locationcode'] + '-' + elem.find('marketingairline')['code'] + elem['flightnumber'] +'|' 
                + elem.find('operatingairline')['code'] + elem.find('operatingairline')['flightnumber'] +'(' + elem['resbookdesigcode'] +')-' +elem.find('arrivalairport')['locationcode'] + ' ')
            requestData.loc[index:index:,('OW Routing')]=routing
            fare_basis = ""
            for elem in itinerary_soup.find_all('farebasiscode'.lower()):
                fare_basis = fare_basis + (elem.string + '-')
            requestData.loc[index:index:,('OW Fare Basis')]=fare_basis
    
    #Pull out the relavent ifnromation for round trip fares an place it into appropriate columns    
    for index, row in requestData.iterrows():
        if len(str(requestData['RT Raw Itinerary'][index])) > 2:
            itinerary_soup = BeautifulSoup(str(requestData['RT Raw Itinerary'][index]), 'html.parser')
            requestData.loc[index:index:,('RT Trip Begin Date')] = itinerary_soup .find('flightsegment'.lower())['departuredatetime']
            requestData.loc[index:index:,('RT Fare')] = float(itinerary_soup.find('TotalFare'.lower(), decimalplaces=True)['amount'])
            requestData.loc[index:index:,('RT Passenger Type')] = itinerary_soup.find('PassengerTypeQuantity'.lower())['code']
            requestData.loc[index:index:,('RT Fare Calc')] = itinerary_soup.find('FareCalcLine'.lower())['info']
            routing = ""
            for elem in itinerary_soup.find_all('flightsegment'.lower()):
                routing = routing + (elem.find('departureairport')['locationcode'] + '-' + elem.find('marketingairline')['code'] + elem['flightnumber'] +'|' 
                + elem.find('operatingairline')['code'] + elem.find('operatingairline')['flightnumber'] +'(' + elem['resbookdesigcode'] +')-' +elem.find('arrivalairport')['locationcode'] + ' ')
            requestData.loc[index:index:,('RT Routing')]=routing
            fare_basis = ""
            for elem in itinerary_soup.find_all('farebasiscode'.lower()):
                fare_basis = fare_basis + (elem.string + '-')
            requestData.loc[index:index:,('RT Fare Basis')]=fare_basis
    
    
    #Create the final version of the file    
    requestData.to_csv(file_path.replace("raw","final"), sep=',')
    
    print("end:" + str(datetime.datetime.now()))
    
