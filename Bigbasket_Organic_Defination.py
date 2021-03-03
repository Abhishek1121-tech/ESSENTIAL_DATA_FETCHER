from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json
import re

class Bigbasket_Organic_Defination:

    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Gournet_Garden]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Big_basket_Organic]['base_url']+vendor['product_id']+Constants.FORWARDSLASH+vendor['product_query']+Constants.FORWARDSLASH
        cookie_header="cookie:  _bb_cid="+vendor['location_query']
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
            parsed_txt=soup.findAll(config_dict[Constants.Big_basket_Organic]['script_tag_value'])
            #print(parsed_txt)
            for txt in parsed_txt:
                if re.search(config_dict[Constants.Big_basket_Organic]['match_price_content'],txt.text):
                    #print(txt)
                    data_txt_split=txt.text.split(config_dict[Constants.Big_basket_Organic]['split_matched_content'].replace(Constants.DOLLAR,Constants.SPACE))
                    extracted_data=data_txt_split[Constants.NUM_1].strip()
                    #print(extracted_data)
                    data = json.loads(extracted_data)
                    price_vendor_list.append(Constants.Big_basket_Organic.replace(Constants.UNDERSCORE,Constants.SPACE))
                    price_vendor_list.append(data[config_dict[Constants.Big_basket_Organic]['json_product_index_name']][config_dict[Constants.Big_basket_Organic]['json_variants_index_name']][Constants.NUM_0][config_dict[Constants.Big_basket_Organic]['mrpprice_syntax_in_json']])
                    return_list.append(price_vendor_list)
                    if config_dict[Constants.Big_basket_Organic]['discounted_is_required'] == str(True):
                        #print("if True then will add the discounted price also not required in this case, you can add later")
                        price_vendor_list=[]
                        price_vendor_list.append(Constants.Big_basket_organic_Discounted.replace(Constants.UNDERSCORE,Constants.SPACE))
                        price_vendor_list.append(data[config_dict[Constants.Big_basket_Organic]['json_product_index_name']][config_dict[Constants.Big_basket_Organic]['json_variants_index_name']][Constants.NUM_0][config_dict[Constants.Big_basket_Organic]['spprice_syntax_in_json']])
                        return_list.append(price_vendor_list)
        return return_list