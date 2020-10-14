import pandas as pd
import numpy as np
import os
from back_test.employee.positionspilitor import PositionSpilitor
from back_test.date_interface.data_api import UserDataApi
from back_test.employee.inspector import Inspector

class StockTrader(object):
    def __init__(self,fee_rate,slide_point,bookkeeper,position_mode):
        self.fee = fee_rate
        self.slide_point = slide_point
        self.position_mode = position_mode
        self.bookkeeper = bookkeeper
        self.position_spilitor = PositionSpilitor(position_mode,bookkeeper)
        self.inspector = Inspector()

    def sell(self,target_code,target_info,last_hold_by_code):
        last_aver_cost = last_hold_by_code['aver_cost']
        last_hold_num = last_hold_by_code['hold_num']

        sell_num =  last_hold_num - target_info['target_num']
        sell_price = target_info['market_price']
        
        self_value = sell_price * sell_num 
        trade_fee = self_value * self.fee

        if last_hold_num - sell_num > 0:
            target_aver_cost = (last_aver_cost * last_hold_num - self_value + trade_fee)/(last_hold_num - sell_num)
            self.bookkeeper.addNewHoldStateForCode(target_code,target_aver_cost,sell_price,target_info['target_num'] )
        else:
            target_aver_cost = (last_aver_cost * last_hold_num - self_value + trade_fee)
            self.bookkeeper.addNewHoldStateForCode(target_code,target_aver_cost,sell_price,target_info['target_num'] )

        self.bookkeeper.addNewTransactionInfoForCode(target_code,sell_price,-sell_num,trade_fee)
        self.bookkeeper.cash += (self_value - trade_fee)
            

    def buy(self,target_code,target_info,last_hold_by_code):
        last_aver_cost = last_hold_by_code['aver_cost']
        last_hold_num = last_hold_by_code['hold_num']

        buy_num = target_info['target_num'] - last_hold_num
        buy_price = target_info['market_price']

        buy_value = buy_num * buy_price
        trade_fee = buy_value * self.fee

        target_aver_cost = (last_aver_cost * last_hold_num + buy_value + trade_fee ) / (buy_num + last_hold_num)

        if self.bookkeeper.cash < (buy_value + trade_fee):

            raise ("error : cash is not enough for target stock num, please check you codes")
        self.bookkeeper.addNewHoldStateForCode(target_code,target_aver_cost,buy_price,target_info['target_num'] )
        self.bookkeeper.addNewTransactionInfoForCode(target_code,buy_price,buy_num,trade_fee)

        self.bookkeeper.cash -= (buy_value + trade_fee)


    def BatchBuy(self,last_account_hold_dict,target_hold_dict):
        
        for target_code,target_info in target_hold_dict.items():
            if target_code not in last_account_hold_dict.keys():
                last_hold_by_code = self.bookkeeper.initCodeInfoForHoldState(aver_cost = 0, market_price = 0, hold_num = 0)
            else:
                last_hold_by_code = last_account_hold_dict[target_code]            
            
            last_hold_num = last_hold_by_code['hold_num']
            target_hold_num = target_info['target_num']
            if last_hold_num == 0.0 and abs(target_hold_num) == 0.0:
                continue 
            if target_hold_num >= last_hold_num:
                self.buy(target_code,target_info,last_hold_by_code)  
        
        

    def BatchSell(self,last_account_hold_dict,target_hold_dict):
        for target_code,target_info in target_hold_dict.items():
            if target_code not in last_account_hold_dict.keys():
                last_hold_by_code = self.bookkeeper.initCodeInfoForHoldState(aver_cost = 0, market_price = 0, hold_num = 0)
            else:
                last_hold_by_code = last_account_hold_dict[target_code]            
            
            last_hold_num = last_hold_by_code['hold_num']
            
            target_hold_num = target_info['target_num']
            if last_hold_num == 0 and abs(target_hold_num) == 0:
                continue 
            if target_hold_num < last_hold_num:
                self.sell(target_code,target_info,last_hold_by_code)            
    


    def tradeByDatetime(self,last_account_dict,target_hold_dict):
        #target_hold_dict_extend = self.extend_target_hold_dict(ori_hold_dict,target_hold_dict)
        
        last_account_hold_dict = last_account_dict['hold_state']
        self.BatchSell(last_account_hold_dict,target_hold_dict)

        self.BatchBuy(last_account_hold_dict,target_hold_dict)      
        self.bookkeeper.finishTradeByDatetime()
             

    def getStockPriceDict(self,date_time,target_stock_pool,last_hold_state_dict):
        last_stock_list = last_hold_state_dict.keys()

        stock_list = list(set(target_stock_pool).union(set(last_stock_list)))
        price_list = UserDataApi.getClosePrices(date_time = date_time,stock_code_list = stock_list)
        tradeable_array = self.inspector.tradeableCheck(date_time= date_time,stock_code_list = stock_list)

        return dict(zip(stock_list,price_list)),dict(zip(stock_list,list(tradeable_array)))
    
    def run(self,datetime,stock_pool,stock_score,total_position):
        last_account_dict = self.bookkeeper.lastAccountState()
        stock_price_dict,stock_tradeable_dict = self.getStockPriceDict(datetime,stock_pool,last_account_dict['hold_state'])
        self.bookkeeper.updateAccountInfo(stock_price_dict)
        target_hold_dict = self.position_spilitor.getTargetPosition(stock_pool = stock_pool,
                                                                    stock_score = stock_score,
                                                                    total_position = total_position,
                                                                    stock_price_dict = stock_price_dict,
                                                                    stock_tradeable_dict = stock_tradeable_dict,
                                                                    last_hold_account_dict = last_account_dict)
        self.tradeByDatetime(last_account_dict,target_hold_dict)

        
        