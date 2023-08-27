import logging
from constants import LogpathConstants
from getItm import getInTheMoneyContract

# Logger
logging.basicConfig(
    filename=LogpathConstants.errorlogspath,
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


# Returns the order object
def createOrderArray(orderBody, filteredList, FyersInstance):
    id = orderBody["id"]
    level = float(orderBody["level"])
    underlyingSymbol = orderBody["underlying"]
    target = float(orderBody["target"])
    stoploss = float(orderBody["stoploss"])
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
    }

    if type == "TouchDown":
        return orderArrayElement

    breakoutArrayElement = [orderArrayElement]

    placeorderLevel = (
        getPreviousSwingResistance(tradeSymbol, FyersInstance)
        if bool
        else getPreviousSwingSupport(tradeSymbol, FyersInstance)
    )

    orderplaceElement = {
        "id": id,
        "limits": placeorderLevel,
        "underlyingSymbol": underlyingSymbol,
        "tradeSymbol": tradeSymbol,
        "target": target,
        "stoploss": stoploss,
    }
    return breakoutArrayElement.append(orderplaceElement)


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
    today = datetime.now(your_timezone).date()

    # Set the target times
    time_9am = today.replace(hour=9, minute=0, second=0, microsecond=0)
    time_3_30pm = today.replace(hour=15, minute=30, second=0, microsecond=0)

    # Calculate epoch timestamps
    _from = int(time_9am.timestamp())
    to = int(time_3_30pm.timestamp())
    data = {
        "symbol": symbol,
        "resolution": "15",
        "date_format": "0",
        "range_from": _from,
        "range_to": to,
        "cont_flag": "1",
    }
    response = FyersInstance.history(data=data)
    return response["candles"]


def getPreviousSwingSupport(symbol, FyersInstance):
    data = createHistoricalData(symbol, FyersInstance)
    previousSwing = None
    for i in range(1, len(data) - 1):
        if data[i][1] > data[i - 1][1] and data[i][1] > data[i + 1][1]:
            previousSwing = (i, data[i][1], "peak")
    return previousSwing


def getPreviousSwingResistance(symbol, FyersInstance):
    data = createHistoricalData(symbol, FyersInstance)
    previousSwing = None
    for i in range(1, len(data) - 1):
        if data[i][1] < data[i - 1][1] and data[i][1] < data[i + 1][1]:
            previousSwing = (i, data[i][1], "trough")
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


def createHistoricalData(symbol, FyersInstance):
    today = datetime.now(your_timezone).date()

    # Set the target times
    time_9am = today.replace(hour=9, minute=0, second=0, microsecond=0)
    time_3_30pm = today.replace(hour=15, minute=30, second=0, microsecond=0)

    # Calculate epoch timestamps
    _from = int(time_9am.timestamp())
    to = int(time_3_30pm.timestamp())
    data = {
        "symbol": symbol,
        "resolution": "15",
        "date_format": "0",
        "range_from": _from,
        "range_to": to,
        "cont_flag": "1",
    }
    response = FyersInstance.history(data=data)
    return response["candles"]
