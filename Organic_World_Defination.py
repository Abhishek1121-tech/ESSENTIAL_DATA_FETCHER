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
        if read_response and read_response != Constants.EXCEPTION_QUERY:
            #print(read_response)
            soup = BeautifulSoup(read_response.text,features="html.parser")
            parsed_txt=soup.find_all(config_dict[Constants.Organic_World]['tag_value'])
            #print(parsed_txt)
            extracted_data=Constants.NONE
            for txt in parsed_txt:
                if re.search('var meta',txt.text):
                    #print(txt.text)
                    extracted_data=txt.text
                    break
            if extracted_data != Constants.NONE:
                data_str=extracted_data.split("var meta = ")[Constants.NUM_1].split(';\nfor')[Constants.NUM_0]
                data = json.loads(data_str)
                any_one_variant=data['product']['variants'][Constants.NUM_0]
                sku_value=any_one_variant['price']/100
                sku_unit=any_one_variant['public_title']
                if sku_unit is None:
                    sku_unit=any_one_variant['name'].split(Constants.COMMA)[Constants.NUM_1]
                price_vendor_list.append(Constants.Organic_World.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(sku_value)
                #print(price_vendor_list)
                return_list.append(price_vendor_list)
                #print(sku_value+Constants.SPACE+sku_unit)
                price_vendor_list=[]
                price_vendor_list.append(Constants.Organic_World.replace(Constants.UNDERSCORE,Constants.SPACE)+Constants.SPACE+Constants.STR_SKU)
                price_vendor_list.append(sku_unit)
                #print(price_vendor_list)
                return_list.append(price_vendor_list)
            if config_dict[Constants.Organic_World]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        print(return_list)
        return return_list
                   
            
           
