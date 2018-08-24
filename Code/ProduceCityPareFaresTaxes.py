# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 22:16:59 2017

@author: Morgan_Win7
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May  5 08:52:40 2017

@author: rhmorgan
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:29:51 2017

@author: rhmorgan
"""


# coding: utf-8

# In[35]:
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 15:51:03 2017

@author: rhmorgan
"""

import json
import Code.SabreTaxAPICall
import os
import datetime
import pandas as pd
from bs4 import BeautifulSoup

def ProduceCityPareTaxFile(datafile, DepartureDateString, number_itineraries, key):

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
    requestData['OW Trip Begin Date'] = ""
    requestData['OW Fare'] =0
    requestData['OW Passenger Type']=""
    requestData['OW Fare Calc']=""
    requestData['OW Routing']=""
    requestData['OW Fare Basis']=""
    requestData['OW Total Tax']=""
    requestData['OW US1 Tax']=""
    requestData['OW Basefare']=""
    requestData['OW YCA Price']=""
    requestData['OW Tax String']=""

    requestData['RT Trip Begin Date'] = ""
    requestData['RT Return Date']=""
    requestData['RT Fare'] =0
    requestData['RT Passenger Type']=""
    requestData['RT Fare Calc']=""
    requestData['RT Routing']=""
    requestData['RT Fare Basis']=""
    requestData['RT Total Tax']=""
    requestData['RT US1 Tax']=""
    requestData['RT Basefare']=""
    requestData['RT YCA Price']=""
    requestData['RT Tax String']=""

    requestData['OW_R Trip Begin Date'] = ""
    requestData['OW_R Fare'] =0
    requestData['OW_R Passenger Type']=""
    requestData['OW_R Fare Calc']=""
    requestData['OW_R Routing']=""
    requestData['OW_R Fare Basis']=""
    requestData['OW_R Total Tax']=""
    requestData['OW_R US1 Tax']=""
    requestData['OW_R Basefare']=""
    requestData['OW_R YCA Price']=""
    requestData['OW_R Tax String']=""

    requestData['BC_OW Trip Begin Date'] = ""
    requestData['BC_OW Fare'] =0
    requestData['BC_OW Passenger Type']=""
    requestData['BC_OW Fare Calc']=""
    requestData['BC_OW Routing']=""
    requestData['BC_OW Fare Basis']=""
    requestData['BC_OW Total Tax']=""
    requestData['BC_OW US1 Tax']=""
    requestData['BC_OW Basefare']=""
    requestData['BC_OW YCA Price']=""
    requestData['BC_OW Tax String']=""

    requestData['BC_RT Trip Begin Date'] = ""
    requestData['BC_RT Return Date']=""
    requestData['BC_RT Fare'] =0
    requestData['BC_RT Passenger Type']=""
    requestData['BC_RT Fare Calc']=""
    requestData['BC_RT Routing']=""
    requestData['BC_RT Fare Basis']=""
    requestData['BC_RT Total Tax']=""
    requestData['BC_RT US1 Tax']=""
    requestData['BC_RT Basefare']=""
    requestData['BC_RT YCA Price']=""
    requestData['BC_RT Tax String']=""


    requestData['BC_OW_R Trip Begin Date'] = ""
    requestData['BC_OW_R Fare'] =0
    requestData['BC_OW_R Passenger Type']=""
    requestData['BC_OW_R Fare Calc']=""
    requestData['BC_OW_R Routing']=""
    requestData['BC_OW_R Fare Basis']=""
    requestData['BC_OW_R Total Tax']=""
    requestData['BC_OW_R US1 Tax']=""
    requestData['BC_OW_R Basefare']=""
    requestData['BC_OW_R YCA Price']=""
    requestData['BC_OW_R Tax String']=""

    if 'OW Raw Itinerary' not in requestData: 
        requestData['OW Raw Itinerary'] = ""
        requestData['OW Raw Itinerary']  = requestData['OW Raw Itinerary'].astype(object)
    if 'RT Raw Itinerary' not in requestData:
        requestData['RT Raw Itinerary'] = ""
        requestData['RT Raw Itinerary']  = requestData['RT Raw Itinerary'].astype(object)
    if 'OW_R Raw Itinerary' not in requestData: 
        requestData['OW_R Raw Itinerary'] = ""
        requestData['OW_R Raw Itinerary'] = requestData['OW_R Raw Itinerary'].astype(object)
    if 'BC_OW Raw Itinerary' not in requestData:
        requestData['BC_OW Raw Itinerary'] = ""
        requestData['BC_OW Raw Itinerary'] = requestData['BC_OW Raw Itinerary'].astype(object)
    if 'BC_RT Raw Itinerary' not in requestData: 
        requestData['BC_RT Raw Itinerary'] = ""
        requestData['BC_RT Raw Itinerary'] = requestData['BC_RT Raw Itinerary'].astype(object)
    if 'BC_OW_R Raw Itinerary' not in requestData: 
        requestData['BC_OW_R Raw Itinerary'] = ""
        requestData['BC_OW_R Raw Itinerary'] = requestData['BC_OW_R Raw Itinerary'].astype(object)
    

    for index, row in requestData.iterrows():
        
        DepartureDate = DepartureDateString
