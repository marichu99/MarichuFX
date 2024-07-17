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
SYMBOLS = ["XAUUSD"]
SYMBOLZ = ["XAUUSD","EURUSD","USDCAD","USDJPY","AUDCAD","GBPUSD","GBPJPY","EURJPY"]
TIMEFRAME = mt5.TIMEFRAME_M15  
high_TIMEFRAME=[mt5.TIMEFRAME_M30,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_H1,mt5.TIMEFRAME_H4]
lower_TIMEFRAMES=[mt5.TIMEFRAME_M1,mt5.TIMEFRAME_M5,mt5.TIMEFRAME_M15,mt5.TIMEFRAME_M30]
NUM_BARS=1000
VOLUME=0.1
DEVIATION =20 # deviation for order slippage
MAGIC =10
FSMA_PERIOD = 10 # number of periods in the fast simple moving average
SL_SMA_PERIOD = 50 # number of periods in the slow moving average
STANDARD_DEVIATIONS=int(2) # number of deviations for calculation of bolinger bands


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
cont_xauusd_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[],"highPriceRSI":[],"lowPriceRSI":[]}
cont_eurusd_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_usdcad_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_usdjpy_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_audcad_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_gbpusd_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_gbpjpy_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}
cont_eurjpy_Dict ={"highPrice":[],"lowPrice":[],"confirmedPrice":[]}

ema_20=[]
ema_5=[]

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
        with open("data.json","w") as dataF:
            json.dump(resu,dataF)
        gatherDataController()

def gatherDataController():
    print("We are gathering the data")
    global  lower_TIMEFRAMES,high_TIMEFRAME,SYMBOLS    
    for pair in SYMBOLS:
        for timeframe in  lower_TIMEFRAMES:
            backtest_data = mt5.copy_rates_from_pos(pair,timeframe,1,NUM_BARS)
            bars = pd.DataFrame(backtest_data)
            # save the data into a dataframe
            comprehensive_name=f"{str(pair)}{str(timeframe)}"

            price=bars.iloc[-1]["close"]

            print(f"The price is {price} for {pair} at the {timeframe} timeframe")

            bars.to_csv(rf"backend\backtest\{comprehensive_name}.csv")
            # pass the dataframe to another method for further pre-processing 
            splitAndPreprocess(bars,str(pair),timeframe)   
            # since we have price points that are repetitive, lets get the current price and see whether it is close to any of the points
    while True:
        if (isPriceCloseToAnySweetSpot(pair)):
            time.sleep(1) 
            break


def splitAndPreprocess(df,pair,timeframe):
    df=pd.DataFrame(df)
    num_splits = df.shape[0]/100
    split_dfs=np.array_split(df,num_splits)

    for i,split_df in enumerate(split_dfs):
        getHighLowPricesPerSplitDf(split_df,pair,timeframe)



def getCrossOver(df):
    df= pd.DataFrame(df)
    # change the time variable
    df["time"]=pd.to_datetime(df["time"],unit="s")

    df['fast_ema'] = df['close'].ewm(span=5, adjust=False).mean()
    df['slow_ema'] = df['close'].ewm(span=20, adjust=False).mean()

    df['prev_fast_ema'] = df['fast_ema'].shift(1)
    df['prev_slow_ema'] = df['slow_ema'].shift(1)

    df=df.fillna(0)

    df['crossover'] = np.vectorize(calculate_ema_crossover)(df['fast_ema'], df['prev_fast_ema'], df['slow_ema'], df['prev_slow_ema'])

    cross_over_type=df.iloc[-1]["crossover"]

    return cross_over_type

def getHighLowPricesPerSplitDf(split_df,pair,timeframe):
    split_df=pd.DataFrame(split_df)
    highClosePrice=(split_df["close"].max())
    lowClosePrice=(split_df["close"].min())
    highPrice =(split_df["high"].max())
    lowPrice=(split_df["low"].min())

    # wick analysis
    bearish_PinBar=highPrice-highClosePrice
    bullish_PinBar=lowPrice-lowClosePrice

    if(pair == "XAUUSD"):
        xauusd_Dict[timeframe]["highPrice"].append(math.floor(highClosePrice))
        xauusd_Dict[timeframe]["lowPrice"].append(math.floor(lowClosePrice))
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
    # max price analysis for the same timeframe
    for counter,price in enumerate(price_Dict[30]["highPrice"]):
        price=math.floor(price)
        if(price in price_Dict[15]["highPrice"] or price in price_Dict[5]["highPrice"] or price in price_Dict[1]["highPrice"]):
            cont_xauusd_Dict["highPrice"].append(price)
            # rsi,signal=calculateRSI(pair,30)
            # cont_xauusd_Dict["highPriceRSI"].append(rsi)

        
    for counter,price in enumerate(price_Dict[30]["lowPrice"]):
        price=math.floor(price)
        if(price in price_Dict[15]["lowPrice"] or price_Dict[5]["lowPrice"] or price_Dict[1]["lowPrice"]):
            cont_xauusd_Dict["lowPrice"].append(price)
            # rsi,signal=calculateRSI(pair,30)
            # cont_xauusd_Dict["lowPriceRSI"].append(rsi)

