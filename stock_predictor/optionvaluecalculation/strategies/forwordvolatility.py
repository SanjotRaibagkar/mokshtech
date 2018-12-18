#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 20:55:22 2018

@author: sanjotraibagkar
"""
import nsepy
from nsepy import get_history
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from datetime import date, datetime
import mibian
symbol="BANKNIFTY"

statergyStructCol = ['Date','StatergyName','Symbol','StrikePrice','ExpieryDate','PutorCall', 'Prices', 'NoofLot']

#banknifty_fut = get_history(symbol="BANKNIFTY", 
#                    start=date(2018,11,24), 
#                    end=date(2018,12,13),
#					index=True,
#                    futures=True,
#                    expiry_date=date(2018,11,29))
#
#print(banknifty)
#
#startDate = date(2018,11,23)
#
#banknifty_opt = get_history(symbol="BANKNIFTY",
#			start=startDate, 
#			end=date(2018,11,29),
#			option_type="CE",
#			strike_price=26500,
#			expiry_date=date(2018,11,29),
#            index=True)
#
#banknifty_opt1 = get_history(symbol="BANKNIFTY",
#			start=startDate, 
#			end=date(2018,12,6),
#			option_type="CE",
#			strike_price=26500,
#			expiry_date=date(2018,12,6),
#            index=True)
#banknifty_opt2 = get_history(symbol="BANKNIFTY",
#			start=startDate, 
#			end=date(2018,12,13),
#			option_type="CE",
#			strike_price=26500,
#			expiry_date=date(2018,12,13),
#            index=True)
#
#c = mibian.Me([27008.75,27000,0,0,2],callPrice = 118)
#
#threedayVari = calculatendayVarience(c.impliedVolatility,2)
#
#c1 = mibian.Me([27008.75,27000,0,0,9],callPrice = 231.5)
#
#tendayvari = calculatendayVarience(c1.impliedVolatility,9)
#
#c2 = mibian.Me([27116.75,27000,0,0,16],callPrice = 330)
#seveenteendayVari = calculatendayVarience(c2.impliedVolatility,16)
#
#sevenDayvolbetween3and10 = np.sqrt(((tendayvari-threedayVari)/7)*365)
#sevenDayvariencbetween10and17 =np.sqrt(((seveenteendayVari-tendayvari)/7)*365)
#
#
#
#
#
#
#opt_closeVale = pd.concat([banknifty_opt2['Underlying'],banknifty_opt['Close'],banknifty_opt1['Close'],
#                             banknifty_opt2['Close']],axis=1)
#
#opt_closeVale = opt_closeVale.fillna(0)
#

def calculatendayVarience(impvol,n):
    return n*(impvol**2)/365

def defineForwordVolatilityStatergy(underlyinglist,strikeprice,nofdayslist,callorputlist,callorputflag,symbol,expieryDaysList) :
 
    m = range(0,3)
    noofdaysVarienceDir = dict()
    name =''
    for i in m:
        underlying = underlyinglist[i]
        noofdays = nofdayslist[i]
        callorputprice = callorputlist[i]
        flag =callorputflag
        if flag=='P':
            name = 'Put'
            price = mibian.Me([underlying,strikeprice,0,0,noofdays],putPrice = callorputprice)
        else:
            name = 'Call'  
            #print("values are ",underlying,strikeprice,noofdays,callorputprice)
            price = mibian.Me([underlying,strikeprice,0,0,noofdays],callPrice = callorputprice)
       # price = mibian.Me([underlying,strikeprice,0,0,noofdays],name = callorputprice)
        varience = calculatendayVarience(price.impliedVolatility,noofdays)
        noofdaysVarienceDir.update( {i :(noofdays,varience)})  
    
    firstVarince = noofdaysVarienceDir[0]
    secondVarince = noofdaysVarienceDir[1]
    thridVarience = noofdaysVarienceDir[2]
    
    firstandsecondVol = calculateForwordVolatility(firstVarince,secondVarince)
    secondandthridVol = calculateForwordVolatility(secondVarince,thridVarience)
    
    statergy , statergyDF = makeFvStatergy(firstandsecondVol,secondandthridVol,strikeprice,symbol,name,expieryDaysList,callorputlist)
    
    return statergy,statergyDF,noofdaysVarienceDir,firstandsecondVol,secondandthridVol


def calculateForwordVolatility(firstVarince,secondVarince) :
  
    
    varienceVal = (secondVarince[1]-firstVarince[1])/(secondVarince[0]-firstVarince[0])*365
    #print("calculateForwordVolatility", varienceVal)
    
    
    volatility = np.sqrt(varienceVal)
    #print("calculateForwordVolatility volatility",volatility)
    return volatility

def makeFvStatergy(firstandsecondVol,secondandthridVol,strikeprice,symbol,name,expieryDaysList,callorputlist):
     #statergyDF = pd.DataFrame(columns= statergyStructCol)
     statergy =''
     if firstandsecondVol > secondandthridVol:
         statergy = 'Buy one {} {} , Sell 2 {} {} , Buy one {} {} for strike price {} of {}'.format(expieryDaysList[0],name,expieryDaysList[1],name,
                                                                                        expieryDaysList[2],name,strikeprice,symbol)
         statergylist = [
                         (datetime.now,'Statergy1',symbol,strikeprice,expieryDaysList[0],name,-callorputlist[0],1),
                         (datetime.now,'Statergy1',symbol,strikeprice,expieryDaysList[1],name, callorputlist[1],2),
                         (datetime.now,'Statergy1',symbol,strikeprice,expieryDaysList[2],name,-callorputlist[2],1)
                        ]
      
         statergyDF = pd.DataFrame(statergylist,columns= statergyStructCol)
     else :
         statergy = 'Sell one {} {} , Buy 2 {} {} , Sell one {} {} for strike price {} of {}'.format(expieryDaysList[0],name,expieryDaysList[1],name,
                                                                                        expieryDaysList[2],name,strikeprice,symbol)
         statergylist = [
                         (datetime.now,'Statergy1',symbol,strikeprice,expieryDaysList[0],name,callorputlist[0],1),
                         (datetime.now,'Statergy1',symbol,strikeprice,expieryDaysList[1],name,-callorputlist[1],2),
                         (datetime.now,'Statergy1',symbol,strikeprice,expieryDaysList[2],name,callorputlist[2],1)
                        ]
         statergyDF = pd.DataFrame(statergylist,columns= statergyStructCol)

     return statergy,statergyDF
     

if __name__ == '__main__':
    underlyinglist =[27008.75,27008.75,27116.75]  
    strikePrice = 27000
    nofdaysList =[2,9,16]
    callorputlist =[118,231.5,330]
    callorputflag ='C'
    expieryDaysList = ['20-dec-2018','27-dec-2018','3-Jan-2018']
    statergy,statergyDF,noofdaysVarienceDir,firstandsecondVol,secondandthridVol = defineForwordVolatilityStatergy(underlyinglist,strikePrice,
                                                                    nofdaysList,callorputlist,callorputflag,symbol,expieryDaysList)
    
    print('Statergy is ', statergy)
    print('Statergy DF is ', statergyDF)
    print('First vol is ', firstandsecondVol, 'and second os',secondandthridVol)
    
    

      
    
    

    
    
    