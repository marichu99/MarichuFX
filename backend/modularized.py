import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np    
from threading import Thread
import sys
import math
import json



#global variables
SYMBOLS = ["XAUUSD","EURUSD","USDCAD","USDJPY","AUDCAD","GBPUSD","GBPJPY","EURJPY"]
TIMEFRAME = mt5.TIMEFRAME_M15  
high_TIMEFRAME=[mt5.TIMEFRAME_M30,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_H1,mt5.TIMEFRAME_H4]
lower_TIMEFRAMES=[mt5.TIMEFRAME_M1,mt5.TIMEFRAME_M5,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_M30]
NUM_BARS=1000
FSMA_PERIOD = 10 # number of periods in the fast simple moving average
SL_SMA_PERIOD = 50 # number of periods in the slow moving average

# window formation
xauusd_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
eurusd_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
usdcad_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
usdjpy_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
audcad_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
gbpusd_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
gbpjpy_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}
eurjpy_Dict ={1:{"highPrice":[],"lowPrice":[]},5:{"highPrice":[],"lowPrice":[]},15:{"highPrice":[],"lowPrice":[]},30:{"highPrice":[],"lowPrice":[]}}


# contentious price points
cont_xauusd_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_eurusd_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_usdcad_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_usdjpy_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_audcad_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_gbpusd_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_gbpjpy_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_eurjpy_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}

def conn():
    # start the connection to MT5
    resu={
            "Response":200,
            "Message":"Data from python"
        }
    # resu["server"]=server
    valid_conn= mt5.initialize()
    # check if the connection went through
    if not (valid_conn):
        resu["init_err"]=mt5.last_error()
    # login into your account 
    login = mt5.login(36610,"Marichu12","EGMSecurities-Demo")
    if not login:
        resu["login_err"]=mt5.last_error()
    else:
        resu["Message"]="Login is Successful"
        print("the login was successful")
        # print(json.dumps(resu))
        with open("data.json","w") as dataF:
            json.dump(resu,dataF)
        gatherDataController()

def gatherDataController():
    print("We are gathering the data")
    global  er_TIMEFRAMES,high_TIMEFRAME,SYMBOLS
    for pair in SYMBOLS:
        for timeframe in  lower_TIMEFRAMES:
            backtest_data = mt5.copy_rates_from_pos(pair,timeframe,1,NUM_BARS)
            bars = pd.DataFrame(backtest_data)
            # save the data into a dataframe
            comprehensive_name=f"{str(pair)}{str(timeframe)}"
            bars.to_csv(rf"backend\backtest\{comprehensive_name}.csv")
            # pass the dataframe to another method for further pre-processing 
            splitAndPreprocess(bars,str(pair),timeframe)

def splitAndPreprocess(df,pair,timeframe):
    df= pd.DataFrame(df)
    # change the time variable
    df["time"]=pd.to_datetime(df["time"],unit="s")
    if(pair == "XAUUSD"):
        print("The size of the dataframe",df.shape[0])
        num_splits = df.shape[0]/100
        split_dfs=np.array_split(df,num_splits)
        for i,split_df in enumerate(split_dfs):
            print("The timeframe",timeframe)
            print(f"The {i+1} dataframe is")
            print(split_df)
            getHighLowPricesPerSplitDf(split_df,pair,timeframe)

