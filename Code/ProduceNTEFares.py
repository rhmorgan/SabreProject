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


def city_pair_check(dataset, origin, destination):
    if len(
            dataset[((dataset.ORIGIN_AIRPORT_ABBREV==origin) & (dataset.DESTINATION_AIRPORT_ABBREV==destination)) |
                  ((dataset.ORIGIN_AIRPORT_ABBREV==destination) & (dataset.DESTINATION_AIRPORT_ABBREV==origin))  
                 ]
        ) > 0:
        return "Warning: GSA City Pair"



def ProduceNTEFile(datafile, DepartureDateString, ReturnDateString, number_itineraries, key, ServiceClass, GenerateReverseInd, DaysToTry, HoursBtwnMinFlight, CpFile):

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
    CpData = pd.read_csv(CpFile)
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
    requestData['Warnings']=""


    if 'OW Raw Itinerary' not in requestData.columns:
        requestData['OW Raw Itinerary'] = ""
        requestData['OW Raw Itinerary']  = requestData['OW Raw Itinerary'].astype(object)
    if 'RT Raw Itinerary' not in requestData.columns:
        requestData['RT Raw Itinerary'] = ""
        requestData['RT Raw Itinerary']  = requestData['RT Raw Itinerary'].astype(object)
    if 'u_depart_date' not in requestData.columns: requestData['u_depart_date'] = ""        
    if 'u_return_date' not in requestData.columns: requestData['u_return_date'] = ""        
    if 'u_business_class_indicator' not in requestData.columns: requestData['u_business_class_indicator'] = ""        

    if GenerateReverseInd == "Y":
        requestData['OW_R Trip Begin Date'] = ""
        requestData['OW_R Return Date']=""
        requestData['OW_R Fare'] =0
        requestData['OW_R Passenger Type']=""
        requestData['OW_R Fare Calc']=""
        requestData['OW_R Routing']=""
        requestData['OW_R Fare Basis']=""
        if 'OW_R Raw Itinerary' not in requestData.columns:
            requestData['OW_R Raw Itinerary'] = ""
            requestData['OW_R Raw Itinerary']  = requestData['OW_R Raw Itinerary'].astype(object)
                                                                                                                                                          
    #Use API to pull lowest price itenerary and load it into datatable

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
                    
        if len(str(requestData['u_business_class_indicator'][index]))>0:
                if requestData['u_business_class_indicator'][index].upper() in ('BUSINESS', 'C'):
                    varServiceClass = "C"
                else: varServiceClass = "Y"
        else: varServiceClass = ServiceClass
        requestData.loc[[index], ['Service Class']]= varServiceClass


        if len(str(requestData.loc[[index], ['OW Raw Itinerary']]))<50:  
            apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Departure Airport Code'][index]), str(requestData['Destination Airport Code'][index]), "OneWay", DepartureDate, ReturnDate, number_itineraries, key, varServiceClass, DaysToTry, HoursBtwnMinFlight)
            requestData.loc[[index], ['OW Raw Itinerary']]= str(apiResults)             

        if len(str(requestData.loc[[index], ['RT Raw Itinerary']]))<50:  
            apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Departure Airport Code'][index]), str(requestData['Destination Airport Code'][index]), "RoundTrip", DepartureDate, ReturnDate, number_itineraries, key, varServiceClass, DaysToTry, HoursBtwnMinFlight)
            requestData.loc[[index], ['RT Raw Itinerary']]= str(apiResults)                        

        if GenerateReverseInd == "Y":
            if len(str(requestData.loc[[index], ['OW_R Raw Itinerary']]))<50:  
                apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Destination Airport Code'][index]), str(requestData['Departure Airport Code'][index]), "OneWay", DepartureDate, ReturnDate, number_itineraries, key, varServiceClass, DaysToTry, HoursBtwnMinFlight)
                requestData.loc[[index], ['OW_R Raw Itinerary']]= str(apiResults)                        

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
            requestData.loc[index:index:,('OW Trip Begin Date')]= itinerary_soup.find('flightsegment'.lower())['departuredatetime']
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
            requestData.loc[index:index:,('Warnings')]=city_pair_check(CpData, requestData['Departure Airport Code'][index], requestData['Destination Airport Code'][index])
    
    #Pull out the relavent ifnromation for round trip fares an place it into appropriate columns    
    for index, row in requestData.iterrows():
        if len(str(requestData['RT Raw Itinerary'][index])) > 2:
            itinerary_soup = BeautifulSoup(str(requestData['RT Raw Itinerary'][index]), 'html.parser')
            requestData.loc[index:index:,('RT Trip Begin Date')] = itinerary_soup.find('flightsegment'.lower())['departuredatetime']
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

    if GenerateReverseInd == "Y":
        for index, row in requestData.iterrows():
            if len(str(requestData['OW_R Raw Itinerary'][index])) > 2:
                itinerary_soup = BeautifulSoup(str(requestData['OW_R Raw Itinerary'][index]), 'html.parser')
                requestData.loc[index:index:,('OW_R Trip Begin Date')]= itinerary_soup.find('flightsegment'.lower())['departuredatetime']
                requestData.loc[index:index:,('OW_R Fare')] = float(itinerary_soup.find('TotalFare'.lower(), decimalplaces=True)['amount'])
                requestData.loc[index:index:,('OW_R Passenger Type')] = itinerary_soup.find('PassengerTypeQuantity'.lower())['code']
                requestData.loc[index:index:,('OW_R Fare Calc')] = itinerary_soup.find('FareCalcLine'.lower())['info']
                routing = ""
                for elem in itinerary_soup.find_all('flightsegment'.lower()):
                    routing = routing + (elem.find('departureairport')['locationcode'] + '-' + elem.find('marketingairline')['code'] + elem['flightnumber'] +'|' 
                    + elem.find('operatingairline')['code'] + elem.find('operatingairline')['flightnumber'] +'(' + elem['resbookdesigcode'] +')-' +elem.find('arrivalairport')['locationcode'] + ' ')
                requestData.loc[index:index:,('OW_R Routing')]=routing
                fare_basis = ""
                for elem in itinerary_soup.find_all('farebasiscode'.lower()):
                    fare_basis = fare_basis + (elem.string + '-')
                requestData.loc[index:index:,('OW_R Fare Basis')]=fare_basis
    
    
    #Create the final version of the file    
    requestData.to_csv(file_path.replace("raw","final"), sep=',')
    
    print("end:" + str(datetime.datetime.now()))
    
