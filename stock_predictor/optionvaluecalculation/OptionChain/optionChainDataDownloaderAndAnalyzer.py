
import requests
import json
#import logging
#import http.client
import pandas as pd
import xlwings as xw
from time import sleep
from datetime import datetime,time,timedelta
import os
import property as p
import numpy as np


pd.set_option("display.width",1500)
pd.set_option("display.max_columns",75)
pd.set_option("display.max_rows",150)



request_url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
banknifyurl = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
nifyurl = f"https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
expiry = "08-Apr-2021"
#expiry =None
excle_file= "option_chain_analysis.xlsx"
wb = xw.books(excle_file)
oidata_sheet = wb.sheets("oidata")


main_sheet = wb.sheets("maindata")
df_list=[]

mp_list= []
#oi_data_file = os.path.join(p.optionchaindata,"oi_data_records_{0}.json".format(datetime.now().strftime("%d%m%y")))
#oi_data_file = os.path.normpath(oi_data_file)

#mp_data_file = os.path.join(p.optionchaindata,"mp_data_records_{0}.json".format(datetime.now().strftime("%d%m%y")))
#mp_data_file = os.path.normpath(mp_data_file)

oi_data_file = "oi_data_records_{0}.json".format(datetime.now().strftime("%d%m%y"))
mp_data_file = "mp_data_records_{0}.json".format(datetime.now().strftime("%d%m%y"))



timeFrame = 3
loadFromFile = False


def fetchChainData(url ,symbol):
    all_chain_data = "all_day_oi_data_records_{0}_{1}.json".format(symbol,datetime.now().strftime("%d%m%y"))
    url_oc = "https://www.nseindia.com/option-chain"
    url = url
  # url = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    #print(response.json())

    with open(all_chain_data,"a") as files:
        files.write(json.dumps(response.json(),indent=4,sort_keys=True))
    return response.json(),all_chain_data

def readJson(filename):
    with open(filename,"r") as files:
        data = json.load(files)
    #print(data)
    return data

