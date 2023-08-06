import pandas as pd
from datetime import timedelta,date,datetime
from calendar import day_name

def FilteredSymbolList():
    try:
        sym_details = pd.read_csv("https://public.fyers.in/sym_details/NSE_FO.csv")
        sym_details.columns =  ['epoch_time','symbol_name','o','h','c','l','exg_time','date','expiry_date','symbol','10','11','underlying_price','underlying_name','underlying','strike_price','call_put','abc','None']
        def filterWeeklyexpiry():
            for i in range(8):
                    my_date = date.today()+timedelta(i)
                    a = day_name[my_date.weekday()]
                    if a == 'Thursday':
                        expiry_date = my_date
                        break
            for i in range(10):
                expiry_date = expiry_date - timedelta(i)
                expiry_date_epoch =  int((datetime.strptime(f'{expiry_date} 20:00:00', '%Y-%m-%d %H:%M:%S')).timestamp())
                sym_details_temp = sym_details.loc[sym_details['expiry_date'] == expiry_date_epoch]
                if  len(sym_details_temp) != 0 :
                    return sym_details_temp
        return filterWeeklyexpiry()
    except:
         return None
    
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