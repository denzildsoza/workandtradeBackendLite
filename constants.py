from os import getcwd

path = getcwd()


#Config
#workandtrade config
class workandtradeconfig:
    baseUrl="http://127.0.0.1:5000"
    newSession="/newSession"
    getOrders="/orders"
    placeOrder="/placeorder"
    deleteOrder="/orders/<orderId>"
    getTypes="/getordertypes"
    getSymbols="/getsymbols"
  

#Credentials
class CredentialsConstants:
    clientId = '3H021OQ8ZI-100'
    redirectUrl = f"{workandtradeconfig.baseUrl}${workandtradeconfig.newSession}"
    secretKey = "PPEJLUL3HA"
    SymbolUpdate = "SymbolUpdate"
    code = "code"
    state = "KJSDIUSEKJSRKJBIUGDJSBISESHIHSDGIS"
    grantType = "authorization_code"

#LogPaths
class LogpathConstants:
    fyerslogpath = f"{path}/Logs/Fyers"
    errorlogspath = f"{path}/Logs/Errors/errors.log"


#api Constants
class ApiConstants:
    IndexSymbolsList = ['NSE:NIFTY50-INDEX','NSE:NIFTYBANK-INDEX']
    orderTypes = ["BreakOut", "TouchDown"]








# Orders = {
#     "id": "",
#     "quantity": "",
#     "level": [0.0000518*100+1],
#     "underLyingSymbol": "",
#     "Target":1,
#     "stopLoss":1
# }

# data = {"id": ""}



# orderDetails = {
#     "id": "",
#     "level": "",
#     "direction": "",
#     "target": "",
#     "stoploss": "",
#     "type": "",
# }

'''msg[0]['ltp']'''

("https://public.fyers.in/sym_details/NSE_FO.csv")