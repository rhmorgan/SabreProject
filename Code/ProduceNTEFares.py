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

    #Load List with all of the worlds airports    
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'airports.json')
    print(file_path)
    with open(file_path, 'r') as json_data:
        data = json.load(json_data)
        
    #Load List with just US airports
    us_airports = []
    country = 'US'
    for sublist in data:
        if sublist['iso'] == country:
            us_airports.extend([sublist])

    #Load List with American Flagged Carriers
    us_airlines = []
    us_airlines = ['AS', 'AA','DL','F9','HA', 'B6','WN','NK','UA','VX','3M']



    print("start:" + str(datetime.datetime.now()))
    data1 = pd.read_csv(datafile)
    requestData = data1

    requestData['OW Raw Itinerary'] = ""#requestData.apply(Code.SabreAPICall.apiCall(us_airports, us_airlines, "LON", "IAD", "OneWay", DepartureDateString, ReturnDateString, number_itineraries, key), axis=1)
    requestData['RT Raw Itinerary'] = ""#requestData.apply(Code.SabreAPICall.apiCall(us_airports, us_airlines, "LON", "IAD" , "RoundTrip", DepartureDateString, ReturnDateString, number_itineraries, key), axis=1)
    requestData['OW Trip Begin Date'] = ""
    requestData['OW Fare'] =0
    requestData['OW Passenger Type']=""
    requestData['OW Fare Calc']=""
    requestData['OW Routing']=""
    requestData['OW Fare Basis']=""
    requestData['RT Trip Begin Date'] = ""
    requestData['RT Fare'] =0
    requestData['RT Passenger Type']=""
    requestData['RT Fare Calc']=""
    requestData['RT Routing']=""
    requestData['RT Fare Basis']=""
    
    requestData['OW Raw Itinerary']  = requestData['OW Raw Itinerary'].astype(object)
    requestData['RT Raw Itinerary']  = requestData['OW Raw Itinerary'].astype(object)
    for index, row in requestData.iterrows():
        apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Departure Airport Code'][index]), str(requestData['Destination Airport Code'][index]), "OneWay", DepartureDateString, ReturnDateString, number_itineraries, key, ServiceClass)
        requestData['OW Raw Itinerary'][index] = apiResults 
        apiResults = Code.SabreAPICall.apiCall(us_airports, us_airlines, str(requestData['Departure Airport Code'][index]), str(requestData['Destination Airport Code'][index]), "RoundTrip", DepartureDateString, ReturnDateString, number_itineraries, key, ServiceClass)
        requestData['RT Raw Itinerary'][index] = apiResults 
        print('CLASS:'+ServiceClass+' ORG:'+str(requestData['Departure Airport Code'][index])+' DES:'+str(requestData['Destination Airport Code'][index])+' '+str(((index+1)/len(requestData.index))*100)+'% Complete')

#        requestData.loc[index:index:,('OW Raw Itinerary')]= apiResults 


    file_name = str(datetime.datetime.now()).replace(":",".")+"-"+ServiceClass+' Sabre_Tool_raw.csv'    
    file_path = os.path.join(script_dir, file_name)
#    requestData.to_csv("C:/Users/rhmorgan/Desktop/Sabre/Sabre_Tool_raw.csv", sep=',')
    file_path = file_path.replace("Code", "ResultFiles") 
    requestData.to_csv(file_path, sep=',')
    
    
    print("checkpoint 1-"+ str(datetime.datetime.now()))
    
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
    
    print("checkpoint 2-"+ str(datetime.datetime.now()))
    
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
    
    print("checkpoint 3-"+ str(datetime.datetime.now()))
            #print(row['Departure Airport Code'], row['Destination Airport Code'])
    
    header = [
    'Departure Airport Code',
    'Dep City',
    'Dep State',
    'Dep Country',
    'Destination Airport Code',
    'Destination City',
    'Destination State',
    'Destination Country',
    'Airline',
    'One Way',
    'Roundtrip',
    'Business Class Leg',
    'Business One Way',
    'Business Rountrip',
    'Business Airline',
    'Business Leg Connection 1',
    'Business Leg Connection 2',
    'Split Tickets',
    'Connection',
    'Fares Used',
    'Comments / MAY 13-20',
    'IN/OUT',
    'COMMENTS',
    'OW Trip Begin Date',
    'OW Fare',
    'OW Passenger Type',
    'OW Fare Calc',
    'OW Routing',
    'OW Fare Basis',
    'RT Trip Begin Date',
    'RT Fare',
    'RT Passenger Type',
    'RT Fare Calc',
    'RT Routing',
    'RT Fare Basis'
    ]
    
    print("checkpoint 4-"+ str(datetime.datetime.now()))
    
    
    #df.to_csv('output.csv', columns = header)
    
    #requestData
#    requestData.to_csv("C:/Users/rhmorgan/Desktop/Sabre/Sabre_Tool_Output3.csv", sep=',', columns = header)
    requestData.to_csv(file_path.replace("raw","final"), sep=',')
    print("checkpoint 5"+ str(datetime.datetime.now()))
    
    print("end:" + str(datetime.datetime.now()))
    
