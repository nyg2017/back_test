## CROSS SECTION BACKTEST SYSTEM

*最近在研究基于机器学习、深度学习的股票因子挖掘和策略构建，简单调研了一些开源的主流的回测框架，发现难以满足自己的需求，因为机器学习一般对于一个股票池中的所有股票预测信号，信号的强度可以作为是该股票池的建仓基础，然后对该股票池的股票进行仓位分配后进行建仓，所以需要一套基于某一日期的股票池横截面信号的回测系统，在进行了一系列思考后，最终决定自己写一套简易的回测框架，从而支持后续的研究工作。十一期间利用假期算是完成了初步版本，初步的测试发现是能用的，但是可能存在潜在的bug，希望开源后，在更多人的努力下逐渐完善该回测系统欢迎大佬拍砖，以及提bug。*

交流微信：（申请中）

### CROSS SECTION BACKTEST SYSTEM（基于横截面的回测系统）是一套用于测试机器学习因子效果以及构建基于机器学习的股票池的回测系统，

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

```
python sample back_test/base_bt.py
```



