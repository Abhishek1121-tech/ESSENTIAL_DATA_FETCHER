from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json
import requests
import re

class Organic_World_Defination:

    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Organic_World]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Organic_World]['base_url']+vendor['product_query']
        cookie_header=Constants.NONE
        raw_data=Constants.NONE
        return url,cookie_header,raw_data

    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(url)
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type).text
        #print(r.text)
        if read_response:
            #print(read_response)
            soup = BeautifulSoup(read_response,features="lxml")
            parsed_txt=soup.find(config_dict[Constants.Organic_World]['meta_tag_value'],property=config_dict[Constants.Organic_World]['match_price_content'])
            #print(parsed_txt["content"])
            price_vendor_list.append(Constants.Organic_World.replace(Constants.UNDERSCORE,Constants.SPACE))
            price_vendor_list.append(parsed_txt[config_dict[Constants.Organic_World]['mrpprice_syntax_in_json']])
            #print(price_vendor_list)
            return_list.append(price_vendor_list)
            if config_dict[Constants.Organic_World]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list
                   
            
           