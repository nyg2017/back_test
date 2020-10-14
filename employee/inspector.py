import numpy as np
from back_test.date_interface.data_api import UserDataApi


class Inspector(object):
    def __init__(self,):
        pass
        

    def suspensionCheck(self,date_time,stock_code_list):
        suspension = UserDataApi.getSuspensionInfor(date_time,stock_code_list)
        return np.array(suspension)

    def limitCheck(self,date_time,stock_code_list):
        limit = UserDataApi.getLimitInfor(date_time,stock_code_list)
        return np.array(limit)

    def tradeableCheck(self,date_time,stock_code_list):
        suspension = self.suspensionCheck(date_time,stock_code_list)
        limit = self.limitCheck(date_time,stock_code_list)
        tradeable = np.logical_and(suspension,limit)
        return tradeable
        #return stock_list[tradeable],stock_rank[tradeable]

