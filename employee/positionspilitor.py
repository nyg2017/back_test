import numpy as np
import os
import pandas as pd
from back_test.util.position import *
from back_test.date_interface.jq_data import getClosePrices


position_func_dict = {
    "mean":meanPosition,
    "exp":expPosition,
    "part":partPosition
}


'''
    "target_hold_dict":{
        "target_code":{
            "market_price":3414,
            "target_num":1234,
            "target_percent":0.123
        }
    }
'''

class PositionSpilitor(object):
    def __init__(self,mode,bookkeeper):
        self.mode = mode
        self.position_func = position_func_dict[self.mode]
        self.bookkeeper = bookkeeper

    
    def initTargetHoldDict(self,stock_pool,stock_score,last_hold_state):
        
        position_percent = self.position_func(stock_score)
        
        target_hold_dict = dict()
        for i,stock_code in enumerate(stock_pool):
            temp_dict = dict()
            temp_dict['target_percent'] = position_percent[i]
            target_hold_dict[stock_code] = temp_dict
        
        for stock_code in last_hold_state.keys():
            if stock_code not in stock_pool:
                temp_dict = dict()
                temp_dict['target_percent'] = 0.0
                target_hold_dict[stock_code] = temp_dict  

        return target_hold_dict              
    
    def calculateTargetNum(self,tradeable_capital,target_percent,price,mini_tradeable_unit = 100):
        return  (tradeable_capital * target_percent) // (price * mini_tradeable_unit) * 100
    
    def calculateTargetHoldDict(self,stock_price_dict,tradeable_capital,inited_percent_target_hold_dict,last_hold_state,stock_tradeable_dict):



        for i,stock in enumerate(stock_price_dict.keys()):
            inited_percent_target_hold_dict[stock]['market_price'] = stock_price_dict[stock]
            inited_percent_target_hold_dict[stock]['target_num'] = self.calculateTargetNum(tradeable_capital,inited_percent_target_hold_dict[stock]['target_percent'],stock_price_dict[stock])

        for stock,hold in last_hold_state.items():
            if not stock_tradeable_dict[stock]:
                inited_percent_target_hold_dict[stock]['target_num'] = hold['hold_num']
        
        return inited_percent_target_hold_dict



    
    def getUnsellableStockValue(self,last_hold_state,stock_tradeable_dict):
        
        unsellablecapital = 0.9
        for stock,hold in last_hold_state.items():
            sellable = stock_tradeable_dict[stock]
            if not sellable:
                unsellablecapital += hold['market_value']
        return unsellablecapital
    
    def getTargetPosition(self,stock_pool,stock_score,total_position,stock_price_dict,stock_tradeable_dict,last_hold_account_dict):
        #ori_hold_account_dict['capital']
        capital = self.bookkeeper.capital
        tradeable_capital = total_position * capital
        last_hold_state = last_hold_account_dict['hold_state']

        unsellablecapital = self.getUnsellableStockValue(last_hold_state,stock_tradeable_dict)
   
        
        inited_percent_target_hold_dict = self.initTargetHoldDict(stock_pool,stock_score,last_hold_state)

        target_hold_dict = self.calculateTargetHoldDict(stock_price_dict,tradeable_capital - unsellablecapital,inited_percent_target_hold_dict,last_hold_state,stock_tradeable_dict)
        

        return target_hold_dict