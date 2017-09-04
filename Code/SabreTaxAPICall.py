# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 08:54:14 2017

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
import json
#import datetime
from datetime import datetime  
from datetime import timedelta  
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup



def taxApiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, DepartureDate, number_itineraries, key, ServiceClass, InternationalInd, GOV_FARE):

    add_days_counter=1    
    api = apiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, DepartureDate, number_itineraries, key, ServiceClass, InternationalInd, GOV_FARE)

    while (len(api)==0 and add_days_counter<5):
        date_1 = datetime.strptime(DepartureDate, "%Y-%m-%d")
        a = str(date_1 + timedelta(days=add_days_counter))
        newDepartureDateString = a[0:10]       
        print(newDepartureDateString)
        api = apiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, newDepartureDateString, number_itineraries, key, ServiceClass, InternationalInd, GOV_FARE)
        add_days_counter=add_days_counter+1

    print(len(api))
    add_days_counter=1
    return api

  
#This code will make a call to Sabre to get flight information
def apiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, DepartureDate, number_itineraries, key, ServiceClass, InternationalInd, GOV_FARE):
#    number_itineraries = 50
    number_itineraries_text = '<RequestType Name="' + str(number_itineraries) + 'ITINS" />'
    startOriginString =  "<OriginLocation LocationCode="
    startDestString =  "<DestinationLocation LocationCode="
    endString = " />"
    quote ="'"
    OriginCity = origin_airport
    DestCity = destination_airport
    OriginString = startOriginString + quote + OriginCity + quote + endString
    DestString = startDestString + quote + DestCity + quote + endString
    ReturnOriginString = startOriginString + quote + DestCity + quote + endString
    ReturnDestString = startDestString + quote + OriginCity + quote + endString
    TripInd = OW_RT_Desc
    DepartureDateString = DepartureDate
    ReturnDateString = str(datetime.strptime(DepartureDate, "%Y-%m-%d") + timedelta(days=5))[0:10]
    number_itineraries = 200
    YCA_FARE = GOV_FARE
    url="https://webservices.havail.sabre.com"
    headers = {'content-type': 'text/xml'}
    ServiceClassTxt = quote + ServiceClass + quote
    
    
    if ServiceClass=='Y':
        faretype = 'YCA'
    else:
        faretype = 'DCB'
        


    try:
    #if origCode != "N/A":    
        if TripInd == "RoundTrip":
            requestBody = """<?xml version='1.0' encoding='UTF-8'?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                <SOAP-ENV:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" SOAP-ENV:mustUnderstand="0">
                        <eb:From>
                            <eb:PartyId eb:type="urn:x12.org:IO5:01">from</eb:PartyId>
                        </eb:From>
                        <eb:To>
                            <eb:PartyId eb:type="urn:x12.org:IO5:01">ws</eb:PartyId>
                        </eb:To>
                        <eb:CPAId>EL0I</eb:CPAId>
                        <eb:ConversationId>1234</eb:ConversationId>
                        <eb:Service eb:type="sabreXML"></eb:Service>
                        <eb:Action>BargainFinderMaxRQ</eb:Action>
                    </eb:MessageHeader> <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" SOAP-ENV:mustUnderstand="0">
                        <eb:BinarySecurityToken>""" + key + """</eb:BinarySecurityToken>
                    </eb:Security>
                </SOAP-ENV:Header>
                <SOAP-ENV:Body>
                  <OTA_AirLowFareSearchRQ xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Target="Production" Version="3.0.0" ResponseType="OTA" ResponseVersion="3.0.0">
                    <POS>
                        <Source PseudoCityCode="EL0I" ISOCurrency="USD">
                        <RequestorID ID="1" Type="1">
                            <CompanyName Code="TN" />
                        </RequestorID>
                        </Source>
                    </POS>
                    <OriginDestinationInformation RPH="1">
                        <DepartureDateTime>""" + DepartureDateString + """T11:00:00</DepartureDateTime>
                        """ + OriginString + """
                        """ + DestString + """
                        <TPA_Extensions>
                            <SegmentType Code="O" />
                        </TPA_Extensions>
                    </OriginDestinationInformation>
                    <OriginDestinationInformation RPH="2">
                        <DepartureDateTime>""" + ReturnDateString + """T11:00:00</DepartureDateTime>
                        """ + ReturnOriginString + """
                        """ + ReturnDestString + """
                        <TPA_Extensions>
                            <SegmentType Code="O" />
                        </TPA_Extensions>
                    </OriginDestinationInformation>
                    <TravelPreferences ValidInterlineTicket="true">
                        <CabinPref PreferLevel="Preferred" Cabin=""" + ServiceClassTxt + """ />
                        <TPA_Extensions>
                            <TripType Value="Return" />
                            <LongConnectTime Min="780" Max="1200" Enable="true" />
                            <ExcludeCallDirectCarriers Enabled="true" />
                            <FlexibleFares>
                                <FareParameters>
                                    <RefundPenalty Ind="false"/>
                                </FareParameters>
                            </FlexibleFares>
                        </TPA_Extensions>
                    </TravelPreferences>
                    <TravelerInfoSummary>
                        <SeatsRequested>1</SeatsRequested>
                        <AirTravelerAvail>
                            <PassengerTypeQuantity Code="GV1" Quantity="1" />
                        </AirTravelerAvail>
                        <PriceRequestInformation CurrencyCode="USD">
                            <TPA_Extensions>
                                <Indicators>
                                    <RefundPenalty Ind="false"/>
                                </Indicators>
                            </TPA_Extensions>
                        </PriceRequestInformation>
                    </TravelerInfoSummary>
                    <TPA_Extensions>
                        <IntelliSellTransaction>
                            """ + number_itineraries_text + """
                        </IntelliSellTransaction>
                    </TPA_Extensions>
                </OTA_AirLowFareSearchRQ>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
        elif TripInd == "OneWay":
            requestBody = """<?xml version='1.0' encoding='UTF-8'?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                <SOAP-ENV:Header>
                    <eb:MessageHeader xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" SOAP-ENV:mustUnderstand="0">
                        <eb:From>
                            <eb:PartyId eb:type="urn:x12.org:IO5:01">from</eb:PartyId>
                        </eb:From>
                        <eb:To>
                            <eb:PartyId eb:type="urn:x12.org:IO5:01">ws</eb:PartyId>
                        </eb:To>
                        <eb:CPAId>EL0I</eb:CPAId>
                        <eb:ConversationId>1234</eb:ConversationId>
                        <eb:Service eb:type="sabreXML"></eb:Service>
                        <eb:Action>BargainFinderMaxRQ</eb:Action>
                    </eb:MessageHeader> <eb:Security xmlns:eb="http://schemas.xmlsoap.org/ws/2002/12/secext" SOAP-ENV:mustUnderstand="0">
                        <eb:BinarySecurityToken>""" + key + """</eb:BinarySecurityToken>
                    </eb:Security>
                </SOAP-ENV:Header>
                <SOAP-ENV:Body>
                  <OTA_AirLowFareSearchRQ xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Target="Production" Version="3.0.0" ResponseType="OTA" ResponseVersion="3.0.0">
                    <POS>
                        <Source PseudoCityCode="EL0I" ISOCurrency="USD">
                        <RequestorID ID="1" Type="1">
                            <CompanyName Code="TN" />
                        </RequestorID>
                        </Source>
                    </POS>
                    <OriginDestinationInformation RPH="1">
                        <DepartureDateTime>""" + DepartureDateString + """T11:00:00</DepartureDateTime>
                        """ + OriginString + """
                        """ + DestString + """
                        <TPA_Extensions>
                            <SegmentType Code="O" />                            
                        </TPA_Extensions>
                    </OriginDestinationInformation>
                    <TravelPreferences ValidInterlineTicket="true">
                        <CabinPref PreferLevel="Preferred" Cabin=""" + ServiceClassTxt + """ />
                        <TPA_Extensions>
                            <TripType Value="Return" />
                            <LongConnectTime Min="780" Max="1200" Enable="true" />
                            <ExcludeCallDirectCarriers Enabled="true" />
                            <FlexibleFares>
                                <FareParameters>
                                    <RefundPenalty Ind="false"/>
                                </FareParameters>
                            </FlexibleFares>
                        </TPA_Extensions>
                    </TravelPreferences>
                    <TravelerInfoSummary>
                        <SeatsRequested>1</SeatsRequested>
                        <AirTravelerAvail>
                            <PassengerTypeQuantity Code="GV1" Quantity="1" />
                        </AirTravelerAvail>
                        <PriceRequestInformation CurrencyCode="USD">
                            <TPA_Extensions>
                                <Indicators>
                                    <RefundPenalty Ind="false"/>
                                </Indicators>

                            </TPA_Extensions>
                        </PriceRequestInformation>
                    </TravelerInfoSummary>
                    <TPA_Extensions>
                        <IntelliSellTransaction>
                            """ + number_itineraries_text + """
                        </IntelliSellTransaction>
                    </TPA_Extensions>
                    </OTA_AirLowFareSearchRQ>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""            


        answer = requests.post(url,data=requestBody,headers=headers)

        all_itineraries = answer.content
        all_itineraries_soup = BeautifulSoup(all_itineraries, 'html.parser')

        #Go through each returned itinerary and only include those that use an US Flagged Carrier if they are flighting to/from US
        itinerary_sequences_dict = {}
