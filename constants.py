from os import getcwd

path = getcwd()


#Config
#workandtrade config
class workandtradeconfig:
    baseUrl="http://127.0.0.1:5000"
    newSession="/newSession"
    getOrders="/orders"
    placeOrder="/placeorder"
    deleteOrder="/deleteorder/<orderId>"
    getTypes="/getordertypes"
    getSymbols="/getsymbols"
  

#Credentials
class CredentialsConstants:
    clientId = '3H021OQ8ZI-100'
    redirectUrl = f"{workandtradeconfig.baseUrl}${workandtradeconfig.newSession}"
    secretKey = "..."
    SymbolUpdate = "SymbolUpdate"
    code = "code"
    state = "..."
    grantType = "authorization_code"
    auth = "..."

#LogPaths
class LogpathConstants:
    fyerslogpath = f"{path}/Logs/Fyers"
    errorlogspath = f"{path}/Logs/Errors/errors.log"


#api Constants
class ApiConstants:
    IndexSymbolsList = ['NSE:NIFTY50-INDEX','NSE:NIFTYBANK-INDEX']
    # IndexSymbolsList = ["MCX:GOLDM23SEPFUT"]
    orderTypes = ["TouchDown","BreakOut"]

