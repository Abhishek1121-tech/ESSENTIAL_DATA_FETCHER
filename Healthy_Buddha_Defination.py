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
        print(url)
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type).text
        #print(r.text)
        if read_response:
            #print(read_response)
            soup = BeautifulSoup(read_response,'html.parser')
            sku_value_selected=(str(soup.option).split(Constants.DASH)[Constants.NUM_0].split(Constants.GREATER_OP)[Constants.NUM_1])
            #print(sku_value_selected)
            parsed_txt=soup.findAll(config_dict[Constants.Healthy_Buddha]['script_tag_value'])
            #print(parsed_txt)
            extracted_data=Constants.NONE
            for txt in parsed_txt:
                if re.search(config_dict[Constants.Healthy_Buddha]['match_price_content'],txt.text):
                    #print(txt.text)
                    extracted_data=txt.text
            if extracted_data != Constants.NONE:
                #print(extracted_data)
                regex = r'''(?<=[}\]"']),(?!\s*[{["'])'''
                extracted_data=re.sub(regex, "", extracted_data, 0)
                print(extracted_data)
                data = json.loads(extracted_data)
                #print(data)
                price_vendor_list.append(Constants.Healthy_Buddha.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(data[config_dict[Constants.Healthy_Buddha]['json_product_index_name']][config_dict[Constants.Healthy_Buddha]['mrpprice_syntax_in_json']])
                #print(price_vendor_list)
                return_list.append(price_vendor_list) 
                price_vendor_list=[]
                price_vendor_list.append(Constants.Healthy_Buddha.replace(Constants.UNDERSCORE,Constants.SPACE)+Constants.SPACE+Constants.STR_SKU)
                price_vendor_list.append(sku_value_selected)
                #print(price_vendor_list)
                return_list.append(price_vendor_list)
            if config_dict[Constants.Healthy_Buddha]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list     
           
