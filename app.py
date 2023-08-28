from flask import Flask, jsonify, request
from threading import Thread
from FyersInstance import generateFyersInstance
from Utils import logger, createOrderArray
from getItm import FilteredSymbolList
from OrderArrayServices import DeleteOrder,GetOrders
from constants import workandtradeconfig,CredentialsConstants

# create instance of flask
app = Flask(__name__)

# Initializations
Orders = [[],[]]
FyersInstance , FyersWebsocketInstance = generateFyersInstance('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTMxOTY1NTMsImV4cCI6MTY5MzI2OTAzMywibmJmIjoxNjkzMTk2NTUzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazdDRUpsa1hpSEZtVERMVVRlMktDWkpWeXFMQWJfbUZmOWR4bHVoZ09DYXlDcUVXU1ZUNkNVLVlxV1ROTDFEMkR2N2dXNkREbWZOaTZTQzlQTXRCaE5JQy1TSnJnMGFJR2ZKYUpZY1V2a0FTVG0xRT0iLCJkaXNwbGF5X25hbWUiOiJERU5aSUwgRFNPVVpBIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjVkOTdlYTE1YmY5MWRhMzUxOTJmODUzZTNiNWQ2YTEwMGQyYzc2OTEwMTk3MjIyZWVlZjY5ZjIiLCJmeV9pZCI6IlhEMDg2ODUiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.ufBFeHJRtgtrtz4O2JGehf2xnN_5u5N0IDvs9WEdH3A')
filteredList = FilteredSymbolList()

#handle on message callback
def onmessage(data):
    global Orders
    arrayFiltered = [order for order in Orders[0] if order["underlyingSymbol"] == data["symbol"]]
    for order in arrayFiltered:
        if data["ltp"] >= order["limits"][1] and data["ltp"] <= order["limits"][0]:
            Orders.remove(order)
            logger.info("Order  placed successfully.")
            print("orderPlaced")

#Interceptor for authentication
# @app.before_request
def before_request_func():
    if request.path.startswith('/createsession') :
        stateRes = request.args.get('state')
        if stateRes == CredentialsConstants.state:
            return request 
        else:
            return jsonify({'message':'not authenticated'}),404
    authTocken = request.headers.get('Authorization')
    if authTocken != CredentialsConstants.auth :
        return jsonify({'message':'not authenticated'}),404


# Define the api end points
# Create fyers object
@app.route(workandtradeconfig.newSession)
def createFyersObject():
    global FyersInstance, FyersWebsocketInstance
    try:
        FyersInstance, FyersWebsocketInstance = generateFyersInstance(
            request.args.get("auth_code")
        )
        FyersWebsocketInstance.On_message=onmessage
        return jsonify({"message": "Success created a session"}), 200
    except Exception as error:
        logger.log(error, "We have a %s", "mysterious problem", exc_info=1)
        return jsonify({"message": "Error occured while authenticating"}), 404


# API endpoint to get all orders
@app.route(workandtradeconfig.getOrders, methods=["GET"])
def getOrders():
    global Orders
    try:
        Orders = GetOrders(Orders)
        return jsonify(Orders), 200
    except:
        return jsonify({"message": "Error occured while fetching orders"}), 404


# API endpoint to add a new order
@app.route(workandtradeconfig.placeOrder, methods=["POST"])
def PlaceOrders():
    global Orders
    orderBody = request.json
    try:
        orderBody,tradeSymbol = createOrderArray(Orders,orderBody, filteredList,FyersInstance)
        if(tradeSymbol):
            FyersWebsocketInstance.subscribe(symbols=[tradeSymbol], data_type='SymbolUpdate')
        Orders = Orders
        print(Orders)
        return jsonify({'message':'Successfully placed the Order'}),200
    except Exception as error:
        print(error)
        return jsonify({"message": "Error occured while Placing order"}), 404


# API endpoint to delete a order
@app.route(workandtradeconfig.deleteOrder, methods=["DELETE"])
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

