import datetime
import pandas as pd
import os
import mibian

from utility import getstart
import property as p
from optionvaluecalculation.OptionChain import optionChainData
from optionvaluecalculation.OptionChain.optionChainData import get_tradingDay
from optionvaluecalculation.optionvalueprop import *
from optionvaluecalculation.OptionChain import OIMAXPAIN
from optionvaluecalculation.utility import getStrikes
from utility.dbutilities.dbproperties import sqlmokshtechdb
from utility.dbutilities.dbqueries import *
class ImpliedVolatility(object):
    """"""
    def __init__(self,conn,dbq,symbol="NIFTY",Dffile='abc.csv',DfFlag=False):
        self.DfFlag = DfFlag
        self.Dffile = Dffile
        self.Symbol = symbol
        self.striklist=[]
        self.dbq = dbq
        self.con = conn

    def load_Data(self):
        """
        if Data frame is passed while class initilisation use the same dataframe
        else get the latest dataframe
        :return: Dataframe of sybol
        """
        if self.DfFlag:
            Df = pd.read_csv(self.Dffile)
        else:
            optionChainData.appendData()  # get the Latest data.
            # currentFile = 'prices_2018_5.csv' #optionChainData.get_OptionFile(True) # Get current month Option Data File.
            # lastDate = getstart.get_date(currentFile,Options=True)
            # print(lastDate)
            currentFile = os.path.join(p.optiondata,"prices_2018_7.csv")
            Df = pd.read_csv(currentFile)
        return Df

    def save_data(self,list):
        self.striklist_DF = pd.DataFrame(
            list,
            columns=['Date', 'symbol', 'exp_date', 'temp_Close', 'Strike_High',
                     'Strike_Low', 'CE_H_I', 'CE_L_I', 'PE_H_I', 'PE_L_I', 'days_to_expire',
                     'ce_maxpain', 'pe_maxpain', 'maxpain', 'mp_strike_pr',
                     'CE_OI_Max2_St_Pr', 'CE_OI_Max2_CHG_OI',
                     'CE_OI_Max1_St_Pr', 'CE_OI_Max1_CHG_OI',
                     'PE_OI_Max2_St_Pr', 'PE_OI_Max2_CHG_OI',
                     'PE_OI_Max1_St_Pr', 'PE_OI_Max1_CHG_OI'
                     ])
        if os.path.isfile(OptionsIV):
            self.striklist_DF.to_csv(OptionsIV, mode='a', header=False)
        else:
            self.striklist_DF.to_csv(OptionsIV, header=True)
        try:
            self.con = self.dbq.df_sql(self.striklist_DF,tb_MaxpainIV,self.con)
        except Exception as e:
            print("IMP Vol 4 ",e)
            try:
                self.striklist_DF.to_csv(OptionsIV_temp, mode='a', header=False)
                self.con = self.dbq.csv_sql(OptionsIV_temp,tb_MaxpainIV,self.con)
            except Exception as e:
                print("IMP Vol 5 ",e)


    def getSymbolStrike(self,symbol="NIFTY",Df=pd.DataFrame(),x=0):
        print(symbol)
        def getDateStrike(i,dbq,con):
            strlist = []
            temp_Close = Df_F.loc[Df_F[date] == i][close].tolist()[x]
            exp_date = Df_F.loc[Df_F[close] == temp_Close]['EXPIRY_DT'].tolist()[0]

            temp_OI = DF_O.loc[DF_O[date] == i]['STRIKE_PR'].tolist()[-2:]

            diff, Strike_High, Strike_Low = getStrikes.getStrikes(temp_Close,temp_OI)

            # diff = abs(temp_OI[0] - temp_OI[1])
            # Strike_High = temp_Close + (diff - (temp_Close % diff))  # Get smallest no from larger no then Close
            # Strike_Low = temp_Close + - (temp_Close % diff)  # Get largest no from smaller then Close
            Strike_High_mask_CE = (DF_O[date] == i)\
                                  & (DF_O['STRIKE_PR'] == Strike_High)\
                                  & (DF_O['EXPIRY_DT'] == exp_date)\
                                  & (DF_O['OPTION_TYP'] == 'CE')

            Strike_High_mask_PE = (DF_O[date] == i) \
                                  & (DF_O['STRIKE_PR'] == Strike_High) \
                                  & (DF_O['EXPIRY_DT'] == exp_date) \
                                  & (DF_O['OPTION_TYP'] == 'PE')

            Strike_Low_mask_CE = (DF_O[date] == i) \
                                  & (DF_O['STRIKE_PR'] == Strike_Low) \
                                  & (DF_O['EXPIRY_DT'] == exp_date) \
                                  & (DF_O['OPTION_TYP'] == 'CE')

            Strike_Low_mask_PE = (DF_O[date] == i) \
                                  & (DF_O['STRIKE_PR'] == Strike_Low) \
                                  & (DF_O['EXPIRY_DT'] == exp_date) \
                                  & (DF_O['OPTION_TYP'] == 'PE')

            CE_High = DF_O.loc[Strike_High_mask_CE][close].tolist()[0]
            CE_Low = DF_O.loc[Strike_Low_mask_CE][close].tolist()[0]
            PE_High = DF_O.loc[Strike_High_mask_PE][close].tolist()[0]
            PE_Low = DF_O.loc[Strike_Low_mask_PE][close].tolist()[0]

            days_to_expire = int(get_tradingDay(i,exp_date,False))

            CE_H_IV = mibian.Me([temp_Close, Strike_High, 7, 0, days_to_expire], callPrice=CE_High).impliedVolatility
            CE_L_IV = mibian.Me([temp_Close, Strike_Low, 7, 0, days_to_expire], callPrice=CE_Low).impliedVolatility
            PE_H_IV = mibian.Me([temp_Close, Strike_High, 7, 0, days_to_expire], putPrice=PE_High).impliedVolatility
            PE_L_IV = mibian.Me([temp_Close, Strike_Low, 7, 0, days_to_expire], putPrice=PE_Low).impliedVolatility


            DF_test = DF_O.loc[(DF_O[date] == i) & (DF_O['EXPIRY_DT'] == exp_date)]

            mp_strike_pr,mp,r1 = OIMAXPAIN.findmaxpain(symbol,DF_test)
            ce_maxpain, pe_maxpain, maxpain = mp['CE'],mp['PE'],mp['totalpain']

            CE_OI_Max2,CE_OI_Max1 = sorted(r1['CE'].tolist())[-2:]
            PE_OI_Max2,PE_OI_Max1 = sorted(r1['PE'].tolist())[-2:]

            CE_OI_Max2_St_Pr,CE_OI_Max2_CHG_OI = DF_test.loc[DF_test['OPEN_INT'] == CE_OI_Max2][['STRIKE_PR','CHG_IN_OI']].values[0][-2:]
            CE_OI_Max1_St_Pr,CE_OI_Max1_CHG_OI = DF_test.loc[DF_test['OPEN_INT'] == CE_OI_Max1][['STRIKE_PR','CHG_IN_OI']].values[0][-2:]
            PE_OI_Max2_St_Pr,PE_OI_Max2_CHG_OI = DF_test.loc[DF_test['OPEN_INT'] == PE_OI_Max2][['STRIKE_PR','CHG_IN_OI']].values[0][-2:]
            PE_OI_Max1_St_Pr,PE_OI_Max1_CHG_OI = DF_test.loc[DF_test['OPEN_INT'] == PE_OI_Max1][['STRIKE_PR','CHG_IN_OI']].values[0][-2:]

            #

            # OI_CE_High = DF_O.loc[Strike_High_mask_CE][close].tolist()[0]
            # OI_CE_Low = DF_O.loc[Strike_Low_mask_CE][close].tolist()[0]
            # OI_PE_High = DF_O.loc[Strike_High_mask_PE][close].tolist()[0]
            # OI_PE_Low = DF_O.loc[Strike_Low_mask_PE][close].tolist()[0]
            #
            # COI_CE_High = DF_O.loc[Strike_High_mask_CE][close].tolist()[0]
            # COI_CE_Low = DF_O.loc[Strike_Low_mask_CE][close].tolist()[0]
            # COI_PE_High = DF_O.loc[Strike_High_mask_PE][close].tolist()[0]
            # COI_PE_Low = DF_O.loc[Strike_Low_mask_PE][close].tolist()[0]
            #
            #
            strlist.append([i, symbol, exp_date, temp_Close, Strike_High,Strike_Low,
                            CE_H_IV, CE_L_IV, PE_H_IV, PE_L_IV, days_to_expire,
                            ce_maxpain, pe_maxpain, maxpain, mp_strike_pr,
                            CE_OI_Max2_St_Pr, CE_OI_Max2_CHG_OI,
                            CE_OI_Max1_St_Pr, CE_OI_Max1_CHG_OI,
                            PE_OI_Max2_St_Pr, PE_OI_Max2_CHG_OI,
                            PE_OI_Max1_St_Pr, PE_OI_Max1_CHG_OI])
            implobj = ImpliedVolatility(dbq = dbq, conn = con)
            implobj.save_data(strlist)
        mask_F = (Df['SYMBOL'] == symbol) & (Df['INSTRUMENT'].str.contains('FUT'))
        mask_O = (Df['SYMBOL'] == symbol) & (Df['INSTRUMENT'].str.contains('OPT'))
        Df_F = Df.loc[mask_F]
        DF_O = Df.loc[mask_O]
        Dates_F = pd.Series(Df.loc[mask_F]['Date'].unique())
        try:
            dbq = self.dbq
            con = self.con
            Dates_F.apply(getDateStrike,args=(dbq,con))
        except IndexError as e:
            pass
            #log.debug(e)
        except Exception as e:
            print("error Implied_Volatility1 ",Dates_F, e)

    def getStrike(self):
        Df = self.load_Data()
        symbols = Df['SYMBOL'].unique()
        # symbols=['ARVIND','NIFTY',
        #              'BANKNIFTY',
        #              'NIFTYCPSE',
        #              ]
        # symbols = pd.Series(symbols)
        x_no = [0,1,2,3,4,5,6]
        try:
            #a = list(map(lambda x:symbols.apply(self.getSymbolStrike,args=(Df=Df,x=x,)),x_no))
            for i in symbols:
                try:
                    for j in x_no:
                        self.getSymbolStrike(symbol=i,Df=Df,x=j)
                except Exception as e:
                    print("error Implied_Volatility2 ",e ,i, j, x_no)
        except Exception as e:
            print("error Implied_Volatility3 ",e,i,x_no)

if __name__ == '__main__':
    try:
        dbq = db_queries()
        con = dbq.create_connection(db_file=sqlmokshtechdb)
        implobj = ImpliedVolatility(dbq=dbq,conn=con)
        implobj.getStrike()
    except Exception as e:
        print("IMVo 5 ", e)
    finally:
        dbq.close_conn(conn=con)
