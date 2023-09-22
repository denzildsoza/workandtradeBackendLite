from flask import Flask, jsonify, request
from threading import Thread
from fyers_apiv3 import fyersModel
from Utils import logger, createOrderArray
from getItm import FilteredSymbolList
from OrderArrayServices import DeleteOrder, CreateOrderData
from fyers_apiv3.FyersWebsocket import data_ws
from constants import (
    CredentialsConstants,
    LogpathConstants,
    workandtradeconfig,
    ApiConstants,
)
import copy

# create instance of flask
app = Flask(__name__)

# Initializations
accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTUzNTYwOTUsImV4cCI6MTY5NTQyOTA1NSwibmJmIjoxNjk1MzU2MDk1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbERSU19PVGcyTE56RXZRZFgxMVlmeEZjSGwyRUtoRzlSQjNfQ0VfM2hjXzBqV2UxM2p5aXU0WFc0ZW0tQkxZc0FMdjcxOEZiTWIzWVRzYmI5T3oySzRfS3FuanFpQ2tJcjViUUhBcHc4OXZ4TUlKaz0iLCJkaXNwbGF5X25hbWUiOiJERU5aSUwgRFNPVVpBIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjVkOTdlYTE1YmY5MWRhMzUxOTJmODUzZTNiNWQ2YTEwMGQyYzc2OTEwMTk3MjIyZWVlZjY5ZjIiLCJmeV9pZCI6IlhEMDg2ODUiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.v68mc1Ib2FFzqZNbWyO0Ot7OeiBOD793vpk9iVBH7iQ"
Orders = []
filteredList = FilteredSymbolList()
print(filteredList)

FyersInstance = fyersModel.FyersModel(
    client_id=CredentialsConstants.clientId,
    token=accessToken,
    log_path=LogpathConstants.fyerslogpath,
)


def placeOrder(order):
    global Orders
    data = CreateOrderData(quantity=order["quantity"], symbol=order["tradeSymbol"])
    response = FyersInstance.place_order(data=data)
    print(response)
    id = response["id"]
    tartget = order["target"]
    stoploss = order["stoploss"]
    underlyingSymbol = order["underlyingSymbol"]
    Orders.append({"id": id, "limits": [stoploss, tartget],"underlyingSymbol":underlyingSymbol, "type": "exit"})


def exitpositionByid(order):
    data = {"id": order["id"]}
    FyersInstance.exit_positions(data=data)
    logger.log(f"possitions exited ${order}")

def onmessage(data):
    print(data)
    global Orders
    touchdown = []
    breakout = []
    for order in Orders:
        if order["underlyingSymbol"] == data["symbol"]:
            touchdown.append(order)
        if order["tradeSymbol"] == data["symbol"]:
            breakout.append(order)
    for order in touchdown:
        if data["ltp"] >= order["limits"][1] and data["ltp"] <= order["limits"][0]:

            if order["type"] == "Breakout":
                order["isCrossed"] = True
                continue
            if order["type"] == "TouchDown":
                try:
                    Orders = DeleteOrder(Orders, order["id"])
                except Exception as e:
                    logger.info(e)
                else:
                    Thread(target=placeOrder, args=(order,)).start()
                continue
            else:
                try:
                    Orders = DeleteOrder(Orders, order["id"])
                finally:
                    Thread(target=exitpositionByid, args=(order,)).start()
        else:
            if order["type"] == "Breakout":
                order["isCrossed"] = False

    for order in breakout:
        if order["isCrossed"] == True and data["ltp"] >= order["contractLevel"]:
            try:
                Orders = DeleteOrder(Orders, order["id"])
            except Exception as e:
                logger.info(e)
            else:
                Thread(target=placeOrder, args=(order,)).start()


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

    # Subscribe to the specified symbols and data type
    symbols = ApiConstants.IndexSymbolsList
    fyers.subscribe(symbols=symbols, data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()


wsAccessToken = f"{CredentialsConstants.clientId}:{accessToken}"
# Replace the sample access token with your actual access token obtained from Fyers

# Create a FyersDataSocket instance with the provided parameters
fyers = data_ws.FyersDataSocket(
    access_token=wsAccessToken,  # Access token in the format "appid:accesstoken"
    log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=True,  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=False,  # Save response in a log file instead of printing it.
    reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
    on_connect=onopen,  # Callback function to subscribe to data upon connection.
    on_close=onclose,  # Callback function to handle WebSocket connection close events.
    on_error=onerror,  # Callback function to handle WebSocket errors.
    on_message=onmessage,  # Callback function to handle incoming messages from the WebSocket.
)

# Establish a connection to the Fyers WebSocket
fyers.connect()


# Interceptor for authentication
@app.before_request
def before_request_func():
    authTocken = request.headers.get("Authorization")
    if authTocken != CredentialsConstants.auth:
        return jsonify({"message": "not found"}), 404


# Define the api end points
# Create fyers object
@app.route(workandtradeconfig.newSession)
def createFyersObject():
    try:
        global FyersInstance, fyerswstoken
#       
        return jsonify({"message": "Success created a session"}), 200
    except Exception as error:
        logger.log(error, "We have a %s", "mysterious problem", exc_info=1)
        print(error)
        return jsonify({"message": "Error occured while authenticating"}), 404


# API endpoint to get all orders
@app.route(workandtradeconfig.getOrders, methods=["GET"])
def getOrders():
    global Orders
    try:
        return jsonify(Orders), 200
    except:
        return jsonify({"message": "Error occured while fetching orders"}), 404


# API endpoint to add a new order
@app.route(workandtradeconfig.placeOrder, methods=["POST"])
def PlaceOrders():
    global Orders
    orderBody = request.json
    print(orderBody)
    orders = copy.deepcopy(Orders)
    try:
        Orders, tradeSymbol = createOrderArray(
            orders, orderBody, filteredList, FyersInstance
        )
        if tradeSymbol:
            fyers.subscribe(symbols=[tradeSymbol], data_type="SymbolUpdate")
        return jsonify({"message": "Successfully placed the Order"}), 200
    except Exception as error:
        print(error)
        return jsonify({"message": error}), 404


# API endpoint to delete a order
@app.route("/deleteorder/<orderId>", methods=["GET"])
def deleteOrders(orderId):
    global Orders
    try:
        Orders = DeleteOrder(Orders, orderId)
        return (
            jsonify({"message": f"successfully deleted order with id ${orderId}"}),
            200,
        )
    except:
        return jsonify({"message": "Error occured while deleting the order"}), 404


if __name__ == "__main__":
    Thread(target=lambda: app.run()).start()