def isPriceCloseToAnySweetSpot(pair):
    global lower_TIMEFRAMES
    for timeframe in lower_TIMEFRAMES:
        tick =mt5.symbol_info_tick(pair)
        print(f"The price for {pair} is currently {tick.bid} at {timeframe} timeframe")
        current_high_price = math.floor(tick.bid)
        current_low_price = math.floor(tick.ask)
        rsi,signal = calculateRSI(pair,timeframe)
        # time.sleep(6)

        high_prices = cont_xauusd_Dict["highPrice"]
        low_prices = cont_xauusd_Dict["lowPrice"]

        # Print each high price
        for price in high_prices:
            # Check if the price is within the specified range
            if price in range(current_high_price-2, current_high_price+2):
                print("We have a price on our higher sweep")
                print(f"The value of the RSI is {rsi} and its {signal} at the {timeframe} timeframe")

                if(signal == "sell"):
                    print("We have a complete sell signal")
                    awaitSupportResistance(tick.ask,pair,timeframe,type="buy")
                    return True
        for price in low_prices:
            if(price in range(current_low_price-2,current_low_price+2)):
                print("We have price on our lower sweet spot")
                print(f"The value of the RSI is {rsi} and its {signal}")
                if(signal == "buy"):
                    print("We have a complete buy signal")
                    awaitSupportResistance(tick.ask,pair,timeframe,type="buy")
                    return True
            # if there is price on our sweet spot, we wait for price to retest our sweet spot
    return False


def awaitSupportResistance(price,pair,timeframe,type):
    retest_df = mt5.copy_rates_from_pos(pair,timeframe,0,10)[["close","open","high","low"]]
    retest_df = pd.DataFrame(retest_df)

    atr = calculate_atr(retest_df)
    stop_loss,take_profit=calculate_levels(price,atr,type)
    if(type == "sell"):
        if(all(retest_df["close"].iloc[-3:]) < price):
            print("Final confirmation made, we are about to sell")           
            market_order(pair,VOLUME,"sell",DEVIATION,MAGIC,stop_loss,take_profit)
        else:
            print("Possible price is continuing with a specific trend")
            market_order(pair,VOLUME,"sell",DEVIATION,MAGIC,stop_loss,take_profit)
    
    elif(type == "buy"):
        if(all(retest_df["close"].iloc[-3:]) > price):
            print("Final confirmation made, we are about to buy")
            market_order(pair,VOLUME,"sell",DEVIATION,MAGIC,stop_loss,take_profit)
        else:
            print("Possible price is continuing with a specific trend")
            market_order(pair,VOLUME,"sell",DEVIATION,MAGIC,stop_loss,take_profit)

def calculate_atr(df, period=14):
    # Ensure the dataframe is sorted by date
    df = df.sort_index()
    
    # Calculate True Range (TR)
    df['high-low'] = df['High'] - df['Low']
    df['high-prevclose'] = abs(df['High'] - df['Close'].shift(1))
    df['low-prevclose'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['high-low', 'high-prevclose', 'low-prevclose']].max(axis=1)

    # Calculate the ATR
    df['ATR'] = df['TR'].rolling(window=period, min_periods=1).mean()

    return df["ATR"].iloc[-1]

def calculate_levels(entry_price, atr, position_type, stop_loss_multiplier=1.5, take_profit_multiplier=3):
    if position_type == 'buy':
        stop_loss = entry_price - (stop_loss_multiplier * atr)
        take_profit = entry_price + (take_profit_multiplier * atr)
    elif position_type == 'sell':
        stop_loss = entry_price + (stop_loss_multiplier * atr)
        take_profit = entry_price - (take_profit_multiplier * atr)
    else:
        raise ValueError("position_type must be 'long' or 'short'")
    
    return stop_loss, take_profit


