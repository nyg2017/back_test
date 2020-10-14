## CROSS SECTION BACKTEST SYSTEM

*最近在研究基于机器学习、深度学习的股票因子挖掘和策略构建，简单调研了一些开源的主流的回测框架，发现难以满足自己的需求，因为机器学习一般对于一个股票池中的所有股票预测信号，信号的强度可以作为是该股票池的建仓基础，然后对该股票池的股票进行仓位分配后进行建仓，所以需要一套基于某一日期的股票池横截面信号的回测系统，在进行了一系列思考后，最终决定自己写一套简易的回测框架，从而支持后续的研究工作。十一期间利用假期算是完成了初步版本，初步的测试发现是能用的，但是可能存在潜在的bug，希望开源后，在更多人的努力下逐渐完善该回测系统。欢迎大佬拍砖，以及提bug。*

交流微信：（申请中）

### CROSS SECTION BACKTEST SYSTEM（基于横截面的回测系统）是一套用于测试机器学习因子效果以及构建基于机器学习的股票池的简易回测系统

## Install

### 1. Clone code
```bash
mkdir ml_quant
cd ml_quant
git clone 
export PYTHONPATH=../ml_quant
```

### 2. Install dependence python packages

It is recommend to use Anaconda package manager.

```bash
conda install numpy matplotlib pandas 
pip install jqdatasdk
```

If you don't have Anaconda:

```
pip3 install numpy matplotlib pandas 
pip install jqdatasdk
```

### 3. Run Sample

```bash
# add you jqdata account and passwd
vim ./back_test/data_interface.py
#modify  account and password as your jqdata account and password
# 聚宽数据可以申请一年的免费试用期。申请方式见：https://www.joinquant.com/default/index/sdk
# account = ""
# password = ""
python sample back_test/base_bt.py
```



### 基本框架

#### 特性：

- 初始化账户信息BaseBT.__init__(capital,base_index,fee_rate,slide_point,start_date,end_date,position_mode)
  - capital：初始资金
  - base_index：参照指数
  - fee_rate：手续费率
  - start_date：开始日期
  - end_date：结束日期
  - position_mode：根据机器学习的预测scores，采用的分仓策略，（可以在./back_test/util/position.py 中自定义规则和参数）
- 按照交易日排序逐日传入股票池的stock_array，以及对应的机器学习预测的score_array。（BaseBt.run(datetime,stock_pool,stock_score,total_position))）
  - datetime：交易日期
  - stock_pool：股票池（ndarray）
  - stock_score：预测的分数（ndarray）
  - total_position：总仓位（0～1，float）

#### 部分特性说明：

- 一字涨停跌停的票均不买不卖。
- 不支持多空策略（TODO）
- 不支持滑点
- 以收盘价进行买卖
- 自定义数据接口，目前采用的是jqdata，如果用其他的数据，在data_interface/data_api.py中定义自己的数据接口，并且重写data_interface/jq_data.py中所有方法。

#### 框架示意图：

![1.png](https://github.com/nyg2017/back_test/blob/master/image/1.png?raw=true)

#### 设计思路

待整理



TODO：

- debug
- 滑点
- 太多了