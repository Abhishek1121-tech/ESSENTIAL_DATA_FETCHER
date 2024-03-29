
from ConfigReader import ConfigReader
from Constants import Constants
from Utils import Utils
from collections import defaultdict
from Gournet_Defination import Gournet_Defination
from Bigbasket_Defination import Bigbasket_Defination
from Natures_Defination import Natures_Defination
from Townness_Defination import Townness_Defination
from Bigbasket_Organic_Defination import Bigbasket_Organic_Defination
from ModelMonthlyBucketDataPersister import ModelMonthlyBucketDataPersister
from Simpli_Namdharis_Defination import Simpli_Namdharis_Defination
from Organic_World_Defination import Organic_World_Defination
from Healthy_Buddha_Defination import Healthy_Buddha_Defination

class ModelMonthlyBucketDataMiner:

    def __init__(self):
        self.start()

    def start(self):
        config_dict=ConfigReader.get_confic_dict()
        raw_file_path=config_dict[Constants.STRING_APP]['info_file_basepath_app']+config_dict[Constants.STRING_APP]['info_file_path_app']
        #print(raw_file_path)
        dict_data = defaultdict(list)
        data = Utils.loadDataFromFile(raw_file_path)
        if data != Constants.EXCEPTION_LOAD:
            for info in data[Constants.INFO_DETAIL]:
                #print(info)
                data_dict_info = {}
                product_name=info[Constants.STR_PRODUCT_NAME]
                data_dict_info[Constants.STR_PRODUCT_NAME]=product_name
                product_type=info[Constants.STR_PRODUCT_TYPE]
                #data_dict_info[Constants.STR_PRODUCT_TYPE]=product_type
                sku_g=info[Constants.STR_SKU_G]
                data_dict_info[Constants.STR_SKU_G]=sku_g
                sku_u=info[Constants.STR_SKU_U]
                data_dict_info[Constants.STR_SKU_U]=sku_u
                vendor_list_in_dict=[]
                for vendor in info[Constants.STR_VENDOR_LIST]:
                    vendor_name=vendor[Constants.STR_V_NAME]
                    vendor_price_list=self.vendor_url_defination_caller(vendor)
                    #print(url+""+cookie_header+""+raw_data+""+str(price))
                    #print(vendor_name)
                    if vendor_price_list:
                        for v_p in vendor_price_list:
                            vendor_list_in_dict.append((v_p[Constants.NUM_0]+Constants.DOLLAR+str(v_p[Constants.NUM_1])).split(Constants.DOLLAR))           
                            print(str(vendor_list_in_dict)+"Data added")
                data_dict_info[Constants.STR_VENDOR_LIST]=vendor_list_in_dict
                vendor_list_in_dict=[]
                dict_data[product_type].append(data_dict_info)
                data_dict_info = {}
        else:
            print(data)
        ModelMonthlyBucketDataPersister.recDataPersist(dict_data)
        
    def vendor_url_defination_caller(self,vendor):
        #print(vendor[Constants.STR_V_NAME])
        #print(vendor)
        #print(Constants.Gournet_Garden)
        if vendor[Constants.STR_V_NAME] == Constants.Gournet_Garden.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Gournet_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Gournet_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Big_basket.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Bigbasket_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Bigbasket_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Big_basket_discounted.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Bigbasket_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Bigbasket_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Big_basket_Organic.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Bigbasket_Organic_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Bigbasket_Organic_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Big_basket_organic_Discounted.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Bigbasket_Organic_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Bigbasket_Organic_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Nature_s_Basket.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Natures_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Natures_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Townness.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Townness_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Townness_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_POST)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Townness_Discounted.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Townness_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Townness_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_POST)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Namdhari_s.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Simpli_Namdharis_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Simpli_Namdharis_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Organic_World.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Organic_World_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Organic_World_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list
        elif vendor[Constants.STR_V_NAME] == Constants.Healthy_Buddha.replace(Constants.UNDERSCORE,Constants.SPACE):
            url,cookie_header,raw_data=Healthy_Buddha_Defination.getUrlWithHeaderRawData(vendor)
            vendor_price_list=Healthy_Buddha_Defination.queryWebsite(url,cookie_header,raw_data,Constants.HTTP_METHOD_TYPE_GET)
            return vendor_price_list

        

modelMonthlyBucketDataMiner=ModelMonthlyBucketDataMiner()
