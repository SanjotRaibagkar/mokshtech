# coding: utf-8
'''
This file contains all file paths, common libraries and stockpath


'''
import os

import import_ipynb
import pandas as pd
import math
import numpy as np
from numpy import nan
from datetime import date
import warnings
import socket
warnings.filterwarnings("ignore")

##File Path

basepath=os.path.dirname(os.path.abspath('.'))
if str(basepath).split("\\")[-1] == "mokshtech":
    basepath = os.path.join(basepath,"stock_predictor")

#
# if socket.gethostname()=='shashank':
#     basepath="C:\\Prgs\\Code\\mokshtech\\stock_predictor\\"                   #############This needs to be adjusted as per user.
# else:
#     basepath=""

dbpath=os.path.join(basepath,'database')
stockdata=os.path.join(dbpath,'stockdata')
#stockdata=os.path.join(dbpath,'stockdata_1')
featurescsv=os.path.join(dbpath,'features.csv')
featuresdata=os.path.join(dbpath,'featuresdata.csv')
repobasepath = os.path.join(basepath,'report')


indlist=['NIFTY']#,'BANKNIFTY','NIFTY']#'NIFTYIT','NIFTYMID50','NIFTYPSE','NIFTYINFRA']
nonindlist=['SYNDIBANK_F1']#,'TCS']#,'ARVIND','ASHOKLEY','ASIANPAINT','AUROPHARMA','AXISBANK','BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE','BALKRISIND','BALRAMCHIN','BANKBARODA','BANKINDIA','BATAINDIA','BEL','BEML','BERGEPAINT','BHARATFIN','BHARATFORG','BHARTIARTL','BHEL','BIOCON','BOSCHLTD','BPCL','BRITANNIA','CADILAHC','CANBK','CANFINHOME','CAPF','CASTROLIND','CEATLTD','CENTURYTEX','CESC','CGPOWER','CHENNPETRO','CHOLAFIN','CIPLA','COALINDIA','COLPAL','CONCOR','CUMMINSIND','DABUR','DALMIABHA','DCBBANK','DHFL','DISHTV','DIVISLAB','DLF','DRREDDY','EICHERMOT','ENGINERSIN','EQUITAS','ESCORTS','EXIDEIND','FEDERALBNK','GAIL','GLENMARK','GMRINFRA','GODFRYPHLP','GODREJCP','GODREJIND','GRANULES','GRASIM','GSFC','HAVELLS','HCC','HCLTECH','HDFC','HDFCBANK','HEROMOTOCO','HEXAWARE','HINDALCO','HINDPETRO','HINDUNILVR','HINDZINC','IBULHSGFIN','ICICIPRULI','IDBI','IDEA','IDFC','IDFCBANK','IFCI','IGL','INDIACEM','INDIANB','INDIGO','INDUSINDBK','INFIBEAM','INFRATEL','INFY','IOC','IRB','ITC','JETAIRWAYS','JINDALSTEL','JISLJALEQS','JPASSOCIAT','JSWSTEEL','JUBLFOOD','JUSTDIAL','KAJARIACER','KOTAKBANK','KPIT','KSCL','KTKBANK','L&TFH','LICHSGFIN','LT','LUPIN','M&M','M&MFIN','MANAPPURAM','MARICO','MARUTI','MCDOWELL-N','MCX','MFSL','MGL','MINDTREE','MOTHERSUMI','MRF','MRPL','MUTHOOTFIN','NATIONALUM','NBCC','NCC','NESTLEIND','NHPC','NIITTECH','NMDC','NTPC','OFSS','OIL','ONGC','ORIENTBANK','PAGEIND','PCJEWELLER','PEL','PETRONET','PFC','PIDILITIND','PNB','POWERGRID','PTC','PVR','RAMCOCEM','RAYMOND','RBLBANK','RCOM','RECLTD','RELCAPITAL','RELIANCE','RELINFRA','REPCOHOME','RNAVAL','RPOWER','SAIL','SBIN','SHREECEM','SIEMENS','SOUTHBANK','SREINFRA','SRF','SRTRANSFIN','STAR','SUNPHARMA','SUNTV','SUZLON','ICICIBANK','TATACHEM','TATACOMM','TATAELXSI','TATAGLOBAL','TATAMOTORS','TATAMTRDVR','TATAPOWER','TATASTEEL','TECHM','TITAN','TORNTPHARM','TORNTPOWER','TV18BRDCST','TVSMOTOR','UBL','UJJIVAN','ULTRACEMCO','UNIONBANK','UPL','VEDL','VGUARD','VOLTAS','WIPRO','WOCKPHARMA','YESBANK','ZEEL']

## not included
#'ACC','ADANIENT','ADANIPORTS','ADANIPOWER','AJANTPHARM','ALBK','AMARAJABAT','AMBUJACEM','ANDHRABANK','APOLLOHOSP','APOLLOTYRE'
#'FTSE100','INDIAVIX','NIFTYCPSE',  These are not coming

unformat_header=['Symbol','Date','Time','Open','High','Low','Close','Volume','Turnover']


