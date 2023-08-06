def placeOrder(fyers, symbol, quantity):
    data = {
        "symbol": symbol,
        "qty": quantity,
        "type": 2,
        "side": 1,
        "productType": "MARGIN",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0,
    }

    response = fyers.place_order(data)
    return response["id"]


def exitPositionByID(fyers, id):
    data = {"id": id}
    response = fyers.exit_positions(data=data)
    return response["id"]


def exitAllOpenPositions(fyers):
    response = fyers.exit_positions(data={})
    return response["id"]
