from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json


class Gournet_Defination:

    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Gournet_Garden]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Gournet_Garden]['base_url']+vendor['product_query']+Constants.QUESTION_MARK+Constants.WRD_CITY+Constants.EQUALS+vendor['location_query']
        try:
            #print(vendor['product_vpid'])
            if vendor['v_id'] != "NA":
                url+=Constants.AMPERCENT+"variant"+Constants.EQUALS+vendor['v_id']
        except KeyError:
            print("product_vpid is not found, normal url will be used for quering "+vendor['product_name']+" || vendor is "+vendor['vendor_name'])   
        cookie_header=Constants.NONE
        raw_data=Constants.NONE
        return url,cookie_header,raw_data

    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type)
        #print(r.text)
        if read_response and read_response != Constants.EXCEPTION_QUERY:
            soup = BeautifulSoup(read_response.text, 'html.parser')
            parsed_txt=soup.find(id=config_dict[Constants.Gournet_Garden]['script_parser_id'])
            #print(parsed_json)
            if parsed_txt is not None:
                data = json.loads(parsed_txt.text.strip())
                #print(data)
                price_vendor_list.append(Constants.Gournet_Garden.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(data[config_dict[Constants.Gournet_Garden]['price_syntax_in_json']]/Constants.NUM_100)
                return_list.append(price_vendor_list)
                parsed_txt_name_with_sku=soup.find(config_dict[Constants.Gournet_Garden]['meta_tag_value'],property=config_dict[Constants.Gournet_Garden]['match_name_content'])
                sku_parse=str(parsed_txt_name_with_sku[config_dict[Constants.Gournet_Garden]['sku_syntax_in_json']]).split(Constants.DASH)
                length_sku_list=len(sku_parse)
                sku_list_value=sku_parse[Constants.NUM_1:length_sku_list]
                #print(sku_parse[Constants.NUM_1:length_sku_list])
                sku_value=Constants.SPACE.join(map(str,sku_list_value))
                #print(sku_value)
                price_vendor_list=[]
                price_vendor_list.append(Constants.Gournet_Garden.replace(Constants.UNDERSCORE,Constants.SPACE)+Constants.SPACE+Constants.STR_SKU)
                price_vendor_list.append(sku_value)
                return_list.append(price_vendor_list)
                if config_dict[Constants.Gournet_Garden]['discounted_is_required'] == str(True):
                    print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list




    