stocklist=['FTSE100','INDIAVIX','NIFTYCPSE','NIFTY','NIFTYIT','BANKNIFTY','NIFTYMID50','NIFTYPSE','NIFTYINFRA','ACC','ADANIENT','ADANIPORTS','ADANIPOWER','AJANTPHARM','ALBK','AMARAJABAT','AMBUJACEM','ANDHRABANK','APOLLOHOSP','APOLLOTYRE','ARVIND','ASHOKLEY','ASIANPAINT','AUROPHARMA','AXISBANK','BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE','BALKRISIND','BALRAMCHIN','BANKBARODA','BANKINDIA','BATAINDIA','BEL','BEML','BERGEPAINT','BHARATFIN','BHARATFORG','BHARTIARTL','BHEL','BIOCON','BOSCHLTD','BPCL','BRITANNIA','CADILAHC','CANBK','CANFINHOME','CAPF','CASTROLIND','CEATLTD','CENTURYTEX','CESC','CGPOWER','CHENNPETRO','CHOLAFIN','CIPLA','COALINDIA','COLPAL','CONCOR','CUMMINSIND','DABUR','DALMIABHA','DCBBANK','DHFL','DISHTV','DIVISLAB','DLF','DRREDDY','EICHERMOT','ENGINERSIN','EQUITAS','ESCORTS','EXIDEIND','FEDERALBNK','GAIL','GLENMARK','GMRINFRA','GODFRYPHLP','GODREJCP','GODREJIND','GRANULES','GRASIM','GSFC','HAVELLS','HCC','HCLTECH','HDFC','HDFCBANK','HEROMOTOCO','HEXAWARE','HINDALCO','HINDPETRO','HINDUNILVR','HINDZINC','IBULHSGFIN','ICICIBANK','ICICIPRULI','IDBI','IDEA','IDFC','IDFCBANK','IFCI','IGL','INDIACEM','INDIANB','INDIGO','INDUSINDBK','INFIBEAM','INFRATEL','INFY','IOC','IRB','ITC','JETAIRWAYS','JINDALSTEL','JISLJALEQS','JPASSOCIAT','JSWSTEEL','JUBLFOOD','JUSTDIAL','KAJARIACER','KOTAKBANK','KPIT','KSCL','KTKBANK','L&TFH','LICHSGFIN','LT','LUPIN','M&M','M&MFIN','MANAPPURAM','MARICO','MARUTI','MCDOWELL-N','MCX','MFSL','MGL','MINDTREE','MOTHERSUMI','MRF','MRPL','MUTHOOTFIN','NATIONALUM','NBCC','NCC','NESTLEIND','NHPC','NIITTECH','NMDC','NTPC','OFSS','OIL','ONGC','ORIENTBANK','PAGEIND','PCJEWELLER','PEL','PETRONET','PFC','PIDILITIND','PNB','POWERGRID','PTC','PVR','RAMCOCEM','RAYMOND','RBLBANK','RCOM','RECLTD','RELCAPITAL','RELIANCE','RELINFRA','REPCOHOME','RNAVAL','RPOWER','SAIL','SBIN','SHREECEM','SIEMENS','SOUTHBANK','SREINFRA','SRF','SRTRANSFIN','STAR','SUNPHARMA','SUNTV','SUZLON','SYNDIBANK','TATACHEM','TATACOMM','TATAELXSI','TATAGLOBAL','TATAMOTORS','TATAMTRDVR','TATAPOWER','TATASTEEL','TCS','TECHM','TITAN','TORNTPHARM','TORNTPOWER','TV18BRDCST','TVSMOTOR','UBL','UJJIVAN','ULTRACEMCO','UNIONBANK','UPL','VEDL','VGUARD','VOLTAS','WIPRO','WOCKPHARMA','YESBANK','ZEEL']

reportcol=['symbol', 'Days', 'RSI', 'BBANDS', 'MA1', 'MA2', 'MA3', 'MA4', 'MSE', 'RMSE','Dates','Actual', 'Forcasted','model']

reportname = str(date.today())+'_technicalreport.csv'
tech_reportname='technicalreport.csv'
mod_reportname = str(date.today())+'_mod_technicalreport.csv'
final_reportname = str(date.today())+'_final_technicalreport.csv'
reportpath = os.path.join(repobasepath,reportname)
techreport=os.path.join(repobasepath,tech_reportname)
mod_reportpath = os.path.join(repobasepath,mod_reportname)
final_reportpath = os.path.join(repobasepath,final_reportname)

########Get symboldata property###################################
y=2011
m=1
d=1

################### Data preprocessing property ##################
test_size=0.3

##################### LSTM model Property ########################
LSTM_units = 50
LSTM_unit_increment = 30
dropoutunit = 0.2
epochs=1


################## Random Forest Property #########################
n_estimators=1000
n_jobs=-1
seed=5
n_splits=10

######################## SVR Property##############################
kernel='rbf'
C=1e3
gamma=0.3

##################### Model List ####################################
modelslist=['SVR','RF','RNN']   # This is list of all the models
models=['SVR']      # This is list of models to be used at run time.