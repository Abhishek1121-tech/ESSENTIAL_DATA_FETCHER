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
        #print(vendor['product_vpid'])
        #print(vendor)
        try:
            #print(vendor['product_vpid'])
            if vendor['product_vpid'] != "NA":
                url+=Constants.QUESTION_MARK+"vpid"+Constants.EQUALS+vendor['product_vpid']
        except KeyError:
            print("product_vpid is not found, normal url will be used for quering "+vendor['product_name']+" || vendor is "+vendor['vendor_name'])   
        #print(url)
        cookie_header=requests.cookies.RequestsCookieJar()
        cookie_header.set('Site_Config',vendor['location_query'])
        raw_data=Constants.NONE
        return url,cookie_header,raw_data

    def queryWebsite(url,cookie_header,raw_data,method_type):
        #print(url)
        #print(raw_data)
        config_dict=ConfigReader.get_confic_dict()
        v_product_id=Simpli_Namdharis_Defination.find_V_ProductID(url,config_dict)
        #print(v_product_id)
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
            #print(data_txt_list)
            extracted_data=data_txt_list[Constants.NUM_0][Constants.NUM_1]
            #print(extracted_data)
            data = json.loads(str(extracted_data))
            variant_data=data[config_dict[Constants.Namdhari_s]['json_product_index_name']][config_dict[Constants.Namdhari_s]['json_variants_index_name']]
            if variant_data is not None:
                #print(variant_data)
                data_variants=json.loads(variant_data)
                #print(data_variants)
                append_price_data=None
                sku_value=None
                if v_product_id == Constants.NONE:
                    append_price_data=data_variants[Constants.NUM_0][config_dict[Constants.Namdhari_s]['mrpprice_syntax_in_json']]
                    sku_value=data_variants[Constants.NUM_0][config_dict[Constants.Namdhari_s]['sku_variant_index_name']][config_dict[Constants.Namdhari_s]['sku_variant_weight_name']]
                    #print(sku_value)
                else:
                    for data_v in data_variants:
                        #print("variants"+str(data_v[config_dict[Constants.Namdhari_s]['variants_match_content']]))
                        if str(data_v[config_dict[Constants.Namdhari_s]['variants_match_content']]) == str(v_product_id):
                            #print("matched variant_product_id")
                            append_price_data=data_v[config_dict[Constants.Namdhari_s]['mrpprice_syntax_in_json']]
                            sku_value=data_v[config_dict[Constants.Namdhari_s]['sku_variant_index_name']][config_dict[Constants.Namdhari_s]['sku_variant_weight_name']]
                            #print(sku_value)
                            break
                #print("append data"+str(append_price_data))
                if append_price_data is not None:
                    price_vendor_list.append(Constants.Namdhari_s.replace(Constants.UNDERSCORE,Constants.SPACE))
                    price_vendor_list.append(append_price_data)
                    #print(price_vendor_list)
                    return_list.append(price_vendor_list)
                if sku_value is not None:
                    price_vendor_list=[]
                    price_vendor_list.append(Constants.Namdhari_s.replace(Constants.UNDERSCORE,Constants.SPACE)+Constants.SPACE+Constants.STR_SKU)
                    price_vendor_list.append(sku_value)
                    #print(price_vendor_list)
                    return_list.append(price_vendor_list)
            if config_dict[Constants.Namdhari_s]['discounted_is_required'] == str(True):
                print("if True then will add the discounted price also not required in this case, you can add later")
        return return_list
    
    def find_V_ProductID(url,config_dict):
        spilter_toFind_url_type=url[::-1].split(Constants.DOT)
        #print(spilter_toFind_url_type[Constants.NUM_0][::-1])
        matching_content=spilter_toFind_url_type[Constants.NUM_0][::-1]
        if matching_content == config_dict[Constants.Namdhari_s]['url_extension']:
           return Constants.NONE
        else:
            return matching_content.split(Constants.EQUALS)[Constants.NUM_1]