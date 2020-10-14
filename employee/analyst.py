import numpy as np
import datetime
from copy import deepcopy
from prettytable import PrettyTable

def isYearEnd(date):
    return False


'''
def getPerDayReturn(capital_list):
    capital_array = np.array(capital_list)
    capital_array_temp = deepcopy(capital_array)
    capital_array_temp[1:] = capital_array[:capital_array.shape[0]-1]
    return_per_day = capital_array/capital_array_temp - 1.0
    return return_per_day
'''
def getPerDayReturn(capital_list):
    capital_array = np.array(capital_list)
    return_per_day = capital_array/capital_array[0]
    return return_per_day


class Analyst(object):
    def __init__(self,free_return = 0.04):
        self.lost_free_return=free_return

    def reCollectData(self,bookkeeper):
        self.date_list = []
        self.capital_list = []
        self.pnl_list = []
        self.cash_list = []
        self.turnover_list = []
        for daily_record in bookkeeper.getDailyRecord():
            self.date_list.append(daily_record['date_time'])
            self.capital_list.append(daily_record['capital'])
            #pnl_list.append(daily_record['pnl'])
            self.cash_list.append(daily_record['cash'])
            self.turnover_list.append(daily_record['turnover'])#['turnover'])
    
    def analystByYear(self,start_index,end_index,table):
        start_date = self.date_list[start_index]
        end_date = self.date_list[end_index]
        day_nums = end_index - start_index + 1
        
        if start_index == 0:
            begin_capital = self.capital_list[start_index]
        else:
            begin_capital = self.capital_list[start_index-1]

        end_capital = self.capital_list[end_index]
        
        annual_return = (end_capital / begin_capital) ** (250 / day_nums) - 1 
        period_return = (end_capital / begin_capital) - 1 

        turnover_rate = np.sum(np.array(self.turnover_list)) / begin_capital

        return_per_day = getPerDayReturn(self.capital_list)

        std_var = np.std(return_per_day)
        sharpe = (annual_return - self.lost_free_return) / std_var
    

        max_draw_back,max_draw_begin,max_draw_end = self.maxDrawback(self.capital_list[start_index:end_index + 1],self.date_list[start_index:end_index + 1])

        table.add_row([start_date,end_date,"%.2f"%period_return,"%.2f"%annual_return,"%.2f"%turnover_rate,"%.2f"%sharpe,"%.2f"%max_draw_back,max_draw_begin,max_draw_end])

    def maxDrawback(self,return_list,date_list):
        '''最大回撤率'''
        i = np.argmax((np.maximum.accumulate(return_list) - return_list) / np.maximum.accumulate(return_list))  # 结束位置

        if i == 0:
            return 0,date_list[0],date_list[0]
        j = np.argmax(return_list[:i])  # 开始位置
        return (return_list[j] - return_list[i]) / (return_list[j]) , date_list[j],date_list[i]


    def run(self,bookkeeper):
        self.reCollectData(bookkeeper)

        begin = 0
        table = PrettyTable(['begin','end','period_return','annual_return','turnover_rate','sharpe','max_draw_back','max_draw_begin','max_draw_end'])
        
        for i in range(len(self.date_list)):
            if isYearEnd(self.date_list[i]) or i == len(self.date_list) - 1:
                self.analystByYear(begin,i,table) 
                begin = i + 1
        print (table)


