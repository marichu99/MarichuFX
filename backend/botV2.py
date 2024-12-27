import MetaTrader5 as mt5
from datetime import datetime
import time
import pandas as pd
import numpy as np
from threading import Thread
from tradenotifier import send_email_notification
import sys
import math
import json
import os
import asyncio


# global variables
SYMBOLS = ["XAUUSD", "EURUSD", "USDCAD", "USDJPY",
           "AUDCAD", "GBPUSD", "GBPJPY", "EURJPY"]
SYMBOLZ = ["XAUUSD", "EURUSD", "USDCAD", "USDJPY",
           "AUDCAD", "GBPUSD", "GBPJPY", "EURJPY"]
TIMEFRAME = mt5.TIMEFRAME_M15
high_TIMEFRAME = [mt5.TIMEFRAME_M30, mt5.TIMEFRAME_M15,
                  mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4]
lower_TIMEFRAMES = [mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M5,
                    mt5.TIMEFRAME_M15, mt5.TIMEFRAME_M30]
extremelyHigh_TIMEFRAMES=[mt5.TIMEFRAME_D1]
all_TIMEFRAMES = high_TIMEFRAME+lower_TIMEFRAMES
NUM_BARS = 1000
VOLUME = 0.1
DEVIATION = 20  # deviation for order slippage
MAGIC = 10
FSMA_PERIOD = 10  # number of periods in the fast simple moving average
SL_SMA_PERIOD = 50  # number of periods in the slow moving average
# number of deviations for calculation of bolinger bands
STANDARD_DEVIATIONS = int(2)


# window formation
xauusd_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
btcusd_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
eurusd_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
usdcad_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
usdjpy_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
audcad_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
gbpusd_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
gbpjpy_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}
eurjpy_Dict = {1: {"highPrice": [], "lowPrice": []}, 5: {"highPrice": [], "lowPrice": []}, 15: {"highPrice": [], "lowPrice": [
]}, 30: {"highPrice": [], "lowPrice": []}, 16385: {"highPrice": [], "lowPrice": []}, 16388: {"highPrice": [], "lowPrice": []}}


# contentious price points
cont_xauusd_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_btcusd_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_eurusd_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_usdcad_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_usdjpy_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_audcad_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_gbpusd_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_gbpjpy_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}
cont_eurjpy_Dict = {"highPrice": [], "lowPrice": [],
                    "confirmedPrice": [], "highPriceRSI": [], "lowPriceRSI": []}

#an array of dictionaries
trendAnalysisDicts=[]

ema_20 = []
ema_5 = []


def conn():
    # start the connection to MT5
    resu = {
        "Response": 200,
        "Message": "Data from python"
    }
    # resu["server"]=server
    valid_conn = mt5.initialize()
    # check if the connection went through
    if not (valid_conn):
        resu["init_err"] = mt5.last_error()
    # login into your account
    login = mt5.login(36610, "Marichu12", "EGMSecurities-Demo")
    if not login:
        resu["login_err"] = mt5.last_error()
    else:
        resu["Message"] = "Login is Successful"
        print("the login was successful")
        with open("data.json", "w") as dataF:
            json.dump(resu, dataF)
        gatherDataController()


def gatherDataController():
    print("We are gathering the data")
    global lower_TIMEFRAMES, high_TIMEFRAME, all_TIMEFRAMES, SYMBOLS, SYMBOLZ
    print([x for x in high_TIMEFRAME])
    for pair in SYMBOLS:
        for timeframe in all_TIMEFRAMES:
            backtest_data = mt5.copy_rates_from_pos(
                pair, timeframe, 1, NUM_BARS)
            bars = pd.DataFrame(backtest_data)
            # save the data into a dataframe
            comprehensive_name = f"{str(pair)}{str(timeframe)}"

            price = bars.iloc[-1]["close"]

            print(f"The price is {price} for {pair} at the {timeframe} timeframe")

            # Define the directory path
            directory = 'backend/backtest'

            # Check if the directory exists, and create it if it does not
            if not os.path.exists(directory):
                os.makedirs(directory)
                bars.to_csv(rf".\backend\backtest\{comprehensive_name}.csv")
            else:
                bars.to_csv(rf".\backend\backtest\{comprehensive_name}.csv")

            # pass the dataframe to another method for further pre-processing
            splitAndPreprocess(bars, str(pair), timeframe)
            # since we have price points that are repetitive, lets get the current price and see whether it is close to any of the points
            # larger scale of things

        

    while True:
        for pair in SYMBOLS:
            isTrending=False
            for timeFrame in extremelyHigh_TIMEFRAMES:
                # the range below is number of bars we excpect the chart to be trending
                range=50
                backtest_data = mt5.copy_rates_from_pos(pair, timeframe, 1, range)
                bars = pd.DataFrame(backtest_data)
                trendAnalysis(pair,bars,timeFrame,range)
            # enforce we only trade trends
            for trend in trendAnalysisDicts:
                trend= dict(trend)
                if(trend["pair"] == pair and str(trend["final_trend"]).startswith("Confirmed")):
                    isTrending=True
                    break
            #if(isTrending):
            if (isPriceCloseToAnySweetSpot(pair)):
                time.sleep(3)
                break

