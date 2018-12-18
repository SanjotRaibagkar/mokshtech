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
import mibian


banknifty_fut = get_history(symbol="BANKNIFTY", 
                    start=date(2018,11,24), 
                    end=date(2018,12,13),
					index=True,
                    futures=True,
                    expiry_date=date(2018,11,29))

print(banknifty)

startDate = date(2018,11,23)

banknifty_opt = get_history(symbol="BANKNIFTY",
			start=startDate, 
			end=date(2018,11,29),
			option_type="CE",
			strike_price=26500,
			expiry_date=date(2018,11,29),
            index=True)

banknifty_opt1 = get_history(symbol="BANKNIFTY",
			start=startDate, 
			end=date(2018,12,6),
			option_type="CE",
			strike_price=26500,
			expiry_date=date(2018,12,6),
            index=True)
banknifty_opt2 = get_history(symbol="BANKNIFTY",
			start=startDate, 
			end=date(2018,12,13),
			option_type="CE",
			strike_price=26500,
			expiry_date=date(2018,12,13),
            index=True)

c = mibian.Me([26363.75,26500,0,0,3/365],callPrice = 92.15)

threedayVari = calculatendayVarience(c.impliedVolatility,3)

c1 = mibian.Me([26363.75,26500,0,0,10/365],callPrice = 200.5)

tendayvari = calculatendayVarience(c1.impliedVolatility,10)

c2 = mibian.Me([26363.75,26500,0,0,17/365],callPrice = 828)
seveenteendayVari = calculatendayVarience(c2.impliedVolatility,17)

sevenDayvolbetween3and10 = np.sqrt(((tendayVol-threedayVol)/7)*365)
sevenDayvariencbetween10and17 =np.sqrt(((seveenteendayVol-tendayVol)/7)*365)


def calculatendayVarience(impvol,n):
    return n*(impvol**2)/365



opt_closeVale = pd.concat([banknifty_opt2['Underlying'],banknifty_opt['Close'],banknifty_opt1['Close'],
                             banknifty_opt2['Close']],axis=1)

opt_closeVale = opt_closeVale.fillna(0)




    
    
    