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
    auth = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2OTMxNjIzOTgsImV4cCI6MTY5MzE5MjM5OCwibmJmIjoxNjkzMTYxNzk4LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYRDA4Njg1Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjVkOTdlYTE1YmY5MWRhMzUxOTJmODUzZTNiNWQ2YTEwMGQyYzc2OTEwMTk3MjIyZWVlZjY5ZjIiLCJub25jZSI6IiIsImFwcF9pZCI6IjNIMDIxT1E4WkkiLCJ1dWlkIjoiMGI3YWFjYTAyNzViNGVjNDk2NzlkMThjZTk4ZTRiYWIiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.8KHWBlvvC8JcNvsKPWjKFqhtwELmvqSLMddSM48cxkw"

#LogPaths
class LogpathConstants:
    fyerslogpath = f"{path}/Logs/Fyers"
    errorlogspath = f"{path}/Logs/Errors/errors.log"


#api Constants
class ApiConstants:
    IndexSymbolsList = ['NSE:NIFTY50-INDEX','NSE:NIFTYBANK-INDEX']
    orderTypes = ["TouchDown","BreakOut"]



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