def getHighLowPricesPerSplitDf(split_df,pair,timeframe):
    split_df=pd.DataFrame(split_df)
    highClosePrice=math.floor(split_df["close"].max())
    lowClosePrice=math.floor(split_df["close"].min())
    highPrice =math.floor(split_df["high"].max())
    lowPrice=math.floor(split_df["low"].min())

    # wick analysis
    bearish_PinBar=highPrice-highClosePrice
    bullish_PinBar=lowPrice-lowClosePrice

    print(f"the {pair} has a max price of {highClosePrice} and a low price of {lowClosePrice} at the {timeframe} minute timeframe")
    if(pair == "XAUUSD"):
        xauusd_Dict[timeframe]["highPrice"].append(highClosePrice)
        xauusd_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "EURUSD"):
        eurusd_Dict[timeframe]["highPrice"].append(highClosePrice)
        eurusd_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "USDCAD"):
        usdcad_Dict[timeframe]["highPrice"].append(highClosePrice)
        usdcad_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "USDJPY"):
        usdjpy_Dict[timeframe]["highPrice"].append(highClosePrice)
        usdjpy_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "AUDCAD"):
        audcad_Dict[timeframe]["highPrice"].append(highClosePrice)
        audcad_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "GBPUSD"):
        gbpusd_Dict[timeframe]["highPrice"].append(highClosePrice)
        gbpusd_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "GBPJPY"):
        gbpjpy_Dict[timeframe]["highPrice"].append(highClosePrice)
        gbpjpy_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    elif(pair == "EURJPY"):
        eurjpy_Dict[timeframe]["highPrice"].append(highClosePrice)
        eurjpy_Dict[timeframe]["lowPrice"].append(lowClosePrice)
    
    windowToWindowAnalysis(xauusd_Dict,pair)
    
    

def windowToWindowAnalysis(price_Dict,pair):
    if(pair == "XAUUSD"):
        # max price analysis for the same timeframe
        for counter,price in enumerate(price_Dict[30]["highPrice"]):
            if(price in price_Dict[15]["highPrice"] or price in price_Dict[5]["highPrice"] or price in price_Dict[1]["highPrice"]):
                print("We have a high point",price)
                cont_xauusd_Dict["highPrice"].append(price)
            
        for counter,price in enumerate(price_Dict[30]["lowPrice"]):
            if(price in price_Dict[15]["lowPrice"] or price_Dict[5]["lowPrice"] or price_Dict[1]["lowPrice"]):
                print("We have a low point",price)            
                cont_xauusd_Dict["lowPrice"].append(price)
    
        # since we have price points that are repetitive, lets get the current price and see whether it is close to any of the points
        isPriceCloseToAnySweetSpot(pair)

def isPriceCloseToAnySweetSpot(pair):
    while True:
        tick =mt5.symbol_info_tick(pair)
        print(f"The price for {pair} is currently {tick.bid}")
        if(math.floor(tick.bid) in cont_xauusd_Dict["highPrice"] or math.floor(tick.ask) in cont_xauusd_Dict["lowPrice"]):
            print("We have a price on our sweet spot")
            # if there is price on our sweet spot, then we check for other signals for entry
        time.sleep(5)
# calculating the SMA
def calculateSMA(fast_sma,prev_fast_sma,slow_sma): 
    """
      The main logic behind sma crossover is that if the previous fast_sma is lesser than the current 
      slow_sma this means that the is a bullish crossover which signifies a buy signal 
      And the converse is also True
    """
    # logic
    if fast_sma>slow_sma and prev_fast_sma< slow_sma:
        return "bullish_crossover"

    elif fast_sma<slow_sma and prev_fast_sma >slow_sma:
        return "bearish_crossover"
    