def trendAnalysis(pair, df, timeframe, range_period=200):
    """
    Analyze the trend for a given trading pair and timeframe using both SMA, EMA, and price action (higher highs, lower lows)
    over a specified range of candles (default 200) to detect trend reversals and price action patterns.
    
    Args:
        pair (str): The trading pair (e.g., "EUR/USD").
        df (pd.DataFrame): The data containing OHLC (Open, High, Low, Close) and time columns.
        timeframe (str): The timeframe for analysis (e.g., "1h", "4h", "1d").
        range_period (int): The number of candles over which to check higher highs/lower lows (default is 200).
    
    Returns:
        dict: A dictionary containing trend information, including moving averages, price action analysis, and final trend.
    """
    # Ensure the dataframe has the required columns

    df = pd.DataFrame(df)
    required_columns = {'open', 'high', 'low', 'close'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"DataFrame must contain the following columns: {required_columns}")
    
    # Calculate Moving Averages
    df['SMA_200'] = df['close'].rolling(window=200).mean()  # 200-period Simple Moving Average
    df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()  # 50-period Exponential Moving Average

    # Determine trend based on SMA and EMA
    ma_trend = ""
    if df['EMA_50'].iloc[-1] > df['SMA_200'].iloc[-1]:
        ma_trend = "Uptrend"
    elif df['EMA_50'].iloc[-1] < df['SMA_200'].iloc[-1]:
        ma_trend = "Downtrend"
    else:
        ma_trend = "Sideways"
    
    # Check for higher highs and higher lows over the last 'range_period' candles
    highest_high = df['high'].iloc[-range_period:].max()  # Highest high in the last 'range_period' candles
    lowest_low = df['low'].iloc[-range_period:].min()    # Lowest low in the last 'range_period' candles
    
    # Check for if the highs and lows are making higher or lower points over the range
    higher_highs = df['high'].iloc[-range_period:].is_monotonic_increasing  # Check if highs are increasing
    higher_lows = df['low'].iloc[-range_period:].is_monotonic_increasing  # Check if lows are increasing
    lower_highs = df['high'].iloc[-range_period:].is_monotonic_decreasing  # Check if highs are decreasing
    lower_lows = df['low'].iloc[-range_period:].is_monotonic_decreasing  # Check if lows are decreasing

    # Determine if the price is making higher highs and higher lows (uptrend) or lower highs and lower lows (downtrend)
    price_action_trend = ""
    if higher_highs and higher_lows:
        price_action_trend = "Uptrend (Higher Highs and Higher Lows)"
    elif lower_highs and lower_lows:
        price_action_trend = "Downtrend (Lower Highs and Lower Lows)"
    else:
        price_action_trend = "Sideways (No clear higher highs/lows or lower highs/lows)"

    # Combine trend from moving averages and price action analysis
    final_trend = ""
    if ma_trend == "Uptrend" and price_action_trend.startswith("Uptrend"):
        final_trend = "Confirmed Uptrend"
    elif ma_trend == "Downtrend" and price_action_trend.startswith("Downtrend"):
        final_trend = "Confirmed Downtrend"
    elif price_action_trend == "Sideways (No clear higher highs/lows or lower highs/lows)" and ma_trend == "Sideways":
        final_trend = "Sideways (No Clear Trend)"
    else:
        final_trend = "Possible Reversal or Consolidation"

    # Create a dictionary with all relevant information for easy lookup
    trend_info = {
        "pair": pair,
        "timeframe": timeframe,
        "ma_trend": ma_trend,
        "price_action_trend": price_action_trend,
        "final_trend": final_trend,
        "highest_high": highest_high,
        "lowest_low": lowest_low,
        "range_period": range_period
    }

    # Log the result for this pair
    #print(f"{pair} ({timeframe}): Trend based on MA is {ma_trend}")
    #print(f"Price action analysis: {price_action_trend}")
    #print(f"Final trend analysis: {final_trend}")
    trendAnalysisDicts.append(trend_info)

    return trend_info


def splitAndPreprocess(df, pair, timeframe):
    df = pd.DataFrame(df)
    num_splits = df.shape[0]/100
    split_dfs = np.array_split(df, num_splits)

    for i, split_df in enumerate(split_dfs):
        getHighLowPricesPerSplitDf(split_df, pair, timeframe)


def getCrossOver(df):
    df = pd.DataFrame(df)
    # change the time variable
    df["time"] = pd.to_datetime(df["time"], unit="s")

    df['fast_ema'] = df['close'].ewm(span=5, adjust=False).mean()
    df['slow_ema'] = df['close'].ewm(span=20, adjust=False).mean()

    df['prev_fast_ema'] = df['fast_ema'].shift(1)
    df['prev_slow_ema'] = df['slow_ema'].shift(1)

    df = df.fillna(0)

    df['crossover'] = np.vectorize(calculate_ema_crossover)(
        df['fast_ema'], df['prev_fast_ema'], df['slow_ema'], df['prev_slow_ema'])

    cross_over_type = df.iloc[-1]["crossover"]

    return cross_over_type


