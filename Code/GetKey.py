# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 14:05:59 2017

@author: rhmorgan
"""
import requests
from bs4 import BeautifulSoup
import Credentials.SabreCredentials


def GetSabreKey():
    url="https://webservices.havail.sabre.com"
    headers = {'content-type': 'text/xml'}
    openSession = """<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:eb="http://www.ebxml.org/namespaces/messageHeader" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsd="http://www.w3.org/1999/XMLSchema">
        <SOAP-ENV:Header>
            <eb:MessageHeader SOAP-ENV:mustUnderstand="1" eb:version="1.0">
                <eb:ConversationId>1234</eb:ConversationId>
                <eb:From>
                    <eb:PartyId type="urn:x12.org:IO5:01">999999</eb:PartyId>
                </eb:From>
                <eb:To>
                    <eb:PartyId type="urn:x12.org:IO5:01">123123</eb:PartyId>
                </eb:To>
                <eb:CPAId>EL0I</eb:CPAId>
                <eb:Service eb:type="OTA">SessionCreateRQ</eb:Service>
                <eb:Action>SessionCreateRQ</eb:Action>
                <eb:MessageData>
                    <eb:MessageId>1000</eb:MessageId>
                    <eb:Timestamp>2001-02-15T11:15:12Z</eb:Timestamp>
                    <eb:TimeToLive>2001-02-15T11:15:12Z</eb:TimeToLive>
                </eb:MessageData>
            </eb:MessageHeader>
            <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2002/12/secext" xmlns:wsu="http://schemas.xmlsoap.org/ws/2002/12/utility">
                <wsse:UsernameToken> 
                    <wsse:Username>""" + Credentials.SabreCredentials.Username + """</wsse:Username>
                    <wsse:Password>""" + Credentials.SabreCredentials.Password + """</wsse:Password>
                    <Organization>"""  + Credentials.SabreCredentials.Organization + """</Organization>
                    <Domain>DEFAULT</Domain> 
                </wsse:UsernameToken>
            </wsse:Security>
        </SOAP-ENV:Header>
        <SOAP-ENV:Body>
            <eb:Manifest SOAP-ENV:mustUnderstand="1" eb:version="1.0">
                <eb:Reference xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="cid:rootelement" xlink:type="simple"/>
            </eb:Manifest>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    """
    
    response = requests.post(url,data=openSession,headers=headers)
    key_xml = response.content
    #key = result.decode().split("</wsse:BinarySecurityToken>")[0].split("<wsse:BinarySecurityToken")[1].split(">")[1]
    key_xml_soup = BeautifulSoup(key_xml, 'html.parser') 
#    key = key_xml_soup.find('wsse:BinarySecurityToken'.lower()).get_text()
    return key_xml_soup.find('wsse:BinarySecurityToken'.lower()).get_text()
