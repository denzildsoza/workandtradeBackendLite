from flask import Flask, jsonify, request
from threading import Thread
from fyers_api import fyersModel
from fyers_api.Websocket import ws
from fyers_api import accessToken
from os import getcwd

#create instance of flask
app = Flask(__name__)

#Initializations


#Define the api end points
# Create fyers object
@app.route('/createsession')
def createFyersObject():
    pass



# API endpoint to get all orders
@app.route('/orders', methods=['GET'])
def getOrders():
    pass


# API endpoint to add a new order
@app.route('/placeorder', methods=['POST'])
def PlaceOrders():
    pass

# API endpoint to delete a order
@app.route('/orders/<orderId>', methods=['DELETE'])
def deleteOrders(orderId):
    pass
        

if __name__ == '__main__':
    app.run()


