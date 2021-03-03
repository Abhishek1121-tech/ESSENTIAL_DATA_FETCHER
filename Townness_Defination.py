from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json

class Townness_Defination:

    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Gournet_Garden]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Townness]['base_url']
        cookie_header=Constants.NONE
        raw_data="categoryid="+vendor['category_id']+"&productid="+vendor['product_id']+"&type=getproduct"
        return url,cookie_header,raw_data
    
    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        data = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type).json()
        #print(data)
        if data:
            price_vendor_list.append(Constants.Townness.replace(Constants.UNDERSCORE,Constants.SPACE))
            price_vendor_list.append(data[Constants.NUM_0][config_dict[Constants.Townness]['mrp_syntax']])
            return_list.append(price_vendor_list)
            if config_dict[Constants.Townness]['discounted_is_required'] == str(True):
                #print("if True then will add the discounted price also not required in this case, you can add later")
                price_vendor_list=[]
                price_vendor_list.append(Constants.Townness_Discounted.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(data[Constants.NUM_0][config_dict[Constants.Townness]['sp_syntax']])
                return_list.append(price_vendor_list)
        return return_list


        
           
