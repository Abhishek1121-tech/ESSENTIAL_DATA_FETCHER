from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from bs4 import BeautifulSoup
import json

class Natures_Defination:
    def getUrlWithHeaderRawData(vendor):
        #print(vendor)
        config_dict=ConfigReader.get_confic_dict()
        url=config_dict[Constants.Nature_s_Basket]['http_scheme']+Constants.COLON+Constants.DOUBLEFORWARDSLASH+config_dict[Constants.Nature_s_Basket]['base_url']+vendor['product_query']+Constants.FORWARDSLASH+vendor['product_id']
        cookie_header="cookie: "+vendor['location_query']
        raw_data=Constants.NONE
        return url,cookie_header,raw_data

    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        return_list=[]
        price_vendor_list=[]
        read_response = Utils.makeRequestUrl(url,cookie_header,raw_data,method_type).text
        #print(read_response)
        if read_response:
            soup = BeautifulSoup(read_response,'html.parser')
            data=soup.find(config_dict[Constants.Nature_s_Basket]['element_type'],{Constants.STR_ID : config_dict[Constants.Nature_s_Basket]['element_id']})[Constants.STR_VALUE]
            #print(data)
            price_vendor_list.append(Constants.Nature_s_Basket.replace(Constants.UNDERSCORE,Constants.SPACE))
            price_vendor_list.append(data)
            return_list.append(price_vendor_list)
            if config_dict[Constants.Nature_s_Basket]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list


