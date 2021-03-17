from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json
import requests
import re

class Simpli_Namdharis_Defination:

    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Namdhari_s]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Namdhari_s]['base_url']+vendor['product_query']+Constants.FORWARDSLASH+vendor['product_id']+Constants.DOT+config_dict[Constants.Namdhari_s]['url_extension']
        cookie_header=requests.cookies.RequestsCookieJar()
        cookie_header.set('Site_Config',vendor['location_query'])
        raw_data=Constants.NONE
        return url,cookie_header,raw_data

    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type).text
        #print(r.text)
        if read_response:
            soup = BeautifulSoup(read_response,'html.parser')
            parsed_txt=soup.findAll(config_dict[Constants.Namdhari_s]['script_tag_value'])
            #print(parsed_txt)
            data_txt_list=[]
            for txt in parsed_txt:
                if re.search(config_dict[Constants.Namdhari_s]['match_price_content'],txt.text):
                    #print(txt)
                    data_txt_split=txt.text.split(config_dict[Constants.Namdhari_s]['split_matched_content'].replace(Constants.DOLLAR,Constants.SPACE))
                    #extracted_data=data_txt_split[Constants.NUM_1].strip()\
                    data_txt_list.append(data_txt_split)
                    #print(extracted_data)
            #print(data_txt_list[Constants.NUM_0][Constants.NUM_1])
            extracted_data=data_txt_list[Constants.NUM_0][Constants.NUM_1]
            data = json.loads(extracted_data)
            data_variant=json.loads(data[config_dict[Constants.Namdhari_s]['json_product_index_name']][config_dict[Constants.Namdhari_s]['json_variants_index_name']])
            #print(data_variant)
            price_vendor_list.append(Constants.Namdhari_s.replace(Constants.UNDERSCORE,Constants.SPACE))
            price_vendor_list.append(data_variant[Constants.NUM_0][config_dict[Constants.Namdhari_s]['mrpprice_syntax_in_json']])
            #print(price_vendor_list)
            return_list.append(price_vendor_list)
            if config_dict[Constants.Namdhari_s]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list
                   
            
           