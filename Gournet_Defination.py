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
        cookie_header=Constants.NONE
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
            soup = BeautifulSoup(read_response, 'html.parser')
            parsed_txt=soup.find(id=config_dict[Constants.Gournet_Garden]['script_parser_id']).text.strip()
            #print(parsed_json)
            if parsed_txt:
                data = json.loads(parsed_txt)
                price_vendor_list.append(Constants.Gournet_Garden.replace(Constants.UNDERSCORE,Constants.SPACE))
                price_vendor_list.append(data[config_dict[Constants.Gournet_Garden]['price_syntax_in_json']]/Constants.NUM_100)
                return_list.append(price_vendor_list)
                if config_dict[Constants.Gournet_Garden]['discounted_is_required'] == str(True):
                    print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list




    