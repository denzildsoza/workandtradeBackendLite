import pandas as pd
from datetime import timedelta, date, datetime
from calendar import day_name
import pytz

def FilteredSymbolList():
    while True:
        try:
            allSymbols = pd.read_csv("https://public.fyers.in/sym_details/NSE_FO.csv")
        except:
            continue
        else:
            break
    try:
        
        allSymbols.columns = [
            "epoch_time",
            "symbol_name",
            "o",
            "h",
            "c",
            "l",
            "exg_time",
            "date",
            "expiry_date",
            "symbol",
            "10",
            "11",
            "underlying_price",
            "underlying_name",
            "underlying",
            "strike_price",
            "call_put",
            "abc",
            "None",
        ]
        allSymbols = allSymbols[
            ["expiry_date", "underlying_name", "call_put","symbol", "strike_price"]
        ]
        # allSymbols.to_excel("output.xlsx")
        def filterWeeklyexpiry():
            for i in range(8):
                my_date = date.today() + timedelta(i)
                a = day_name[my_date.weekday()]
                if a == "Thursday":
                    expiry_date = my_date
                    break
            for i in range(10):
                expiry_date = expiry_date - timedelta(i)
                expiry_datetime = datetime.strptime(f"{expiry_date} 20:00:00", "%Y-%m-%d %H:%M:%S")
                expiry_datetime_in_india = pytz.timezone('Asia/Kolkata').localize(expiry_datetime)
                expiry_date_epoch = int(expiry_datetime_in_india.timestamp())
                allSymbols_temp = allSymbols.loc[
                    allSymbols["expiry_date"] == expiry_date_epoch
                ]
                if len(allSymbols_temp) != 0:
                    return allSymbols_temp
        def filterWeeklyexpiry1():
            for i in range(8):
                my_date = date.today() + timedelta(i)
                a = day_name[my_date.weekday()]
                if a == "Wednesday":
                    expiry_date = my_date
                    break
            for i in range(10):
                expiry_date = expiry_date - timedelta(i)
                expiry_datetime = datetime.strptime(f"{expiry_date} 20:00:00", "%Y-%m-%d %H:%M:%S")
                expiry_datetime_in_india = pytz.timezone('Asia/Kolkata').localize(expiry_datetime)
                expiry_date_epoch = int(expiry_datetime_in_india.timestamp())
                allSymbols_temp = allSymbols.loc[
                    allSymbols["expiry_date"] == expiry_date_epoch
                ]
                if len(allSymbols_temp) != 0:
                    return allSymbols_temp
        filteredData = filterWeeklyexpiry()
        filteredData1 = filterWeeklyexpiry1()

        frames = [filteredData, filteredData1]
  
        result = pd.concat(frames)
        return result
    except Exception as e:
        raise Exception("Could not create filtered symbol list",e)


def getInTheMoneyContract(filteredSymbolList, level, underLying, direction, bool):
    optionsData = filteredSymbolList
    print(optionsData)
    optionsData = optionsData.loc[optionsData["underlying_name"] == underLying]
    optionsData = optionsData.loc[optionsData["call_put"] == direction]
    optionsData = optionsData.sort_values("strike_price", ascending=bool)
    
    if direction == "CE":
        optionsData = optionsData.loc[optionsData["strike_price"] < int(level)]
    else:
        optionsData = optionsData.loc[optionsData["strike_price"] > int(level)]
    return optionsData["symbol"].tolist()[0]

if __name__ == "__main__":
    print(FilteredSymbolList())
