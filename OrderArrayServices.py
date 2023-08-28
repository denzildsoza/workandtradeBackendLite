# Sorts Orders based on the distance of the level from its undrrlying price
def sortArrayByProximityToBase(data):
    return sorted(data, key=lambda x: (abs(x["level"] - x["base"])) / x["base"])


def DeleteOrder(Orders, id):
    return [order for order in Orders if order["id"] != id]


def GetOrders(Orders):
    touchdown = Orders[0]
    breakout = []
    for i in Orders[1]:
        breakout.append(i[1])
    return touchdown+breakout












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