#        print(len(all_itineraries_soup.find_all('PricedItinerary'.lower())))
        for elem in all_itineraries_soup.find_all('PricedItinerary'.lower()):    
            #Get the price for each itinerary
            for price in elem.find_all('TotalFare'.lower(), decimalplaces=True):
                itinerary_sequences_dict[elem['sequencenumber']] = float(price['amount'])    

            for farebasis in elem.find_all('farebasiscode'.lower()):
                if (
                    farebasis.string != faretype 
                    ): 
                    #remove itineraries that don't meet criteria    
                    itinerary_sequences_dict.pop(elem['sequencenumber'], None)


            if InternationalInd == False:
                if len(elem.find_all('tax'.lower(), taxcode='US1'))>0:
                    calc_yca_amount = (float(elem.find('basefare'.lower())['amount']) + float(elem.find('tax'.lower(), taxcode='US1')['amount']))
                    if -1 <= (float(YCA_FARE)-calc_yca_amount) < 1:
#                        print("pass1")
#                        print(elem)
                        pass
                    else:
                        itinerary_sequences_dict.pop(elem['sequencenumber'], None)
                else:
                    print("see you")
                    itinerary_sequences_dict.pop(elem['sequencenumber'], None)
    
            else:
                if len(elem.find_all('basefare'.lower()))>0:
                    if TripInd == "RoundTrip":
                        calc_yca_amount = (float(elem.find('basefare'.lower())['amount']))/2
                        if -1 <= (float(YCA_FARE)-calc_yca_amount) < 1:
                            print("pass2")
                            pass
                        else:
                            itinerary_sequences_dict.pop(elem['sequencenumber'], None)
                    else:
                        calc_yca_amount = (float(elem.find('basefare'.lower())['amount']))
                        if -1 <= (float(YCA_FARE)-calc_yca_amount) < 1:
                            print("pass3")
                            pass
                        else:
                            itinerary_sequences_dict.pop(elem['sequencenumber'], None)


        #Determine the lowest cost itinerary
        if len(itinerary_sequences_dict)>0:
            lowest_priced_sequence_key = min(itinerary_sequences_dict, key=itinerary_sequences_dict.get) 
            print(lowest_priced_sequence_key)
        else:
            lowest_priced_sequence_key=0
        #Select the lowest price itinerary            
        lowest_priced_itinerary = all_itineraries_soup.find_all('PricedItinerary'.lower(), sequencenumber=lowest_priced_sequence_key)            
        return lowest_priced_itinerary 
        
    except:
        try:
            print('Not working1')
        except:
#            print(origCode + " | " + destCode + " | " + ReturnOriginString + " | " + ReturnDestString + " | " + TripInd)
            print('Not working2')
        return "N/A"
