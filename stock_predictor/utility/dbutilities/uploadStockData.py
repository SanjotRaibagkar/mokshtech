import os
import property as p
from utility.dbutilities import dbqueries as dbq
from utility.dbutilities.dbproperties import *
import nsepy
import psycopg2
from nsetools import Nse
import pandas as pd



#  ['ACC.csv', 'ADANIENT.csv', 'ADANIPORTS.csv', 'ADANIPOWER.csv', 'AJANTPHARM.csv', 'ALBK.csv', 'AMARAJABAT.csv', 'AMBUJACEM.csv', 'ANDHRABANK.csv', 'APOLLOHOSP.csv', 'APOLLOTYRE.csv', 'ARVIND.csv', 'ASHOKLEY.csv', 'ASIANPAINT.csv', 'AUROPHARMA.csv', 'AXISBANK.csv', 'BAJAJ-AUTO.csv', 'BAJAJFINSV.csv', 'BAJFINANCE.csv', 'BALKRISIND.csv', 'BALRAMCHIN.csv', 'BANKBARODA.csv', 'BANKINDIA.csv', 'BANKNIFTY.csv', 'BATAINDIA.csv', 'BEL.csv', 'BEML.csv', 'BERGEPAINT.csv', 'BHARATFIN.csv', 'BHARATFORG.csv', 'BHARTIARTL.csv', 'BHEL.csv', 'BIOCON.csv', 'BOSCHLTD.csv', 'BPCL.csv', 'BRITANNIA.csv', 'CADILAHC.csv', 'CANBK.csv', 'CANFINHOME.csv', 'CAPF.csv', 'CASTROLIND.csv', 'CEATLTD.csv', 'CENTURYTEX.csv', 'CESC.csv', 'CGPOWER.csv', 'CHENNPETRO.csv', 'CHOLAFIN.csv', 'CIPLA.csv', 'COALINDIA.csv', 'COLPAL.csv', 'CONCOR.csv', 'CUMMINSIND.csv', 'DABUR.csv', 'DALMIABHA.csv', 'DCBBANK.csv', 'DHFL.csv', 'DISHTV.csv', 'DIVISLAB.csv', 'DLF.csv', 'DRREDDY.csv', 'EICHERMOT.csv', 'ENGINERSIN.csv', 'EQUITAS.csv', 'ESCORTS.csv', 'EXIDEIND.csv', 'FEDERALBNK.csv', 'GAIL.csv', 'GLENMARK.csv', 'GMRINFRA.csv', 'GODFRYPHLP.csv', 'GODREJCP.csv', 'GODREJIND.csv', 'GRANULES.csv', 'GRASIM.csv', 'GSFC.csv', 'HAVELLS.csv', 'HCC.csv', 'HCLTECH.csv', 'HDFC.csv', 'HDFCBANK.csv', 'HEROMOTOCO.csv', 'HEXAWARE.csv', 'HINDALCO.csv', 'HINDPETRO.csv', 'HINDUNILVR.csv', 'HINDZINC.csv', 'IBULHSGFIN.csv', 'ICICIBANK.csv', 'ICICIPRULI.csv', 'IDBI.csv', 'IDEA.csv', 'IDFC.csv', 'IDFCBANK.csv', 'IFCI.csv', 'IGL.csv', 'INDIACEM.csv', 'INDIANB.csv', 'INDIGO.csv', 'INDUSINDBK.csv', 'INFIBEAM.csv', 'INFRATEL.csv', 'INFY.csv', 'IOC.csv', 'IRB.csv', 'ITC.csv', 'JETAIRWAYS.csv', 'JINDALSTEL.csv', 'JISLJALEQS.csv', 'JPASSOCIAT.csv', 'JSWSTEEL.csv', 'JUBLFOOD.csv', 'JUSTDIAL.csv', 'KAJARIACER.csv', 'KOTAKBANK.csv', 'KPIT.csv', 'KSCL.csv', 'KTKBANK.csv', 'L&TFH.csv', 'LICHSGFIN.csv', 'LT.csv', 'LUPIN.csv', 'M&M.csv', 'M&MFIN.csv', 'MANAPPURAM.csv', 'MARICO.csv', 'MARUTI.csv', 'MCDOWELL-N.csv', 'MCX.csv', 'MFSL.csv', 'MGL.csv', 'MINDTREE.csv', 'MOTHERSUMI.csv', 'MRF.csv', 'MRPL.csv', 'MUTHOOTFIN.csv', 'NATIONALUM.csv', 'NBCC.csv', 'NCC.csv', 'NESTLEIND.csv', 'NHPC.csv', 'NIFTY.csv', 'NIFTYINFRA.csv', 'NIFTYIT.csv', 'NIFTYMID50.csv', 'NIFTYPSE.csv', 'NIITTECH.csv', 'NMDC.csv', 'NTPC.csv', 'OFSS.csv', 'OIL.csv', 'ONGC.csv', 'ORIENTBANK.csv', 'PAGEIND.csv', 'PCJEWELLER.csv', 'PEL.csv', 'PETRONET.csv', 'PFC.csv', 'PIDILITIND.csv', 'PNB.csv', 'POWERGRID.csv', 'PTC.csv', 'SYNDIBANK_F1.csv', 'TCS.csv', 'uploadStockData.py']

def uploadData(x,table):
    print(x)
    try:
        with open(x, 'r') as f:
            # Notice that we don't need the `csv` module.
            next(f)  # Skip the header row.
            cur.copy_from(f, table, sep=',')
    except Exception as e:
        print(x,e)
    finally:
        pass
        conn.commit()


stocklist=[]
indlist = []
for a,b,c in os.walk(p.stockdatadelta):
    indlist=['FTSE100','INDIAVIX','NIFTYCPSE','NIFTY','NIFTYIT','BANKNIFTY','NIFTYMID50','NIFTYPSE','NIFTYINFRA']
    c = list(set(c)-set(indlist))
    for files in c:
        #files=files+'.csv'
        if not files.startswith("symbolList.csv"):
            stocklist.append(os.path.join(p.stockdatadelta,files))
    for files in indlist:
        if not files.startswith("symbolList.csv"):
            indlist.append(os.path.join(p.stockdatadelta,files))
stocklist = pd.Series(stocklist)
indlist = pd.Series(indlist)

optionsList=[]
for d, s, files in os.walk(p.optiondata_day):
    for f in files:
        if f.startswith("prices"):
            optionsList.append(os.path.join(p.optiondata_day, f))

optionsList=pd.Series(optionsList)

# stocklist = pd.Series(filelist)
# stocklist.apply(uploadData)

def upload_OptionsData():
    optionsList.apply(uploadData,args=('derivativeData',))
def upload_StockData():
    stocklist.apply(uploadData,args=('StockData',))
    indlist.apply(uploadData)


if __name__ == '__main__':

    dbobj = dbq.db_queries()
    conn = dbobj.create_connection()
    cur = conn.cursor()
    upload_StockData()