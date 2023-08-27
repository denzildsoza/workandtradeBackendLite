from getNearestExpiry import getNextWeaklyEpiry
from pandas import read_csv
from datetime import datetime

allFnoSymbols = read_csv("https://public.fyers.in/sym_details/NSE_FO.csv")
allFnoSymbols.columns =  ['epoch_time','symbol_name','o','h','c','l','exg_time','date','expiry_date','symbol','10','11','underlying_price','underlying_name','underlying','strike_price','call_put','abc','None']
nearestWeaklyExpiry = '2023-08-31'
nearestWeaklyExpiryEpoch =  int((datetime.strptime(f'{nearestWeaklyExpiry} 20:00:00', '%Y-%m-%d %H:%M:%S')).timestamp())
allWeaklyExpiringContracts = allFnoSymbols.loc[allFnoSymbols['expiry_date'] == nearestWeaklyExpiryEpoch]

print(nearestWeaklyExpiry)

def get_ITM(sym_details,level,UnDL,CP,bool):   
    optionsData = sym_details
    optionsData = optionsData.loc[optionsData['underlying_name'] == UnDL]
    optionsData = optionsData.loc[optionsData['call_put'] == CP]
    optionsData = optionsData.sort_values('strike_price', ascending= bool)
    if CP == 'CE':
        optionsData = optionsData.loc[optionsData['strike_price'] < int(level)]
    else:
        optionsData = optionsData.loc[optionsData['strike_price'] > int(level)]   
    return optionsData["symbol"].tolist()[0]

ITM = get_ITM(allWeaklyExpiringContracts,19632,'NIFTY','CE',False)
'NSE:NIFTY2381019600CE'
print(ITM)