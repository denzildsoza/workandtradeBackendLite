from datetime import timedelta,date,datetime
from calendar import day_name
import pandas as pd
from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
# from constants import clientId, secretKey, redirectUrl, code, state ,grantType,fyerslogpath
from Utils import getPreviousSwingSupport,getPreviousSwingResistance
import requests
# sym_details = pd.read_csv("https://public.fyers.in/sym_details/NSE_FO.csv")
# sym_details.columns =  ['epoch_time','symbol_name','o','h','c','l','exg_time','date','expirtDate','symbol','10','11','underlying_price','underlyingName','underlying','strikePrice','callOrPut','abc','None']

# for i in range(8):
#     my_date = date.today()+timedelta(i)
#     a = day_name[my_date.weekday()]
#     if a == 'Thursday':
#         expiry_date = my_date
#         break

# expiry_date_epoch =  int((datetime.strptime(f'{expiry_date} 20:00:00', '%Y-%m-%d %H:%M:%S')).timestamp())
# sym_details_temp = sym_details.loc[sym_details['expiry_date'] == expiry_date_epoch]

# print (expiry_date)
def custom_message(msg):
    print(msg) 



accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTMwNzA0ODksImV4cCI6MTY5MzA5NjIyOSwibmJmIjoxNjkzMDcwNDg5LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazZqU1pScHVJQXRqQWdHTzRRUGtiTkJSVllSdTFibFRqZXJ3WDYzTUVmQzFGY0c4dkREcDlRMi1XRENBTTNpNGxFbGJnNmx0Q18xR254NXVCMy1uWXB5VWwxRjA3b0Z6SjUyN0JHM1ZqSzFiZGVvdz0iLCJkaXNwbGF5X25hbWUiOiJERU5aSUwgRFNPVVpBIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjVkOTdlYTE1YmY5MWRhMzUxOTJmODUzZTNiNWQ2YTEwMGQyYzc2OTEwMTk3MjIyZWVlZjY5ZjIiLCJmeV9pZCI6IlhEMDg2ODUiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.p3DbgWe-9euVYOpV8_6d1Fe0-2Xkh7UOcLhQesCO7yI"

# wsAccessToken = f"3H021OQ8ZI-100:{accessToken}"
# Fyers = fyersModel.FyersModel(
#     client_id=clientId, token=accessToken, log_path=""
# )

# def onOpen():
#     print("connected")
#     FyersWS.subscribe(symbols=["MCX:GOLDM23SEPFUT"],data_type="symbolData")
#     FyersWS.keep_running()
# def onerror(message):
#     print("Error While Connecting to Websocket:", message)


# def onclose(message):
#     print("Connection with server closed:", message)

# FyersWS = data_ws.FyersDataSocket(
#     access_token=wsAccessToken,  # Access token in the format "appid:accesstoken"
#     log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
#     litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
#     write_to_file=False,  # Save response in a log file instead of printing it.
#     reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
#     on_connect=onOpen,  # Callback function to subscribe to data upon connection.
#     on_close=onclose,  # Callback function to handle WebSocket connection close events.
#     on_error=onerror,  # Callback function to handle WebSocket errors.
#     on_message=custom_message,  # Callback function to handle incoming messages from the WebSocket.
# )

# FyersWS.connect()
array = []
# array.append(createOrderArray("abc",19552,'NSE:NIFTY50-INDEX'))
# array.append(createOrderArray("abc",58412,'MCX:GOLDM23SEPFUT'))
# array.append(createOrderArray("abc",6531,'MCX:CRUDEOIL23SEPFUT'))
# array.append(createOrderArray("abc",6524,'MCX:CRUDEOIL23SEPFUT'))
# array.append(createOrderArray("abc",6526,'MCX:CRUDEOIL23SEPFUT'))
# array.append(createOrderArray("abc",6527,'MCX:CRUDEOIL23SEPFUT'))
# array.append(createOrderArray("abc",6528,'MCX:CRUDEOIL23SEPFUT'))
# array.append(createOrderArray("abc",58400,'MCX:GOLDM23SEPFUT'))
# array.append(createOrderArray("abc",58437,'MCX:GOLDM23SEPFUT'))

def checkBreakoutEvent(data):
    global array
    arrayFiltered = [order for order in array if order["underlyingSymbol"] == data["symbol"]]
    for order in arrayFiltered:
        if data["ltp"] >= order["limits"][1] and data["ltp"] <= order["limits"][0]:
            print(data["ltp"],order["limits"][0],order["limits"][1])
            print("orderPlaced")


def onerror(message):
    """
    Callback function to handle WebSocket errors.

    Parameters:
        message (dict): The error message received from the WebSocket.


    """
    print("Error:", message)


def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)


def onopen():

    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.

    """
    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # Subscribe to the specified symbols and data typeMCX:GOLDM23SEPFUT
    symbols=["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX"]

    # symbols=["MCX:GOLDM23SEPFUT","MCX:CRUDEOIL23SEPFUT"]
    # fyers.subscribe(symbols=symbols, data_type=data_type)

    # Keep the socket running to receive real-time data


# Replace the sample access token with your actual access token obtained from Fyers
access_token = accessToken

# Create a FyersDataSocket instance with the provided parameters
# fyers = data_ws.FyersDataSocket(
#     access_token=access_token,       # Access token in the format "appid:accesstoken"
#     log_path="",                     # Path to save logs. Leave empty to auto-create logs in the current directory.
#     litemode=True,                  # Lite mode disabled. Set to True if you want a lite response.
#     write_to_file=False,              # Save response in a log file instead of printing it.
#     reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
#     on_connect=onopen,               # Callback function to subscribe to data upon connection.
#     on_close=onclose,                # Callback function to handle WebSocket connection close events.
#     on_error=onerror,                # Callback function to handle WebSocket errors.
#     on_message=checkBreakoutEvent             # Callback function to handle incoming messages from the WebSocket.
# )

# # # Establish a connection to the Fyers WebSocket
# fyers.connect()
# '''Response: {'type': 'sub', 'code': 200, 'message': 'Subscribed', 's': 'ok'}
# Response: {'ltp': 6742.0, 'symbol': 'MCX:CRUDEOIL23SEPFUT', 'type': 'sf'}
# Response: {'ltp': 58170.0, 'symbol': 'MCX:GOLDM23SEPFUT', 'type': 'sf'}
# Response: {'ltp': 6740.0, 'symbol': 'MCX:CRUDEOIL23SEPFUT', 'type': 'sf'}'''

# print(createOrderArray("abc",58414,'MCX:GOLDM23SEPFUT'))
# def checkBreakoutEvent(data,array):
#     arrayFiltered = [order for order in array if order["underlyingSymbol"] == data["symbol"]]
#     for order in arrayFiltered:
#         if data.ltp >= order["limits"][0] and data.ltp <= order["limits"][0]:
#             print("orderPlaced")
data = {
    "symbol":"NSE:TATAPOWER-EQ",
    "resolution":"15",
    "date_format":"0",
    "range_from":"1692921600",
    "range_to":"1693008000",
    "cont_flag":"1"
}
FyersInstance = fyersModel.FyersModel(
            client_id='3H021OQ8ZI-100', token=accessToken, log_path=""
        )
response = FyersInstance.history(data=data)
print(response)
response['candles']
print(getPreviousSwingResistance(response['candles']))