import jqdatasdk as jq
import numpy as np

account = "15210089516"
password = "Ningyaguang1"

def login():
    print ("login JQDATA servering")
    jq.auth(account,password)
    print ("login successed!")    
    remain_query = jq.get_query_count()
    print ("remain query times for jqdata: ",remain_query)

def getClosePrices(date_time,stock_code_list):
    result = jq.get_price(list(stock_code_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    code = list(result['code'])
    cps = list(result['close'])
    code_cps_dict = dict(zip(code,cps))
    return [code_cps_dict[k] for k in stock_code_list]



def getIndexValue(date_time,index):
    result = jq.get_price(index, start_date=date_time, end_date=date_time, frequency='daily', fields=['close'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    return result['close'].values


def getSuspensionInfor(date_time,stock_list):
    suspened_info_df = jq.get_price(list(stock_list), 
                       start_date=date_time, 
                       end_date=date_time, 
                       frequency='daily', 
                       fields='paused')#['paused'].T
    code = suspened_info_df['code']
    var = suspened_info_df['paused']
    sus_dict = dict(zip(code,var))
    return np.array([sus_dict[k] == 0 for k in stock_list])




def getLimitInfor(date_time,stock_list):
    result = jq.get_price(list(stock_list), start_date=date_time, end_date=date_time, frequency='daily', fields=['high','low'], skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
    var = list(result['high'] - result['low'])
    code = list(result['code'])
    code_limit_dict = dict(zip(code,var))
    return np.array([code_limit_dict[k] != 0 for k in stock_list])

def validIndex(date_time,stock_list):
    a = getSuspensionInfor(date_time,stock_list)
    b = getLimitInfor(date_time,stock_list)
    v = np.logical_and(a,b)
    return v


if __name__ == "__main__":
    login()
    code = ["300313.XSHE","300315.XSHE","300316.XSHE"]
    date_time = "2020-09-11"
    
    panel = getVolumn(date_time,code)
    print (panel)