def getHighLowPricesPerSplitDf(split_df, pair, timeframe):
    split_df = pd.DataFrame(split_df)
    highClosePrice = (split_df["close"].max())
    lowClosePrice = (split_df["close"].min())
    highPrice = (split_df["high"].max())
    lowPrice = (split_df["low"].min())

    # wick analysis
    bearish_PinBar = highPrice-highClosePrice
    bullish_PinBar = lowPrice-lowClosePrice

    if (pair == "XAUUSD"):
        xauusd_Dict[timeframe]["highPrice"].append(math.floor(highClosePrice))
        xauusd_Dict[timeframe]["lowPrice"].append(math.floor(lowClosePrice))
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(xauusd_Dict, pair, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(xauusd_Dict, pair, 30, 15, 5, False)
    if (pair == "BTCUSD"):
        btcusd_Dict[timeframe]["highPrice"].append(math.floor(highClosePrice))
        btcusd_Dict[timeframe]["lowPrice"].append(math.floor(lowClosePrice))
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(btcusd_Dict, pair, mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(btcusd_Dict, pair, 30, 15, 5, False)
    elif (pair == "EURUSD"):
        eurusd_Dict[timeframe]["highPrice"].append(highClosePrice)
        eurusd_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(eurusd_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(eurusd_Dict, pair, 30, 15, 5, False)
    elif (pair == "USDCAD"):
        usdcad_Dict[timeframe]["highPrice"].append(highClosePrice)
        usdcad_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(usdcad_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(usdcad_Dict, pair, 30, 15, 5, False)
    elif (pair == "USDJPY"):
        usdjpy_Dict[timeframe]["highPrice"].append(highClosePrice)
        usdjpy_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(usdjpy_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(usdjpy_Dict, pair, 30, 15, 5, False)
    elif (pair == "AUDCAD"):
        audcad_Dict[timeframe]["highPrice"].append(highClosePrice)
        audcad_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(audcad_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(audcad_Dict, pair, 30, 15, 5, False)
    elif (pair == "GBPUSD"):
        gbpusd_Dict[timeframe]["highPrice"].append(highClosePrice)
        gbpusd_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(gbpusd_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(gbpusd_Dict, pair, 30, 15, 5, False)
    elif (pair == "GBPJPY"):
        gbpjpy_Dict[timeframe]["highPrice"].append(highClosePrice)
        gbpjpy_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(gbpjpy_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(gbpjpy_Dict, pair, 30, 15, 5, False)
    elif (pair == "EURJPY"):
        eurjpy_Dict[timeframe]["highPrice"].append(highClosePrice)
        eurjpy_Dict[timeframe]["lowPrice"].append(lowClosePrice)
        if (timeframe in high_TIMEFRAME):
            windowToWindowAnalysis(eurjpy_Dict, pair,  mt5.TIMEFRAME_H4, mt5.TIMEFRAME_H1, 30, True)
        else:
            windowToWindowAnalysis(eurjpy_Dict, pair, 30, 15, 5, False)


def windowToWindowAnalysis(price_Dict, pair, comparator, firstLower, secondLower, populateConfirmed=False):
    
    tolerance = int(0)
    
    # set the tolerance according to the different pairs
    if("JPY" in pair):
        tolerance = 0.03
    else:
        tolerance = 0.003
    # max price analysis for the same timeframe
    for counter, price in enumerate(price_Dict[comparator]["highPrice"]):
        # price=math.floor(price)
        def is_within_range(price, target_prices, tolerance):
            return any(abs(price - target) <= tolerance for target in target_prices)
        if (
                is_within_range(price, price_Dict[firstLower]["highPrice"], tolerance=tolerance) or
                is_within_range(
                    price, price_Dict[secondLower]["highPrice"], tolerance=tolerance)
        ):
            if (pair == "XAUUSD"):
                if populateConfirmed == False and price not in cont_xauusd_Dict["highPrice"]:
                    cont_xauusd_Dict["highPrice"].append(price)
                elif price not in cont_xauusd_Dict["confirmedPrice"]:
                    cont_xauusd_Dict["confirmedPrice"].append(price)
            elif (pair == "BTCUSD"):
                if populateConfirmed == False and price not in cont_btcusd_Dict["highPrice"]:
                    cont_btcusd_Dict["highPrice"].append(price)
                elif price not in cont_btcusd_Dict["confirmedPrice"]:
                    cont_btcusd_Dict["confirmedPrice"].append(price)
            elif (pair == "EURUSD"):
                if populateConfirmed == False and price not in cont_eurusd_Dict["highPrice"]:
                    cont_eurusd_Dict["highPrice"].append(price)
                elif price not in cont_eurusd_Dict["confirmedPrice"]:
                    cont_eurusd_Dict["confirmedPrice"].append(price)
            elif (pair == "EURJPY"):
                if populateConfirmed == False and price not in cont_eurjpy_Dict["highPrice"]:
                    cont_eurjpy_Dict["highPrice"].append(price)
                elif price not in cont_eurjpy_Dict["confirmedPrice"]:
                    cont_eurjpy_Dict["confirmedPrice"].append(price)
            elif (pair == "AUDCAD"):
                if populateConfirmed == False and price not in cont_audcad_Dict["highPrice"]:
                    cont_audcad_Dict["highPrice"].append(price)
                elif price not in cont_audcad_Dict["confirmedPrice"]:
                    cont_audcad_Dict["confirmedPrice"].append(price)
            elif (pair == "USDCAD"):
                if populateConfirmed == False and price not in cont_usdcad_Dict["highPrice"]:
                    cont_usdcad_Dict["highPrice"].append(price)
                elif price not in cont_usdcad_Dict["confirmedPrice"]:
                    cont_usdcad_Dict["confirmedPrice"].append(price)
            elif (pair == "GBPUSD"):
                if populateConfirmed == False and price not in cont_gbpusd_Dict["highPrice"]:
                    cont_gbpusd_Dict["highPrice"].append(price)
                elif price not in cont_gbpusd_Dict["confirmedPrice"]:
                    cont_gbpusd_Dict["confirmedPrice"].append(price)
            elif (pair == "GBPJPY"):
                if populateConfirmed == False and price not in cont_gbpjpy_Dict["highPrice"]:
                    cont_gbpjpy_Dict["highPrice"].append(price)
                elif price not in cont_gbpjpy_Dict["confirmedPrice"]:
                    cont_gbpjpy_Dict["confirmedPrice"].append(price)
            elif (pair == "USDJPY"):
                if populateConfirmed == False and price not in cont_usdjpy_Dict["highPrice"]:
                    cont_usdjpy_Dict["highPrice"].append(price)
                elif price not in cont_usdjpy_Dict["confirmedPrice"]:
                    cont_usdjpy_Dict["confirmedPrice"].append(price)
            # rsi,signal=calculateRSI(pair,30)
            # cont_xauusd_Dict["highPriceRSI"].append(rsi)

    for counter, price in enumerate(price_Dict[comparator]["lowPrice"]):
        # price=math.floor(price)
        def is_within_range(price, target_price_arr, tolerance):
            for x in target_price_arr:
                if abs(price - x) <= tolerance:
                    return True
            return False
        if (
            is_within_range(price, price_Dict[firstLower]["lowPrice"], tolerance=tolerance) or
            is_within_range(
                price, price_Dict[secondLower]["lowPrice"], tolerance=0.03)
        ):

            if (pair == "XAUUSD"):
                if populateConfirmed == False and price not in cont_xauusd_Dict["lowPrice"]:
                        cont_xauusd_Dict["lowPrice"].append(price)
                elif price not in cont_xauusd_Dict["confirmedPrice"]:
                    cont_xauusd_Dict["confirmedPrice"].append(price)
            elif (pair == "BTCUSD"):
                if populateConfirmed == False and price not in cont_btcusd_Dict["lowPrice"]:
                        cont_btcusd_Dict["lowPrice"].append(price)
                elif price not in cont_btcusd_Dict["confirmedPrice"]:
                    cont_btcusd_Dict["confirmedPrice"].append(price)
            elif (pair == "EURUSD"):
                if populateConfirmed == False and price not in cont_eurusd_Dict["lowPrice"]:
                        cont_eurusd_Dict["lowPrice"].append(price)
                elif price not in cont_eurusd_Dict["confirmedPrice"]:
                    cont_eurusd_Dict["confirmedPrice"].append(price)
            elif (pair == "EURJPY"):
                if populateConfirmed == False and price not in cont_eurjpy_Dict["lowPrice"]:
                        cont_eurjpy_Dict["lowPrice"].append(price)
                elif price not in cont_eurjpy_Dict["confirmedPrice"]:
                    cont_eurjpy_Dict["confirmedPrice"].append(price)
            elif (pair == "AUDCAD"):
                if populateConfirmed == False and price not in cont_audcad_Dict["lowPrice"]:
                        cont_audcad_Dict["lowPrice"].append(price)
                elif price not in cont_audcad_Dict["confirmedPrice"]:
                    cont_audcad_Dict["confirmedPrice"].append(price)
            elif (pair == "USDCAD"):
                if populateConfirmed == False and price not in cont_usdcad_Dict["lowPrice"]:
                        cont_usdcad_Dict["lowPrice"].append(price)
                elif price not in cont_usdcad_Dict["confirmedPrice"]:
                    cont_usdcad_Dict["confirmedPrice"].append(price)
            elif (pair == "GBPUSD"):
                if populateConfirmed == False and price not in cont_gbpusd_Dict["lowPrice"]:
                        cont_gbpusd_Dict["lowPrice"].append(price)
                elif price not in cont_gbpusd_Dict["confirmedPrice"]:
                    cont_gbpusd_Dict["confirmedPrice"].append(price)
            elif (pair == "GBPJPY"):
                if populateConfirmed == False and price not in cont_gbpjpy_Dict["lowPrice"]:
                        cont_gbpjpy_Dict["lowPrice"].append(price)
                elif price not in cont_gbpjpy_Dict["confirmedPrice"]:
                    cont_gbpjpy_Dict["confirmedPrice"].append(price)
            elif (pair == "USDJPY"):
                if populateConfirmed == False and price not in cont_usdjpy_Dict["lowPrice"]:
                        cont_usdjpy_Dict["lowPrice"].append(price)
                elif price not in cont_usdjpy_Dict["confirmedPrice"]:
                    cont_usdjpy_Dict["confirmedPrice"].append(price)
            # rsi,signal=calculateRSI(pair,30)
            # cont_xauusd_Dict["lowPriceRSI"].append(rsi)


def isPriceCloseToAnySweetSpot(pair):
    global lower_TIMEFRAMES
    for timeframe in lower_TIMEFRAMES:
        tick = mt5.symbol_info_tick(pair)
        print(f"The price for {pair} is currently {tick.bid} at {timeframe} timeframe")
        current_high_price = int(0)
        current_low_price = int(0)
        toleranceLevel = int(0)
        if (pair not in ["XAUUSD", "BTCUSD"]):
            current_high_price = round(tick.bid, 4)
            current_low_price = round(tick.ask, 4)
            toleranceLevel = 0.0002
        elif ("JPY" in str(pair)):
            current_high_price = round(tick.bid, 3)
            current_low_price = round(tick.ask, 3)
            toleranceLevel = 0.02
        else:
            current_high_price = math.floor(tick.bid)
            current_low_price = math.floor(tick.ask)
            toleranceLevel = 2
        rsi, signal = calculateRSI(pair, timeframe)
        # time.sleep(6)
        high_prices, low_prices, confirmed_price = setHighLowPriceBasedOnPair(
            pair)

        # Print each high price
        print(f"The high prices for {pair} {high_prices}")
        print(f"The low prices for {pair} {low_prices}")

        print(f"The confirmed prices for {pair} {confirmed_price}")
        print(current_high_price)
        for price in high_prices:
            # print(f"we have a high price of {price} for the {pair} pair")
            # Check if the price is within the specified range
            if (abs(price-current_high_price) <= toleranceLevel):
                print("We have a price on our higher sweep")
                print(f"The value of the RSI is {rsi} and its {signal} at the {timeframe} timeframe at {pair}")
                if (signal == "sell"):
                    print("We have a complete sell signal")
                    asyncio.run(awaitSupportResistance(tick.ask, pair, timeframe, type="sell"))
                    return True
        for price in low_prices:
            if abs(price-current_low_price) <= 2:
                print("We have price on our lower sweet spot")
                print(f"The value of the RSI is {rsi} and its {signal}")
                if (signal == "buy"):
                    print("We have a complete buy signal")
                    signal_message=f" We have a {signal} signal for the {pair} pair at the {timeframe} timeframe"
                    # send the email with signal notice
                    send_email_notification(f"{pair} TRADING SIGNAL",signal_message)
                    asyncio.run(awaitSupportResistance(tick.ask, pair, timeframe, type="buy"))
                    return True
            # if there is price on our sweet spot, we wait for price to retest our sweet spot
    return False


def setHighLowPriceBasedOnPair(pair):
    if pair == "XAUUSD":
        high_prices = cont_xauusd_Dict["highPrice"]
        low_prices = cont_xauusd_Dict["lowPrice"]
        confirmed_price = cont_xauusd_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "BTCUSD.lv":
        high_prices = cont_btcusd_Dict["highPrice"]
        low_prices = cont_btcusd_Dict["lowPrice"]
        confirmed_price = cont_btcusd_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "EURUSD":
        high_prices = cont_eurusd_Dict["highPrice"]
        low_prices = cont_eurusd_Dict["lowPrice"]
        confirmed_price = cont_eurusd_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "EURJPY":
        high_prices = cont_eurjpy_Dict["highPrice"]
        low_prices = cont_eurjpy_Dict["lowPrice"]
        confirmed_price = cont_eurjpy_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "USDCAD":
        high_prices = cont_usdcad_Dict["highPrice"]
        low_prices = cont_usdcad_Dict["lowPrice"]
        confirmed_price = cont_usdcad_Dict["confirmedPrice"]

        return high_prices, low_prices, confirmed_price
    elif pair == "AUDCAD":
        high_prices = cont_audcad_Dict["highPrice"]
        low_prices = cont_audcad_Dict["lowPrice"]
        confirmed_price = cont_audcad_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "USDJPY":
        high_prices = cont_usdjpy_Dict["highPrice"]
        low_prices = cont_usdjpy_Dict["lowPrice"]
        confirmed_price = cont_usdjpy_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "GBPUSD":
        high_prices = cont_gbpusd_Dict["highPrice"]
        low_prices = cont_gbpusd_Dict["lowPrice"]
        confirmed_price = cont_gbpusd_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price

    elif pair == "GBPJPY":
        high_prices = cont_gbpjpy_Dict["highPrice"]
        low_prices = cont_gbpjpy_Dict["lowPrice"]
        confirmed_price = cont_gbpjpy_Dict["confirmedPrice"]
        return high_prices, low_prices, confirmed_price


async def awaitSupportResistance(price, pair, timeframe, type):
    # Fetch the last 10 candlesticks
    retest_df = mt5.copy_rates_from_pos(pair, timeframe, 0, 10)[
        ["close", "open", "high", "low"]]
    retest_df = pd.DataFrame(retest_df)

    # Calculate ATR, stop loss, and take profit levels
    atr = calculate_atr(retest_df)
    stop_loss, take_profit = calculate_levels(price, atr, type, pair)

    # Define the pattern we are looking for based on the trade type
    pattern_detected = False
    pattern_name = None

    if type == "sell":
        pattern_name = "Bearish Engulfing"
    elif type == "buy":
        pattern_name = "Bullish Engulfing"

    # Wait for the desired pattern to form
    for _ in range(3):  # Waiting for up to 3 candles to form
        time.sleep(300)  # Wait for the next 5-minute candle (300 seconds)

        # Update the retest_df with the latest candle data
        latest_candle = mt5.copy_rates_from_pos(pair, timeframe, 0, 10)[
            ["close", "open", "high", "low"]]
        retest_df = pd.DataFrame(latest_candle)

        # Check for the specific candlestick pattern
        if type == "sell" and detect_bearish_patterns(retest_df):
            print(f"Bearish Engulfing pattern detected. Preparing to sell.")
            pattern_detected = True
            break
        elif type == "buy" and detect_bullish_patterns(retest_df):
            print(f"Bullish Engulfing pattern detected. Preparing to buy.")
            pattern_detected = True
            break
        else:
            print(f"Waiting for {pattern_name} pattern to form...")

    if pattern_detected:
        print(f"Final confirmation made, executing {type} order.")
        print(f"The stop loss is {stop_loss} and the take profit is {take_profit}.")
        market_order(pair, VOLUME, type, DEVIATION,
                     MAGIC, stop_loss, take_profit)
    else:
        print(
            f"No {pattern_name} pattern detected. Exiting without placing a trade.")

# Candlestick pattern detection functions


def detect_bearish_patterns(df):
    # Bearish Engulfing pattern
    if df.iloc[-2]["open"] < df.iloc[-2]["close"] and df.iloc[-1]["open"] > df.iloc[-1]["close"]:
        if df.iloc[-1]["open"] > df.iloc[-2]["close"] and df.iloc[-1]["close"] < df.iloc[-2]["open"]:
            return True

    # shooting star
    candle = df.iloc[-1]
    body_size = abs(candle["close"] - candle["open"])
    upper_shadow = candle["high"] - \
        candle["close"] if candle["close"] > candle["open"] else candle["high"] - candle["open"]
    lower_shadow = candle["open"] - \
        candle["low"] if candle["close"] > candle["open"] else candle["close"] - candle["low"]

    if upper_shadow > 2 * body_size and lower_shadow < body_size:
        return True

    # evening star
    if df.iloc[-3]["close"] > df.iloc[-3]["open"] and df.iloc[-1]["open"] > df.iloc[-1]["close"]:
        if df.iloc[-2]["open"] > df.iloc[-3]["close"] and df.iloc[-2]["close"] < df.iloc[-2]["open"] and df.iloc[-1]["close"] < df.iloc[-3]["open"]:
            return True

    # dark cloud cover
    if len(df) < 2:
        return False
    prev_candle = df.iloc[-2]
    candle = df.iloc[-1]

    if prev_candle["close"] > prev_candle["open"] and candle["open"] > prev_candle["high"]:
        if candle["close"] < prev_candle["midpoint"]:
            return True
    if candle["close"] < prev_candle["close"]:
        return True
    return False


def detect_bullish_patterns(df):
    # Bullish Engulfing pattern
    if df.iloc[-2]["open"] > df.iloc[-2]["close"] and df.iloc[-1]["open"] < df.iloc[-1]["close"]:
        if df.iloc[-1]["open"] < df.iloc[-2]["close"] and df.iloc[-1]["close"] > df.iloc[-2]["open"]:
            return True

    # morning star
    if df.iloc[-3]["open"] > df.iloc[-3]["close"] and df.iloc[-1]["close"] > df.iloc[-1]["open"]:
        if df.iloc[-2]["open"] < df.iloc[-3]["close"] and df.iloc[-2]["close"] < df.iloc[-2]["open"] and df.iloc[-1]["open"] > df.iloc[-2]["close"]:
            return True

    # hammer pattern
    candle = df.iloc[-1]
    body_size = abs(candle["close"] - candle["open"])
    lower_shadow = candle["open"] - \
        candle["low"] if candle["close"] > candle["open"] else candle["close"] - candle["low"]
    upper_shadow = candle["high"] - \
        candle["close"] if candle["close"] > candle["open"] else candle["high"] - candle["open"]

    if lower_shadow > 2 * body_size and upper_shadow < body_size:
        return True

    # piercing line
    prev_candle = df.iloc[-2]
    candle = df.iloc[-1]

    if prev_candle["close"] < prev_candle["open"] and candle["open"] < prev_candle["low"]:
        if candle["close"] > prev_candle["midpoint"] and candle["close"] < prev_candle["open"]:
            return True
    return False


def calculate_atr(df, period=14):
    # Ensure the dataframe is sorted by date
    df = df.sort_index()

    # Calculate True Range (TR)
    df['high-low'] = df['high'] - df['low']
    df['high-prevclose'] = abs(df['high'] - df['close'].shift(1))
    df['low-prevclose'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['high-low', 'high-prevclose', 'low-prevclose']].max(axis=1)

    # Calculate the ATR
    df['ATR'] = df['TR'].rolling(window=period, min_periods=1).mean()

    return df["ATR"].iloc[-1]


def calculate_levels(entry_price, atr, position_type, pair, stop_loss_multiplier=1.5, take_profit_multiplier=3):
    stop_loss = int(0)
    take_profit = int(0)
    if position_type == 'buy':
        if (pair == "XAUUSD"):
            new_stops_low = find_closest(
                entry_price, cont_xauusd_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_xauusd_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "BTCUSD"):
            new_stops_low = find_closest(
                entry_price, cont_btcusd_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_btcusd_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "EURUSD"):
            new_stops_low = find_closest(
                entry_price, cont_eurusd_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_eurusd_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "EURJPY"):
            new_stops_low = find_closest(
                entry_price, cont_eurjpy_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_eurjpy_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "AUDCAD"):
            new_stops_low = find_closest(
                entry_price, cont_audcad_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_audcad_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "USDCAD"):
            new_stops_low = find_closest(
                entry_price, cont_usdcad_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_usdcad_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "GBPUSD"):
            new_stops_low = find_closest(
                entry_price, cont_gbpusd_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_gbpusd_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "GBPJPY"):
            new_stops_low = find_closest(
                entry_price, cont_gbpjpy_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_gbpjpy_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
        elif (pair == "USDJPY"):
            new_stops_low = find_closest(
                entry_price, cont_usdjpy_Dict["lowPrice"])
            stop_loss = new_stops_low - (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_usdjpy_Dict["highPrice"])
            take_profit = new_takes_high + (take_profit_multiplier * atr)
    elif position_type == 'sell':
        if (pair == "XAUUSD"):
            new_stops_low = find_closest(
                entry_price, cont_xauusd_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_xauusd_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "BTCUSD"):
            new_stops_low = find_closest(
                entry_price, cont_btcusd_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_btcusd_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "EURUSD"):
            new_stops_low = find_closest(
                entry_price, cont_eurusd_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_eurusd_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "EURJPY"):
            new_stops_low = find_closest(
                entry_price, cont_eurjpy_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_eurjpy_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "AUDCAD"):
            new_stops_low = find_closest(
                entry_price, cont_audcad_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_audcad_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "USDCAD"):
            new_stops_low = find_closest(
                entry_price, cont_usdcad_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_usdcad_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "GBPUSD"):
            new_stops_low = find_closest(
                entry_price, cont_gbpusd_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_gbpusd_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "GBPJPY"):
            new_stops_low = find_closest(
                entry_price, cont_gbpjpy_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_gbpjpy_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
        elif (pair == "USDJPY"):
            new_stops_low = find_closest(
                entry_price, cont_usdjpy_Dict["highPrice"])
            stop_loss = new_stops_low + (stop_loss_multiplier * atr)
            new_takes_high = find_closest(
                entry_price, cont_usdjpy_Dict["lowPrice"])
            take_profit = new_takes_high - (take_profit_multiplier * atr)
    else:
        raise ValueError("position_type must be 'long' or 'short'")

    return stop_loss, take_profit


def find_closest(target, array):
    closest_value = array[0]
    smallest_difference = abs(target - array[0])

    # Iterate over each element in the array
    for num in array:
        difference = abs(target - num)
        if difference < smallest_difference:
            smallest_difference = difference
            closest_value = num

    return closest_value


def market_order(symbol, volume, order_type, deviation, magic, stoploss, takeprofit):
    tick = mt5.symbol_info_tick(symbol)
    orders = mt5.positions_get()

    order_dict = {"buy": 0, "sell": 1}
    price_dict = {"buy": tick.ask, "sell": tick.bid}
    if order_type == "buy":
        taip = mt5.ORDER_TYPE_BUY
    elif order_type == "sell":
        taip = mt5.ORDER_TYPE_SELL
    price = price_dict[order_type]
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": taip,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "sl": stoploss,
        "tp": takeprofit,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }
    result = mt5.order_send(request)

    print("The order is", orders)
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(
        symbol, volume, price, deviation))
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result.retcode))
        # request the result as a dictionary and display it element by element
        result_dict = result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field, result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field == "request":
                traderequest_dict = result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(
                        tradereq_filed, traderequest_dict[tradereq_filed]))
        print("shutdown() and quit")
    else:
        main()

# signal generating functions


def get_signal(TIMEFRAMEs, pair):
    # bar data
    bars = mt5.copy_rates_from_pos(pair, TIMEFRAMEs, 1, NUM_BARS)
    # converting to dataframe
    df = pd.DataFrame(bars)
    # print(f"The symbol is {J}")
    df = df.tail(20)
    # simple moving average
    sma = df['close'].mean()
    # standard deviation
    sd = df['close'].std()

    # lower bolinger band
    lower_band = sma - STANDARD_DEVIATIONS*sd
    # upper bolinger band
    upper_band = sma + STANDARD_DEVIATIONS*sd

    # last close price
    last_price = df.iloc[-1]["close"]

    # print(f"The last price is {last_price} and upper band is {upper_band} and the lower band is {lower_band}")
    # print(df)
    # finding the signal
    if last_price < lower_band:
        return 'buy', sd
    elif last_price > upper_band:
        return 'sell', sd
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
def calculateSMA(fast_sma, prev_fast_sma, slow_sma):
    """
      The main logic behind sma crossover is that if the previous fast_sma is lesser than the current 
      slow_sma this means that the is a bullish crossover which signifies a buy signal 
      And the converse is also True
    """
    # logic
    if fast_sma > slow_sma and prev_fast_sma < slow_sma:
        return "bullish_crossover"

    elif fast_sma < slow_sma and prev_fast_sma > slow_sma:
        return "bearish_crossover"

# calculate the RSI


def calculateRSI(pair, timeframe):
    df = pd.DataFrame(mt5.copy_rates_from_pos(pair, timeframe, 0, 28))[
        ["close", "open", "high", "low"]]

    close_delta = df["close"].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    rsi_period = 14
    df['gain'] = (df['close'] - df['open']).apply(lambda x: x if x > 0 else 0)
    df['loss'] = (df['close'] - df['open']).apply(lambda x: -x if x < 0 else 0)
    df["ema_gain"] = df["gain"].ewm(
        span=rsi_period, min_periods=rsi_period).mean()
    df["ema_loss"] = df["loss"].ewm(
        span=rsi_period, min_periods=rsi_period).mean()

    df["fast_sma"] = df["close"].rolling(FSMA_PERIOD).mean()
    df["slow_sma"] = df["close"].rolling(SL_SMA_PERIOD).mean()
    df["prev_fast_sma"] = df["fast_sma"].shift(1)
    df = df.fillna(0)
    df["crossover"] = np.vectorize(calculateSMA)(
        df["fast_sma"], df["prev_fast_sma"], df["slow_sma"])

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


def getDivergence(highRSI, lowRSI, TIMEFRAMEs):

    print("We are here now")
    trade_signal = ""

    # HIGH PRICE
    current_high_rsi = highRSI.iloc[-1]["rd_14"]
    current_close_low = lowRSI.iloc[-1]["close"]
    current_close_high = highRSI.iloc[-1]["close"]
    previous_high_rsi = highRSI.iloc[-2]["rd_14"]
    previous_close_high = highRSI.iloc[-2]["close"]
    previous_close_low = lowRSI.iloc[-2]["close"]
    # highest price
    highest_price = highRSI.loc[highRSI["close"] == highRSI["close"].max()]
    highest_price = highest_price.iloc[-1]["close"]
    current_low_rsi = lowRSI.iloc[-1]["rd_14"]
    previous_low_rsi = lowRSI.iloc[-2]["rd_14"]

    # logic
    """
    if current_close_high is in the range of the previous_close_high or higher than it
    And the current high rsi is lower than the previous high rsi, then there is a bearish divergence
    THE CONVERSE OF THE ABOVE ALSO APPLIES 
    """
    higher_side = current_close_high-0.8
    lower_side = current_close_low - 0.8

    # if higher_side >= previous_close_high and current_high_rsi<previous_high_rsi:
    #     trade_signal="sell"

    # elif lower_side >= previous_close_low and current_low_rsi>previous_low_rsi:
    #     trade_signal="buy"

    print("The high rsi ", current_high_rsi)

    if current_high_rsi >= 70 and previous_high_rsi >= 70:
        trade_signal = "sell"
    elif current_low_rsi <= 30 and previous_low_rsi <= 30:
        trade_signal = "buy"

    print("The signal obtained is", trade_signal)

    return trade_signal


def main():
    conn()


if __name__ == "__main__":
    main()
