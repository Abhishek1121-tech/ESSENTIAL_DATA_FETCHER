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
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type)
        #print(r.text)
        if read_response:
            #print(read_response)
            soup = BeautifulSoup(read_response.text,features="html.parser")
            parsed_txt=soup.find(config_dict[Constants.Organic_World]['meta_tag_value'],property=config_dict[Constants.Organic_World]['match_price_content'])
            #print(parsed_txt["content"])
            if parsed_txt is not None:
                price_vendor_list.append(Constants.Organic_World.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(parsed_txt[config_dict[Constants.Organic_World]['mrpprice_syntax_in_json']])
                #print(price_vendor_list)
                return_list.append(price_vendor_list)
                parsed_txt_name_with_sku=soup.find(config_dict[Constants.Organic_World]['meta_tag_value'],property=config_dict[Constants.Organic_World]['match_name_content'])
                sku_parse=str(parsed_txt_name_with_sku[config_dict[Constants.Organic_World]['sku_syntax_in_json']]).split(Constants.OPEN_BRC)[Constants.NUM_0].split(Constants.SPACE)
                #print(str(parsed_txt_name_with_sku[config_dict[Constants.Organic_World]['sku_syntax_in_json']]).split(Constants.OPEN_BRC)[Constants.NUM_0])
                sku_parse_len=len(sku_parse)
                #sku_value=parsed_txt_name_with_sku[config_dict[Constants.Organic_World]['sku_syntax_in_json']].split(Constants.OPEN_BRC)[::-1].split(Constants.SPACE)[Constants.NUM_1][::-1]
                sku_unit=sku_parse[sku_parse_len-Constants.NUM_1]
                sku_value=sku_parse[sku_parse_len-Constants.NUM_2]
                #print(sku_value+Constants.SPACE+sku_unit)
                price_vendor_list=[]
                price_vendor_list.append(Constants.Organic_World.replace(Constants.UNDERSCORE,Constants.SPACE)+Constants.SPACE+Constants.STR_SKU)
                price_vendor_list.append(sku_value+Constants.SPACE+sku_unit)
                #print(price_vendor_list)
                return_list.append(price_vendor_list)
            if config_dict[Constants.Organic_World]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list
                   
            
           