#        ReturnDate  = ReturnDateString

#Determine if it is a International Flight        
        if str(requestData['origin_country'][index]).strip() == 'USA' and str(requestData['destination_country'][index]).strip() == 'USA':
          InternationalInd = False
        else:
          InternationalInd = True

#Determine if need to calc business Class
        if requestData['business_fare'][index] > 0:
          BusinessInd = True
        else:
          BusinessInd = False

          
        if len(str(requestData.loc[[index], ['OW Raw Itinerary']]))<50:  
            apiResults = Code.SabreTaxAPICall.taxApiCall(us_airports, us_airlines, str(requestData['origin_airport'][index]), str(requestData['destination_airport'][index]), "OneWay", DepartureDate, number_itineraries, key, "Y", InternationalInd, requestData['yca_fare'][index])
            requestData.loc[[index], ['OW Raw Itinerary']]= str(apiResults)             

        if len(str(requestData.loc[[index], ['OW_R Raw Itinerary']]))<50:    
            apiResults = Code.SabreTaxAPICall.taxApiCall(us_airports, us_airlines, str(requestData['destination_airport'][index]), str(requestData['origin_airport'][index]), "OneWay", DepartureDate, number_itineraries, key, "Y", InternationalInd, requestData['yca_fare'][index])
            requestData.loc[[index], ['OW_R Raw Itinerary']]= str(apiResults)                        

        if InternationalInd == True:
            if len(str(requestData.loc[[index], ['RT Raw Itinerary']]))<50:
                apiResults = Code.SabreTaxAPICall.taxApiCall(us_airports, us_airlines, str(requestData['origin_airport'][index]), str(requestData['destination_airport'][index]), "RoundTrip", DepartureDate, number_itineraries, key, "Y", InternationalInd, requestData['yca_fare'][index])
                requestData.loc[[index], ['RT Raw Itinerary']]= str(apiResults)                        


#TURNED OFF AFTER DURA SAID Business Class must be lowest fair
#        if BusinessInd == True:
#            if len(str(requestData.loc[[index], ['BC_OW Raw Itinerary']]))<40:    
#                apiResults = Code.SabreTaxAPICall.taxApiCall(us_airports, us_airlines, str(requestData['origin_airport'][index]), str(requestData['destination_airport'][index]), "OneWay", DepartureDate, number_itineraries, key, "C", InternationalInd, requestData['business_fare'][index])
#                requestData.loc[[index], ['BC_OW Raw Itinerary']]= str(apiResults)             
    
#            if len(str(requestData.loc[[index], ['BC_RT Raw Itinerary']]))<40:    
#                apiResults = Code.SabreTaxAPICall.taxApiCall(us_airports, us_airlines, str(requestData['origin_airport'][index]), str(requestData['destination_airport'][index]), "RoundTrip", DepartureDate, number_itineraries, key, "C", InternationalInd, requestData['business_fare'][index])
#                requestData.loc[[index], ['BC_RT Raw Itinerary']]= str(apiResults)                        