def market_order(symbol,volume,order_type,deviation,magic,stoploss,takeprofit):
    tick =mt5.symbol_info_tick(symbol)
    orders=mt5.positions_get()

    order_dict ={"buy":0,"sell":1}
    price_dict ={"buy":tick.ask,"sell":tick.bid}
    if order_type == "buy":
        taip=mt5.ORDER_TYPE_BUY
    elif order_type == "sell":
        taip=mt5.ORDER_TYPE_SELL
    price=price_dict[order_type]
    request ={
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": taip,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "sl":stoploss,
        "tp":takeprofit,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,volume,price,deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE and (orders <1 or orders>4):
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
    else: 
        main()

# signal generating functions   
def get_signal(TIMEFRAMEs,pair):
    # bar data
    bars =mt5.copy_rates_from_pos(pair,TIMEFRAMEs,1,NUM_BARS)
    # converting to dataframe
    df =pd.DataFrame(bars)
    # print(f"The symbol is {J}")
    df=df.tail(20)
    # simple moving average
    sma =df['close'].mean()
    # standard deviation
    sd =df['close'].std()
    
    # lower bolinger band
    lower_band = sma -STANDARD_DEVIATIONS*sd
    # upper bolinger band
    upper_band = sma +STANDARD_DEVIATIONS*sd

    # last close price
    last_price =df.iloc[-1]["close"]

    # print(f"The last price is {last_price} and upper band is {upper_band} and the lower band is {lower_band}")
    # print(df)
    # finding the signal
    if last_price <lower_band: 
        return 'buy',sd
    elif last_price > upper_band:
        return 'sell',sd
    else: 
        return None, None

def calculate_ema_crossover(fast_ema, prev_fast_ema, slow_ema, prev_slow_ema):
    if prev_fast_ema < prev_slow_ema and fast_ema > slow_ema:
        return 'Golden Cross'
    elif prev_fast_ema > prev_slow_ema and fast_ema < slow_ema:
        return 'Death Cross'
    else:
        return 'No Crossover'


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
def calculateRSI(pair,timeframe):
    df = pd.DataFrame(mt5.copy_rates_from_pos(pair, timeframe, 0, 1000))[["close", "open", "high", "low"]]

    close_delta = df["close"].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    rsi_period = 14
    df['gain'] = (df['close'] - df['open']).apply(lambda x: x if x > 0 else 0)
    df['loss'] = (df['close'] - df['open']).apply(lambda x: -x if x < 0 else 0)
    df["ema_gain"] = df["gain"].ewm(span=rsi_period, min_periods=rsi_period).mean()
    df["ema_loss"] = df["loss"].ewm(span=rsi_period, min_periods=rsi_period).mean()

    df["fast_sma"] = df["close"].rolling(FSMA_PERIOD).mean()
    df["slow_sma"] = df["close"].rolling(SL_SMA_PERIOD).mean()
    df["prev_fast_sma"] = df["fast_sma"].shift(1)
    df = df.fillna(0)
    df["crossover"] = np.vectorize(calculateSMA)(df["fast_sma"], df["prev_fast_sma"], df["slow_sma"])

    df['RS'] = df['ema_gain'] / df['ema_loss']
    df['rd_14'] = 100 - (100 / (df['RS'] + 1))

    atr_period = 14
    df['range'] = df['high'] - df['low']
    df['atr_14'] = df['range'].rolling(atr_period).mean()

    atr = df.iloc[-1]["atr_14"]
    rd_14 = df.iloc[-1]["rd_14"]

    data1 = df[df["rd_14"] >= 70]
    highRSI = pd.DataFrame(data=data1)[["rd_14", "close"]]

    current_price = df.iloc[-1]["close"]
    previous_price = df.iloc[-2]["close"]

    data = df[df["rd_14"] <= 30]
    lowRSI = pd.DataFrame(data=data)[["rd_14", "close"]]

    print(f"The RSI for {timeframe} tf is", rd_14)

    if rd_14 >= 70 and timeframe in [mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30]:
        signal = "sell"
    elif rd_14 <= 30 and timeframe in [mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30]:
        signal = "buy"
    else:
        signal = "none"

    return rd_14, signal

# get the bullish and bearish divergence
def getDivergence(highRSI,lowRSI,TIMEFRAMEs):

    print("We are here now")
    trade_signal=""

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
    
    # if higher_side >= previous_close_high and current_high_rsi<previous_high_rsi:
    #     trade_signal="sell"     
         
    # elif lower_side >= previous_close_low and current_low_rsi>previous_low_rsi:
    #     trade_signal="buy"

    print("The high rsi ",current_high_rsi)

    if current_high_rsi >=70 and previous_high_rsi >=70:
        trade_signal="sell"
    elif current_low_rsi <=30 and previous_low_rsi<=30:
        trade_signal="buy"
    
    print("The signal obtained is", trade_signal)

    return trade_signal

def main():
    conn()

if __name__ == "__main__":
    main()