from getItm import get_ITM

def CreateOrderData(filteredSymbolList,orderDataDict):
    level = int(orderDataDict['level'])
    type = orderDataDict['type']
    direction = orderDataDict['direction']
    quantity = int(orderDataDict['quantity']) 
    target = int(orderDataDict['target'])
    
    if  direction == 'Support' and level <= 25000:
        ITM = get_ITM(filteredSymbolList,level,'NIFTY','CE',False)
        UNdl_ToKen = 'NSE:NIFTY50-INDEX'
        h_LeVel = level+1
        l_LeVel = level-5
        quantity = int(quantity)*50
    elif  direction == 'Support' and level >= 25000:
        ITM = get_ITM(filteredSymbolList,level,'BANKNIFTY','CE',False)
        UNdl_ToKen = 'NSE:NIFTYBANK-INDEX'
        h_LeVel =  level+2
        l_LeVel =  level-10
        quantity = int(quantity)*25
    elif  direction == 'Resistance' and level <= 25000:
        ITM = get_ITM(filteredSymbolList,level,'NIFTY','PE',True)
        UNdl_ToKen = 'NSE:NIFTY50-INDEX'
        h_LeVel =  level+5
        l_LeVel =  level-1
        quantity = int(quantity)*50
    elif  direction == 'Resistance' and level >= 25000:
        ITM = get_ITM(filteredSymbolList,level,'BANKNIFTY','PE',True)
        UNdl_ToKen = 'NSE:NIFTYBANK-INDEX'
        h_LeVel =  level+10
        l_LeVel =  level-2
        quantity = int(quantity)*25

    return { 
            'level':level,  
            'symbol' : ITM , 
            'h_LeVel' : h_LeVel , 
            'l_LeVel' : l_LeVel ,
            'UNdl_ToKen':UNdl_ToKen,
            'qty':quantity,
            'target':target,
            "typ":type,
            "dir":direction
            } 

# {
#                             "symbol":symbol,
#                             "qty":quantity,
#                             "type":2, 
#                             "side":1,
#                             "productType":"MARGIN",
#                             "limitPrice":0,
#                             "stopPrice":0,
#                             "validity":"DAY",
#                             "disclosedQty":0,
#                             "offlineOrder":"False",
#                             "stopLoss":0,
#                             "takeProfit":0
#                         }