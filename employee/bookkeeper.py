


class BookKeeper(object):
    def __init__(self,ori_capital,start_date):
        self.account = dict()
        self.index = 0
        self.addNewBaseRecord(start_date)
        self.account[self.index]['capital'] = ori_capital
        self.account[self.index]['cash'] = ori_capital
        self.capital = ori_capital
        self.cash = ori_capital

        

    def newDayBegin(self,date):
        self.index += 1
        self.addNewBaseRecord(date)

    def dayEnd(self,date):
        pass

    def addNewBaseRecord(self,date):
        new_record = dict()
        new_record['capital'] = -1
        new_record['cash'] = -1
        new_record['date_time'] = date
        new_record['hold_state'] = dict()
        new_record['transaction_state'] = dict()
        new_record['index_state'] = dict()  
        new_record['turnover'] = 0.0
        self.account[self.index] = new_record

    def addNewHoldStateForCode(self,code,aver_cost,market_price,hold_num):
        re_code_account_info = dict()
        re_code_account_info['aver_cost'] = aver_cost
        re_code_account_info['market_price'] = market_price
        re_code_account_info['hold_num'] = hold_num
        re_code_account_info['cost'] = aver_cost * hold_num
        re_code_account_info['market_value'] = market_price * hold_num
        re_code_account_info['pnl'] = market_price * hold_num - aver_cost * max(hold_num,1) # when sell the stock to zero, we need to keep the aver_cost as pnl cause the hold_num is zero
        self.account[self.index]['hold_state'][code] = re_code_account_info

    def initCodeInfoForHoldState(self,aver_cost,market_price,hold_num):
        re_code_account_info = dict()
        re_code_account_info['aver_cost'] = aver_cost
        re_code_account_info['market_price'] = market_price
        re_code_account_info['hold_num'] = hold_num
        re_code_account_info['cost'] = aver_cost * hold_num
        re_code_account_info['market_value'] = market_price * hold_num
        re_code_account_info['pnl'] = market_price * hold_num - aver_cost * hold_num
        return re_code_account_info

    def addNewTransactionInfoForCode(self,code,transaction_price,transaction_num,transaction_fee):
        re_transaction_info_for_code = dict()
        re_transaction_info_for_code['transaction_price'] = transaction_price
        re_transaction_info_for_code['transaction_num'] = transaction_num
        re_transaction_info_for_code['transaction_fee'] = transaction_fee
        re_transaction_info_for_code['turnover'] = transaction_price * abs(transaction_num) + transaction_fee
        self.account[self.index]['turnover'] += transaction_price * abs(transaction_num) + transaction_fee
        self.account[self.index]['transaction_state'][code] = re_transaction_info_for_code

    def addNewIndexState(self,index_code,index_value):
        re_new_index_state = dict()
        re_new_index_state["index_code"] = index_code
        re_new_index_state["index_value"] = index_value
        self.account[self.index]['index_state'] = re_new_index_state


    def finishTradeByDatetime(self):
        self.account[self.index]['capital'] = self.capital
        self.account[self.index]['cash'] = self.cash

    def updateAccountInfo(self,stock_price_dict):
        stock_total_value = 0
        for k,v in self.account[self.index-1]['hold_state'].items():
            stock_total_value += stock_price_dict[k] * v['hold_num']
        
        self.capital = stock_total_value + self.cash

    def getDailyRecord(self):
        for i in range(self.index + 1):
            yield self.account[i]


    def lastAccountState(self):
        return self.account[self.index-1]
    
    def currentAccountState(self):
        return self.account[self.index]
    
    