# calculate the RSI
def calculateRSI(df,TIMEFRAMEs):
    close_delta=df["close"].diff()
    # make two series: one for lower closes and one for higher closes
    up=close_delta.clip(lower=0)
    down=-1*close_delta.clip(upper=0)

    # setting the RSI period
    rsi_period=14
    # to calculate RSI, we first need to calculate the simple weighted average gain and loss during the period
    df['gain']=(df['close']-df['open']).apply(lambda x: x if x>0 else 0)
    df['loss']=(df['close']-df['open']).apply(lambda x: -x if x<0 else 0)
    # we calculate the exponential moving average
    # df["ema_gain"]=up.rolling(rsi_period).mean()
    # df["ema_loss"]=down.rolling(rsi_period).mean()
    df["ema_gain"]=df["gain"].ewm(span=rsi_period,min_periods=rsi_period).mean()
    df["ema_loss"]=df["loss"].ewm(span=rsi_period,min_periods=rsi_period).mean()
    """
      Calculating the SMA for the symbol in the minute timeframe
    """
    # calculating the simple moving average
    df["fast_sma"]=df["close"].rolling(FSMA_PERIOD).mean()
    df["slow_sma"]=df["close"].rolling(SL_SMA_PERIOD).mean()
    # calculate the previous SMA
    df["prev_fast_sma"]=df["fast_sma"].shift(1)
    # crossover column
    df=df.fillna(0)
    df["crossover"]= np.vectorize(calculateSMA)(df["fast_sma"],df["prev_fast_sma"],df["slow_sma"])
    # the Relative strength is gotten by dividing the exponential average gain witb the exponential average loss
    df['RS']=df['ema_gain']/df['ema_loss']
    # the RSI is calculated based on the RS using the following formula
    df['rd_14']=100-(100/(df['RS']+1))
    # print(df)
    
    # define the ATR period
    atr_period=14
    # calculating the range of each candle
    df['range']=df['high']-df['low']
    # calculating the average value of ranges
    df['atr_14']=df['range'].rolling(atr_period).mean()
    # print(df)
    atr=df.iloc[-1]["atr_14"]
    rd_14=df.iloc[-1]["rd_14"]
    """
     Calculate the RSI divergence by getting the max RSI and min RSI in the periods
     Then call the getDivergence() function
    """
    data1=df[df["rd_14"] >= 70]
    highRSI=pd.DataFrame(data=data1)[["rd_14","close"]]
    # filter to the last 20 bars
    
    # print("HIGH RSI DATAFRAME ")
    # print(highRSI.tail(20))
    current_price=df.iloc[-1]["close"]
    previous_price=df.iloc[-2]["close"]

    
    # low RSI dataframe
    data=df[df["rd_14"] <=30]
    lowRSI=pd.DataFrame(data=data)[["rd_14","close"]]
    # print("LOW RSI DATAFRAME ")
    # print(lowRSI.tail(20))
    getDivergence(highRSI,lowRSI,TIMEFRAMEs)

# get the bullish and bearish divergence
def getDivergence(highRSI,lowRSI,TIMEFRAMEs):
    global trade_signal
    # print("LOW RSI")
    # print(lowRSI)

    # HIGH PRICE
    current_high_rsi=highRSI.iloc[-1]["rd_14"]
    current_close_low=lowRSI.iloc[-1]["close"]
    current_close_high=highRSI.iloc[-1]["close"]
    previous_high_rsi=highRSI.iloc[-2]["rd_14"]
    previous_close_high=highRSI.iloc[-2]["close"]
    previous_close_low=lowRSI.iloc[-2]["close"]
    # highest price
    highest_price =highRSI.loc[highRSI["close"]==highRSI["close"].max()]
    highest_price=highest_price.iloc[-1]["close"]
    current_low_rsi=lowRSI.iloc[-1]["rd_14"]
    previous_low_rsi=lowRSI.iloc[-2]["rd_14"]   

    # logic
    """
    if current_close_high is in the range of the previous_close_high or higher than it
    And the current high rsi is lower than the previous high rsi, then there is a bearish divergence
    THE CONVERSE OF THE ABOVE ALSO APPLIES 
    """
    higher_side =current_close_high-0.8
    lower_side =current_close_low -0.8
    
    if higher_side >= previous_close_high and current_high_rsi<previous_high_rsi:
        trade_signal="sell"     
         
    elif lower_side >= previous_close_low and current_low_rsi>previous_low_rsi:
        trade_signal="buy"

    # print("The gold dictionary")
    # print(f"The {timeframe} timeframe has a maximum price of {highClosePrice} and minimum price of {lowClosePrice}")
    # print(xauusd_Dict)

def main():
    conn()

if __name__ == "__main__":
    main()