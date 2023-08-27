from flask import Flask, jsonify, request
from threading import Thread
from FyersInstance import generateFyersInstance
from Utils import logger, createOrderArray
from getItm import FilteredSymbolList
from OrderArrayServices import DeleteOrder
from constants import workandtradeconfig

# create instance of flask
app = Flask(__name__)

# Initializations
Orders = []
FyersInstance = FyersWebsocketInstance = None
filteredList = FilteredSymbolList()

# Define the api end points
# Create fyers object
@app.route(workandtradeconfig.newSession)
def createFyersObject():
    global FyersInstance, FyersWebsocketInstance
    try:
        FyersInstance, FyersWebsocketInstance = generateFyersInstance(
            request.args.get("auth_code")
        )
        return jsonify({"message": "Success created a session"}), 200
    except Exception as error:
        logger.log(error, "We have a %s", "mysterious problem", exc_info=1)
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
    try:
        orderBody = createOrderArray(orderBody, filteredList,FyersInstance)
        Orders.append(orderBody)
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
    Thread(target=lambda: FyersWebsocketInstance.connect()).start()
    Thread(target=lambda: app.run()).start()