#            if len(str(requestData.loc[[index], ['BC_OW_R Raw Itinerary']]))<40:        
#                apiResults = Code.SabreTaxAPICall.taxApiCall(us_airports, us_airlines, str(requestData['destination_airport'][index]), str(requestData['origin_airport'][index]), "OneWay", DepartureDate, number_itineraries, key, "C", InternationalInd, requestData['business_fare'][index])
#                requestData.loc[[index], ['BC_OW_R Raw Itinerary']]= str(apiResults)                        
            
        print('ORG:'+str(requestData['origin_airport'][index])+' DES:'+str(requestData['destination_airport'][index])+' '+str(((index+1)/len(requestData.index))*100)+'% Complete')


    #Export the raw itenerary table in case there is a problem
    file_name = str(datetime.datetime.now()).replace(":",".")+"-City_Tax_raw.csv"    
    file_path = os.path.join(script_dir, file_name)
    file_path = file_path.replace("Code", "ResultFiles") 
    requestData.to_csv(file_path, sep=',')
    
    flight_types = ['OW','RT', 'OW_R', 'BC_OW', 'BC_RT' , 'BC_OW_R']
    #Pull out the relavent ifnromation for one way fares an place it into appropriate columns        
    for index, row in requestData.iterrows():
        for flighttype in flight_types:
                if len(str(requestData[flighttype +' Raw Itinerary'][index])) > 3:
                    itinerary_soup = BeautifulSoup(str(requestData[flighttype +' Raw Itinerary'][index]), 'html.parser')
                    requestData.loc[index:index:,(flighttype +' Trip Begin Date')]= itinerary_soup .find('flightsegment'.lower())['departuredatetime']
                    requestData.loc[index:index:,(flighttype +' Fare')] = float(itinerary_soup.find('TotalFare'.lower(), decimalplaces=True)['amount'])
                    requestData.loc[index:index:,(flighttype +' Passenger Type')] = itinerary_soup.find('PassengerTypeQuantity'.lower())['code']
                    requestData.loc[index:index:,(flighttype +' Fare Calc')] = itinerary_soup.find('FareCalcLine'.lower())['info']
                    routing = ""
                    for elem in itinerary_soup.find_all('flightsegment'.lower()):
                        routing = routing + (elem.find('departureairport')['locationcode'] + '-' + elem.find('marketingairline')['code'] + elem['flightnumber'] +'|' 
                        + elem.find('operatingairline')['code'] + elem.find('operatingairline')['flightnumber'] +'(' + elem['resbookdesigcode'] +')-' +elem.find('arrivalairport')['locationcode'] + ' ')
                    requestData.loc[index:index:,(flighttype +' Routing')]=routing
                    fare_basis = ""
                    for elem in itinerary_soup.find_all('farebasiscode'.lower()):
                        fare_basis = fare_basis + (elem.string + '-')
                    requestData.loc[index:index:,(flighttype +' Fare Basis')]=fare_basis
            
                    requestData.loc[index:index:,(flighttype +' Total Tax')] = itinerary_soup.find('totaltax'.lower())['amount']
                    requestData.loc[index:index:,(flighttype +' Basefare')] = itinerary_soup.find('basefare'.lower())['amount']
            
                    if len(itinerary_soup.find_all('tax'.lower(), taxcode='US1'))>0:
                        requestData.loc[index:index:,(flighttype +' US1 Tax')] = itinerary_soup.find('tax'.lower(), taxcode='US1')['amount']
                        if len(itinerary_soup.find('tax'.lower(), taxcode='US1')['amount'])>1:
                            requestData.loc[index:index:,(flighttype +' YCA Price')] = float(itinerary_soup.find('basefare'.lower())['amount']) + float(itinerary_soup.find('tax'.lower(), taxcode='US1')['amount']) 
                        else:
                            requestData.loc[index:index:,(flighttype +' YCA Price')] = float(itinerary_soup.find('basefare'.lower())['amount']) 
                    taxes=""
                    for elem in itinerary_soup.find_all('tax'.lower()):
                        taxes = taxes + (elem['taxcode'] + '=' + elem['amount']  +'|')
                    requestData.loc[index:index:,(flighttype +' Tax String')] = taxes
    
    
    #Create the final version of the file    
    requestData.to_csv(file_path.replace("raw","final"), sep=',')
    
    print("end:" + str(datetime.datetime.now()))
    


#END OF FILE    