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
    quantity = int(orderBody["quantity"])
    underlyingSymbol = orderBody["underlying"]
    direction = orderBody["direction"]
    limit = round(0.0000518 * level, 2)
    type = orderBody["type"]
    if direction == "Resistance":
        target =level - float(orderBody["target"]) 
        stoploss =level+ float(orderBody["stoploss"])
        tradeSymbol = getInTheMoneyContract(
            filteredList,
            target,
            "NIFTY" if underlyingSymbol == "NSE:NIFTY50-INDEX" else "BANKNIFTY",
            "PE",
            True,
        )
        placeorderLevel = getSwingHigh(tradeSymbol,FyersInstance) if type == "Breakout" else None

    if direction == "Support":
        target = float(orderBody["target"]) + level
        stoploss =level- float(orderBody["stoploss"])
        tradeSymbol = getInTheMoneyContract(
            filteredList,
            target,
            "NIFTY" if underlyingSymbol == "NSE:NIFTY50-INDEX" else "BANKNIFTY",
            "CE",
            False,
        )
        placeorderLevel = getSwingHigh(tradeSymbol,FyersInstance) if type == "Breakout" else None
    orderArrayElement = {
        "id": id,
        "limits": [limit + level, abs(level - limit)],
        "quantity":quantity,
        "underlyingSymbol": underlyingSymbol,
        "tradeSymbol": tradeSymbol,
        "target": target,
        "stoploss": stoploss,
        "type": type,
    }

    if type == "TouchDown":
        orders.append(orderArrayElement)
        return orders, placeorderLevel
    orderArrayElement["isCrossed"] = False

    orderArrayElement["contractLevel"] = placeorderLevel
    orders.append(orderArrayElement)
    return orders, tradeSymbol




def createHistoricalData(symbol, FyersInstance):
    today = datetime.today()
    fromDate = today.strftime("%Y-%m-%d")
    yesterday = datetime.today() + timedelta(days=1)
    toDate = yesterday.strftime("%Y-%m-%d")
    data = {
        "symbol": symbol,
        "resolution": "15",
        "date_format": "1",
        "range_from": fromDate,
        "range_to": toDate,
        "cont_flag": "1",
    }
    response = FyersInstance.history(data=data)
    return response["candles"]


def getSwingHigh(symbol,FyersInstance):
    data = createHistoricalData(symbol,FyersInstance)
    open =  [sub_array[1] for sub_array in data]
    close = [sub_array[4] for sub_array in data]
    swingHigh = []
    for i in  range(0, len(open) - 1):
        if close[i] > open[i+1]:
            swingHigh.append(close[i])
        else:
            swingHigh.append(open[i+1])
    highSwing = None
    for i in range(1, len(swingHigh) - 1):
        if swingHigh[i] > swingHigh[i - 1] and swingHigh[i] > swingHigh[i + 1]:
            highSwing = swingHigh[i]
    return highSwing  


def getSwingLow(symbol,FyersInstance):
    data = createHistoricalData(symbol,FyersInstance)
    open =  [sub_array[1] for sub_array in data]
    close = [sub_array[4] for sub_array in data]
    swingLow = []
    for i in  range(0, len(open) - 1):
        if close[i] < open[i+1]:
            swingLow.append(close[i])
        else:
            swingLow.append(open[i+1])
    lowSwing = None
    for i in range(1, len(swingLow) - 1):
        if swingLow[i] < swingLow[i - 1] and swingLow[i] < swingLow[i + 1]:
            lowSwing = swingLow[i]
    return lowSwing

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
