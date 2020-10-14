import numpy as np 


def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma

def meanPosition(stock_score):
    position = np.ones_like(stock_score,dtype=np.float)
    position = position/np.sum(position)
    return position

def expPosition(stock_score):
    stock_exp = np.exp(standardization(stock_score).astype(np.float64))
    position = stock_exp/ np.sum(stock_exp)
    return position

def partPosition(stock_score,precent = 0.5):
    stock_exp = np.exp(standardization(stock_score).astype(np.float64))
    mid = np.median(stock_exp)
    stock_exp[stock_exp < mid] = 0.0
    position = stock_exp/ np.sum(stock_exp)  
    return position
    