# Sorts Orders based on the distance of the level from its undrrlying price
def sortArrayByProximityToBase(data):
    return sorted(data, key=lambda x: (abs(x["level"] - x["base"])) / x["base"])


def DeleteOrder(Orders, id):
    return [order for order in Orders if order["id"] != id]


def GetOrders(Orders):
    touchdown = Orders[0]
    breakout = Orders[1]
    return touchdown + breakout


# Returns the data for the place order api
def CreateOrderData(symbol, quantity):
    return {
        "symbol": symbol,
        "qty": quantity,
        "type": 2,
        "side": -1,
        "productType": "MARGIN",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
    }

    # for Order in Orders:
    #     Order.pop(
    #         {
    #             "id": Order["id"],
    #             "level": Order["level"],
    #             "direction": Order["direction"],
    #             "quantity": Order["quantity"],
    #             "target": Order["target"],
    #             "stoploss": Order["stoploss"],
    #             "type": Order["type"],
    #             "underlying": Order["underlying"],
    #         }
    #     )
    #     Order = []
    # return Order