def loadandAnalyzeChainData(df,mp_df,requestdata):
    #print(requestdata)
    tries = 0
    maxtries =0
    while tries <= maxtries:
        try:
            expirly_list= [ '29-Apr-2021','06-May-2021']
            print("Expiry list is " ,expirly_list)
            for expirday in expirly_list :
                if expirly_list.index(expirday)==0:
                    print("expirty index 0")
                    expiry= None
                else:
                    print("expirty index 1")
                    expiry =expirday

                if expiry:
                    print("expire provided")
                    ce_values = [data['CE'] for data in requestdata['records']['data'] if 'CE' in data and str(data['expiryDate']).lower() ==str(expiry).lower()]
                    pe_values = [data['PE'] for data in requestdata['records']['data'] if 'PE' in data and str(data['expiryDate']).lower() ==str(expiry).lower()]
                else:
                    print("expire not provided")
                    ce_values = [data['CE'] for data in requestdata['filtered']['data'] if 'CE' in data]
                    pe_values = [data['PE'] for data in requestdata['filtered']['data'] if 'PE' in data]
                ce_data = pd.DataFrame(ce_values)
                pe_data = pd.DataFrame(pe_values)
                ce_data=ce_data.sort_values("strikePrice")
                pe_data= pe_data.sort_values("strikePrice")
                #print(ce_data)
                #print(ce_values)
                #oidata_sheet.range("A2").options().value =ce_data.drop(['askPrice','askQty'	,'bidQty','bidprice','expiryDate','identifier','totalBuyQuantity' ,'totalSellQuantity' ,'totalTradedVolume','underlying','underlyingValue' ])
                oidata_sheet.range("A2").options(index= False,header =False).value = ce_data.drop(
                    ['askPrice', 'askQty', 'bidQty', 'bidprice', 'expiryDate', 'identifier',
                     'totalBuyQuantity','totalSellQuantity', 'totalTradedVolume', 'underlying', 'underlyingValue'], axis=1)
                oidata_sheet.range("I2").options(index=False,header = False).value = pe_data.drop(
                    ['askPrice', 'askQty', 'bidQty', 'bidprice', 'expiryDate', 'identifier',
                     'totalBuyQuantity', 'totalSellQuantity', 'totalTradedVolume', 'underlying', 'underlyingValue','strikePrice'], axis=1)
                ce_data['type'] = "CE"
                pe_data ['type']  = 'PE'
                df1 = pd.concat([ce_data,pe_data])
                if len(df_list) >0:
                    df1["Time"] = df_list[-1][0]["Time"]
                if len(df_list ) > 0 and df1.to_dict("records") ==df_list[-1]:
                    print("duplicate data , not recording")
                    sleep(10)
                    tries+=1
                    continue
                df1["Time"] =  datetime.now().strftime("%H:%M")

                pcr = pe_data["totalTradedVolume"].sum()/ce_data["totalTradedVolume"].sum()
                mp_dict = {datetime.now().strftime("%H:%M"):{"underlying": df1["underlyingValue"].iloc[-1],
                                                             "maxpain":0,
                                                             "pcr":pcr,
                                                             "call_decay":ce_data.nlargest(5,'openInterest',keep = 'last')['change'].mean(),
                                                             "put_decay":pe_data.nlargest(5,'openInterest',keep = 'last')['change'].mean()}}
                df3 = pd.DataFrame(mp_dict).transpose()
                mp_df = pd.concat([mp_df,df3])
                wb.sheets["mpdata"].range("A1").options(headers = False).value = mp_df

                df = pd.concat([df,df1])
                df_list.append(df1.to_dict('records'))
                with open(mp_data_file, "w") as files:
                    files.write(json.dumps(mp_df.to_dict(), indent=4, sort_keys=True))

                with open(oi_data_file, "w") as files:
                    files.write(json.dumps(df_list, indent=4, sort_keys=True))

            return  df,mp_df
        except Exception as error:
            print("Error executing error {0}".format(error))
            tries = tries+1
            sleep(10)
            continue

    if tries > maxtries:
        print("max tries exceeded no more data time{0}".format(datetime.now()))
        return df, mp_df
def main():
    global df_list
    try:
        df_list = readJson(oi_data_file)
    except Exception as error :
        print("Error reading data  error {0}".format(error))
        df_list =[]

    if df_list:
        df = pd.DataFrame()
        for item in df_list:
            df = pd.concat([df,pd.DataFrame(item)])
    else:
        df = pd.DataFrame()

    try:
        mp_list = readJson(mp_data_file)
        mp_df = pd.DataFrame().from_dict(mp_list)
    except Exception as error :
        print("Error reading data  error {0}".format(error))
        mp_list =[]
        mp_df =pd.DataFrame()



    print("time now is ",datetime.now())
    while (True):
        while time(6,14) <= datetime.now().time() <= time(15,32):
            timenow = datetime.now()
            check = True if timenow.minute/timeFrame in list(np.arange(0.0, 20.0)) else False

            if check:
                if loadFromFile:
                    data = readJson("all_day_oi_data_records_BANKNIFTY_290321.json")
                else:
                    jsondata, filename = fetchChainData(banknifyurl, "BANKNIFTY")
                    print("filename is ", filename)
                    data = jsondata

                nextScan = timenow + timedelta(minutes=timeFrame)

                df,mp_df = loadandAnalyzeChainData(df,mp_df,data)

                if not df.empty:
                    df["impliedVolatility"] = df["impliedVolatility"].replace(to_replace=0,method='bfill').values
                    df['idetifire'] = df['strikePrice'].astype(str)+df['type']
                    main_sheet.range("A1").value = df
                    waitSec =  int((nextScan-datetime.now()).seconds)
                    print("wait for seconds {0}".format(waitSec))
                    sleep(waitSec) if waitSec >0 else sleep(0)
                else:
                    print("no data received")
                    sleep(30)



if __name__ == "__main__":
   main()
