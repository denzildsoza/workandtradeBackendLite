import logging
from constants import LogpathConstants
from getItm import getInTheMoneyContract
from datetime import datetime, timedelta

# Logger
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,filename=LogpathConstants.errorlogspath,)
logger = logging.getLogger("request_logger")


# Returns the order object
def createOrderArray(orders, orderBody, filteredList, FyersInstance):
    id = orderBody["id"]
    level = float(orderBody["level"])
    underlyingSymbol = orderBody["underlying"]
    target = float(orderBody["target"]) + level
    stoploss = float(orderBody["stoploss"]) + level
    direction = orderBody["direction"]
    limit = round(0.0000518 * level, 2)
    bool = True if direction == "Resistance" else False
    type = orderBody["type"]
    tradeSymbol = getInTheMoneyContract(
        filteredList,
        level,
        "NIFTY" if underlyingSymbol == "NSE:NIFTY50-INDEX" else "BANKNIFTY",
        "PE" if direction == "Resistance" else "CE",
        bool,
    )

    orderArrayElement = {
        "id": id,
        "limits": [limit + level, abs(level - limit)],
        "underlyingSymbol": underlyingSymbol,
        "tradeSymbol": tradeSymbol,
        "target": target,
        "stoploss": stoploss,
        "type": type,
    }

    if type == "TouchDown":
        orders.append(orderArrayElement)
        return orders, None
    orderArrayElement["isCrossed"] = False

    placeorderLevel = getPreviousSwing(tradeSymbol, FyersInstance)
    orderArrayElement["contractLevel"] = placeorderLevel
    orders.append(orderArrayElement)
    return orders, tradeSymbol


# Returns the data for the place order api
def CreateOrderData(symbol, quantity):
    return {
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


def createHistoricalData(symbol, FyersInstance):
    today = datetime.today()
    fromDate = today.strftime("%Y-%m-%d")
    yesterday = datetime.today() + timedelta(days=1)
    toDate = yesterday.strftime("%Y-%m-%d")
    data = {
        "symbol": symbol,
        "resolution": "3",
        "date_format": "1",
        "range_from": fromDate,
        "range_to": toDate,
        "cont_flag": "1",
    }
    response = FyersInstance.history(data=data)
    return response["candles"]


def getPreviousSwing(symbol, FyersInstance):
    data = createHistoricalData(symbol, FyersInstance)
    data = [sub_array[4] for sub_array in data]
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            last_swing = data[i]
        elif data[i] < data[i - 1] and data[i] < data[i + 1]:
            last_swing = data[i]

    return last_swing


def getPreviousLowerSwing(symbol, FyersInstance):
    data = createHistoricalData(symbol, FyersInstance)
    data = [sub_array[4] for sub_array in data]
    previousSwing = None
    n = len(data)
    for i in range(1, n - 1):
        if data[i] < data[i - 1] and data[i] < data[i + 1]:
            previousSwing = data[i]
    return previousSwing


def onOpen():
    pass


def onerror(message):
    logger.log(message, "We have a %s", "mysterious problem", exc_info=1)


def onclose(message):
    pass


from datetime import datetime
import pytz

# Replace 'YOUR_TIMEZONE' with your actual time zone
your_timezone = pytz.timezone("Asia/Kolkata")

# Get today's date


# def createHistoricalData(symbol, FyersInstance):
#     today = datetime.now(your_timezone).date()

#     # Set the target times
#     time_9am = today.replace(hour=9, minute=0, second=0, microsecond=0)
#     time_3_30pm = today.replace(hour=15, minute=30, second=0, microsecond=0)

#     # Calculate epoch timestamps
#     _from = int(time_9am.timestamp())
#     to = int(time_3_30pm.timestamp())
#     data = {
#         "symbol": symbol,
#         "resolution": "15",
#         "date_format": "0",
#         "range_from": _from,
#         "range_to": to,
#         "cont_flag": "1",
#     }
#     response = FyersInstance.history(data=data)
#     return response["candles"]
