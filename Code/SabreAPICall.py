# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:29:51 2017

@author: rhmorgan
"""


# coding: utf-8

# In[35]:
import requests
from bs4 import BeautifulSoup
from datetime import datetime  
from datetime import timedelta  



#Function to determine if an airport is within the US
def us_airport_check(us_airports, airport):
    return any(e['iata'] == airport for e in us_airports)   


def apiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, DepartureDate, ReturnDateString, number_itineraries, key, ServiceClass, DaysToTry, HoursBtwnMinFlight):
    add_days_counter=1    
    api = SabreApiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, DepartureDate, ReturnDateString, number_itineraries, key, ServiceClass, HoursBtwnMinFlight)

    while (len(api)==0 and add_days_counter<DaysToTry):
        date_1 = datetime.strptime(DepartureDate, "%Y-%m-%d")
        a = str(date_1 + timedelta(days=add_days_counter))
        newDepartureDateString = a[0:10]       
        print(newDepartureDateString)
        date_1 = datetime.strptime(ReturnDateString, "%Y-%m-%d")
        a = str(date_1 + timedelta(days=add_days_counter))
        newReturnDateString = a[0:10]       

        api = SabreApiCall(us_airports, us_airlines, origin_airport, destination_airport, OW_RT_Desc, newDepartureDateString, newReturnDateString, number_itineraries, key, ServiceClass, HoursBtwnMinFlight)
        add_days_counter=add_days_counter+1

    print(len(api))
    add_days_counter=1
    return api



#This code will make a call to Sabre to get flight information
def SabreApiCall(us_airports, us_airlines, OriginCity, DestCity, TripInd, DepartureDateString, ReturnDateString, number_itineraries, key, ServiceClass, HoursBtwnMinFlight):

    startOriginString =  "<OriginLocation LocationCode="
    startDestString =  "<DestinationLocation LocationCode="
    endString = " />"
    quote ="'"
    ServiceClass = quote + ServiceClass + quote
    origCode = startOriginString + quote + OriginCity + quote + endString
    destCode = startDestString + quote + DestCity + quote + endString
    ReturnOriginString = startOriginString + quote + DestCity + quote + endString
    ReturnDestString = startDestString + quote + OriginCity + quote + endString
    number_itineraries_text = '<RequestType Name="' + str(number_itineraries) + 'ITINS" />'

    vendorPref = ""

    vendorExcl = """
                <ExcludeVendorPref Code="SU"/>
                <ExcludeVendorPref Code="FG"/>
               <ExcludeVendorPref Code="RQ"/>
               <ExcludeVendorPref Code="4Q"/>
               <ExcludeVendorPref Code="VA"/>
               <ExcludeVendorPref Code="HG"/>
               <ExcludeVendorPref Code="5Q"/>
               <ExcludeVendorPref Code="BG"/>
               <ExcludeVendorPref Code="Z5"/>
               <ExcludeVendorPref Code="4H"/>
               <ExcludeVendorPref Code="MY"/>
               <ExcludeVendorPref Code="PM"/>
               <ExcludeVendorPref Code="VU"/>
               <ExcludeVendorPref Code="9H"/>
               <ExcludeVendorPref Code="7I"/>
               <ExcludeVendorPref Code="EO"/>
               <ExcludeVendorPref Code="Q8"/>
               <ExcludeVendorPref Code="4U"/>
               <ExcludeVendorPref Code="O4"/>
               <ExcludeVendorPref Code="P4"/>
               <ExcludeVendorPref Code="GA"/>
               <ExcludeVendorPref Code="RI"/>
               <ExcludeVendorPref Code="MZ"/>
               <ExcludeVendorPref Code="6D"/>
               <ExcludeVendorPref Code="SJ"/>
               <ExcludeVendorPref Code="IZ"/>
               <ExcludeVendorPref Code="LY"/>
               <ExcludeVendorPref Code="6H"/>
               <ExcludeVendorPref Code="J0"/>
               <ExcludeVendorPref Code="2U"/>
               <ExcludeVendorPref Code="MD"/>
               <ExcludeVendorPref Code="ON"/>
               <ExcludeVendorPref Code="W8"/>
               <ExcludeVendorPref Code="PK"/>
               <ExcludeVendorPref Code="5J"/>
               <ExcludeVendorPref Code="PR"/>
               <ExcludeVendorPref Code="JU"/>
               <ExcludeVendorPref Code="WM"/>
               <ExcludeVendorPref Code="TG"/>
               <ExcludeVendorPref Code="VV"/>
               <ExcludeVendorPref Code="3N"/>
               <ExcludeVendorPref Code="Z6"/>
               <ExcludeVendorPref Code="7D"/>
               <ExcludeVendorPref Code="5V"/>
               <ExcludeVendorPref Code="M9"/>
               <ExcludeVendorPref Code="YG"/>
               <ExcludeVendorPref Code="6Z"/>
               <ExcludeVendorPref Code="PS"/>
               <ExcludeVendorPref Code="UT"/>
               <ExcludeVendorPref Code="7W"/>
               <ExcludeVendorPref Code="WU"/>
               <ExcludeVendorPref Code="QD"/>
               <ExcludeVendorPref Code="IY"/>
               <ExcludeVendorPref Code="UM"/>
                """ 

    try:
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
                        """ + origCode + """
                        """ + destCode + """
                        <TPA_Extensions>
                            <SegmentType Code="O" />
                            """ + vendorPref + """
                        </TPA_Extensions>
                    </OriginDestinationInformation>
                    <OriginDestinationInformation RPH="2">
                        <DepartureDateTime>""" + ReturnDateString + """T11:00:00</DepartureDateTime>
                        """ + ReturnOriginString + """
                        """ + ReturnDestString + """
                        <TPA_Extensions>
                            <SegmentType Code="O" />
                            """ + vendorPref + """
                        </TPA_Extensions>
                    </OriginDestinationInformation>
                    <TravelPreferences ValidInterlineTicket="true">
                        <CabinPref PreferLevel="Preferred" Cabin=""" + ServiceClass + """ />
                        <TPA_Extensions>
                            """ + vendorExcl + """
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
                        """ + origCode + """
                        """ + destCode + """
                        <TPA_Extensions>
                            <SegmentType Code="O" />
                            """ + vendorPref + """                            
                        </TPA_Extensions>
                    </OriginDestinationInformation>
                    <TravelPreferences ValidInterlineTicket="true">
                        <CabinPref PreferLevel="Preferred" Cabin= """ + ServiceClass + """ />
                        <TPA_Extensions>
                            """ + vendorExcl + """
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

        url="https://webservices.havail.sabre.com"
        headers = {'content-type': 'text/xml'}
        answer = requests.post(url,data=requestBody,headers=headers)

        all_itineraries = answer.content
        all_itineraries_soup = BeautifulSoup(all_itineraries, 'html.parser')

        #Go through each returned itinerary and only include those that use an US Flagged Carrier if they are flighting to/from US
        itinerary_sequences_dict = {}
        for elem in all_itineraries_soup.find_all('PricedItinerary'.lower()):    
            #Get the price for each itinerary
            for price in elem.find_all('TotalFare'.lower(), decimalplaces=True):
                itinerary_sequences_dict[elem['sequencenumber']] = {"amount": float(price['amount'])}    
#                itinerary_sequences_dict[elem['sequencenumber']] = float(price['amount'])    
            #Determine if flight goes to/from US and if it is using a US carrier. If not pull it out of itineraries to review

#            for rtime in elem.find_all('airitinerary'.lower(), directionind="Return"):
#                print(rtime.find('origindestinationoption')['elapsedtime'])
                
            elapsedtimes = elem.find_all('origindestinationoption'.lower())
            
            if len(elapsedtimes) > 1:
                itinerary_sequences_dict[elem['sequencenumber']]['et_outbound']=int(elapsedtimes[0]['elapsedtime']) 
                itinerary_sequences_dict[elem['sequencenumber']]['et_return']=int(elapsedtimes[1]['elapsedtime']) 
            else:
                itinerary_sequences_dict[elem['sequencenumber']]['et_outbound']=int(elapsedtimes[0]['elapsedtime']) 


            for flight in elem.find_all('FlightSegment'.lower()):
                if (
                    ((us_airport_check(us_airports, flight.find('arrivalairport')['locationcode']) == True) or
                     (us_airport_check(us_airports, flight.find('departureairport')['locationcode']) == True))
                     and ((flight.find('marketingairline')['code'] in us_airlines) == False)
                    ): 
                    #remove itineraries that don't meet criteria    
                    itinerary_sequences_dict.pop(elem['sequencenumber'], None)

        #Remove Flights With Excessive Times (Outbound Flight)
        if len(itinerary_sequences_dict)>0:
            min_itin_time = min(itinerary_sequences_dict, key=lambda x: itinerary_sequences_dict[x]['et_outbound'])
            min_time = itinerary_sequences_dict[min_itin_time]['et_outbound']
            
            for itin in list(itinerary_sequences_dict):
                if (itinerary_sequences_dict[itin]['et_outbound'] -min_time) > (HoursBtwnMinFlight*60):
                    itinerary_sequences_dict.pop(itin, None)

        #Remove Flights With Excessive Times (Return Flight)
        if TripInd == "RoundTrip" and len(itinerary_sequences_dict)>0: 
            min_itin_time = min(itinerary_sequences_dict, key=lambda x: itinerary_sequences_dict[x]['et_return'])
            min_time = itinerary_sequences_dict[min_itin_time]['et_return']
            
            for itin in list(itinerary_sequences_dict):
                if (itinerary_sequences_dict[itin]['et_return'] -min_time) > (HoursBtwnMinFlight*60):
                    itinerary_sequences_dict.pop(itin, None)

        #Determine the lowest cost itinerary
        if len(itinerary_sequences_dict)>0:
            lowest_priced_sequence_key = min(itinerary_sequences_dict, key=lambda x: itinerary_sequences_dict[x]['amount'])
#            lowest_priced_sequence_key = min(itinerary_sequences_dict, key=itinerary_sequences_dict.get) 
        else:
            lowest_priced_sequence_key=0
        #Select the lowest price itinerary            
        lowest_priced_itinerary = all_itineraries_soup.find_all('PricedItinerary'.lower(), sequencenumber=lowest_priced_sequence_key)            
        return lowest_priced_itinerary 
        
    except:
        try:
            print("Tried:Error")
            #print(all_itineraries)
        except:
            print("Except:Error")
            #print(lowest_priced_itinerary)
        return "[]"

