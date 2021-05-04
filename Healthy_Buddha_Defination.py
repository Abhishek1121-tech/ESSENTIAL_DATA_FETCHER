from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json
import requests
import re

class Healthy_Buddha_Defination:

    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Healthy_Buddha]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Healthy_Buddha]['base_url']+vendor['product_query']
        cookie_header=Constants.NONE
        raw_data=Constants.NONE
        return url,cookie_header,raw_data

    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(url)
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type)
        #print(read_response.text)
        if read_response and read_response != Constants.EXCEPTION_QUERY:
            #print(read_response)
            soup = BeautifulSoup(read_response.text,'html.parser')
            extracted_data=soup.find(id=config_dict[Constants.Healthy_Buddha]['id_value']).find_all('option')
            #print(extracted_data)
            if extracted_data :
                #print(extracted_data)
                data = extracted_data[Constants.NUM_0]
                #print(data)
                sku_unit=str(data).split(Constants.DASH+Constants.SPACE+Constants.LESSER_OP)[Constants.NUM_0].split(Constants.GREATER_OP)[Constants.NUM_1]
                sku_value=str(data).split(Constants.DASH+Constants.SPACE+Constants.LESSER_OP)[Constants.NUM_1].split(Constants.GREATER_OP)[Constants.NUM_2].split(Constants.LESSER_OP)[Constants.NUM_0]
                price_vendor_list.append(Constants.Healthy_Buddha.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(sku_value.strip())
                #print(price_vendor_list)
                return_list.append(price_vendor_list) 
                price_vendor_list=[]
                price_vendor_list.append(Constants.Healthy_Buddha.replace(Constants.UNDERSCORE,Constants.SPACE)+Constants.SPACE+Constants.STR_SKU)
                price_vendor_list.append(sku_unit)
                #print(price_vendor_list)
                return_list.append(price_vendor_list)
            if config_dict[Constants.Healthy_Buddha]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        #print(return_list)
        return return_list    
           
