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

class ImpliedVolatility(object):
    """"""
    def __init__(self,symbol="NIFTY",Dffile='abc.csv',DfFlag=False):
        self.DfFlag = DfFlag
        self.Dffile = Dffile
        self.Symbol = symbol
        self.striklist=[]


    def load_Data(self):
        """
        if Data frame is passed while class initilisation use the same dataframe
        else get the latest dataframe
        :return: Dataframe of sybol
        """
        if self.DfFlag:
            Df = pd.read_csv(self.Dffile)
        else:
            #optionChainData.appendData()  # get the Latest data.
            currentFile = optionChainData.get_OptionFile(True) # Get current month Option Data File.
            lastDate = getstart.get_date(currentFile,Options=True)
            print(lastDate)
            Df = pd.read_csv(currentFile)
        return Df

    def save_data(self,list):
        self.striklist_DF = pd.DataFrame(
            list,
            columns=['Date', 'symbol', 'exp_date', 'temp_Close', 'Strike_High',
                     'Strike_Low', 'CE_H_I', 'CE_L_I', 'PE_H_I', 'PE_L_I', 'days_to_expire',
                     'OI_CE_High', 'OI_CE_Low', 'OI_PE_High', 'OI_PE_Low',
                     'COI_CE_High', 'COI_CE_Low', 'COI_PE_High', 'COI_PE_Low'
                     ])
        if os.path.isfile(OptionsIV):
            self.striklist_DF.to_csv(OptionsIV, mode='a', header=False)
        else:
            self.striklist_DF.to_csv(OptionsIV, header=True)

    def getSymbolStrike(self,symbol="NIFTY",Df=pd.DataFrame(),x=0):
        def getDateStrike(i):
            strlist = []

            DF_test = DF_O.loc[DF_O[date] == i]

            a = OIMAXPAIN.findmaxpain(symbol,DF_test)
            print("++++++++++",a)




            # temp_Close = Df_F.loc[Df_F[date] == i][close].tolist()[x]
            # exp_date = Df_F.loc[Df_F[close] == temp_Close]['EXPIRY_DT'].tolist()[0]
            # temp_OI = DF_O.loc[DF_O[date] == i]['STRIKE_PR'].tolist()[-2:]
            # diff = abs(temp_OI[0] - temp_OI[1])
            # Strike_High = temp_Close + (diff - (temp_Close % diff))  # Get smallest no from larger no then Close
            # Strike_Low = temp_Close + - (temp_Close % diff)  # Get largest no from smaller then Close
            # Strike_High_mask_CE = (DF_O[date] == i)\
            #                       & (DF_O['STRIKE_PR'] == Strike_High)\
            #                       & (DF_O['EXPIRY_DT'] == exp_date)\
            #                       & (DF_O['OPTION_TYP'] == 'CE')
            #
            # Strike_High_mask_PE = (DF_O[date] == i) \
            #                       & (DF_O['STRIKE_PR'] == Strike_High) \
            #                       & (DF_O['EXPIRY_DT'] == exp_date) \
            #                       & (DF_O['OPTION_TYP'] == 'PE')
            #
            # Strike_Low_mask_CE = (DF_O[date] == i) \
            #                       & (DF_O['STRIKE_PR'] == Strike_Low) \
            #                       & (DF_O['EXPIRY_DT'] == exp_date) \
            #                       & (DF_O['OPTION_TYP'] == 'CE')
            #
            # Strike_Low_mask_PE = (DF_O[date] == i) \
            #                       & (DF_O['STRIKE_PR'] == Strike_Low) \
            #                       & (DF_O['EXPIRY_DT'] == exp_date) \
            #                       & (DF_O['OPTION_TYP'] == 'PE')
            #
            #
            # CE_High = DF_O.loc[Strike_High_mask_CE][close].tolist()[0]
            # CE_Low = DF_O.loc[Strike_Low_mask_CE][close].tolist()[0]
            # PE_High = DF_O.loc[Strike_High_mask_PE][close].tolist()[0]
            # PE_Low = DF_O.loc[Strike_Low_mask_PE][close].tolist()[0]
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
            #
            #
            #
            #
            # days_to_expire = int(get_tradingDay(i,exp_date,False))
            #
            # CE_H_I = mibian.Me([temp_Close, Strike_High, 7, 0, days_to_expire], callPrice=CE_High).impliedVolatility
            # CE_L_I = mibian.Me([temp_Close, Strike_Low, 7, 0, days_to_expire], callPrice=CE_Low).impliedVolatility
            # PE_H_I = mibian.Me([temp_Close, Strike_High, 7, 0, days_to_expire], putPrice=PE_High).impliedVolatility
            # PE_L_I = mibian.Me([temp_Close, Strike_Low, 7, 0, days_to_expire], putPrice=PE_Low).impliedVolatility
            #
            # strlist.append([i, symbol, exp_date, temp_Close, Strike_High,Strike_Low,
            #                 CE_H_I, CE_L_I, PE_H_I, PE_L_I, days_to_expire,
            #                 OI_CE_High, OI_CE_Low, OI_PE_High, OI_PE_Low,
            #                 COI_CE_High, COI_CE_Low, COI_PE_High, COI_PE_Low])
            #
            # implobj = ImpliedVolatility()
            # implobj.save_data(strlist)
        mask_F = (Df['SYMBOL'] == symbol) & (Df['INSTRUMENT'].str.contains('FUT'))
        mask_O = (Df['SYMBOL'] == symbol) & (Df['INSTRUMENT'].str.contains('OPT'))
        Df_F = Df.loc[mask_F]
        DF_O = Df.loc[mask_O]

        Dates_F = pd.Series(Df.loc[mask_F]['Date'].unique())
        #try:
        Dates_F.apply(getDateStrike)
        #except Exception as e:
        #print("error Implied_Volatility1 ",Dates_F, e)
        # self.save_data()

    def getStrike(self):
        Df = self.load_Data()
        symbols = Df['SYMBOL'].unique()
        # symbolstest=['NIFTY',
        #              'BANKNIFTY',
        #              'NIFTYCPSE',
        #              'ARVIND'
        #              ]
        # symbols = pd.Series(symbols)
        x_no = [0,1,2]
        try:
            #a = list(map(lambda x:symbols.apply(self.getSymbolStrike,args=(Df=Df,x=x,)),x_no))
            for i in symbols:
                try:
                    for j in x_no:
                        self.getSymbolStrike(symbol=i,Df=Df,x=j)
                except Exception as e:
                    print("error Implied_Volatility2 ", i, j, e, x_no)
        except Exception as e:
            print("error Implied_Volatility2 ",i,j,e,x_no)

if __name__ == '__main__':
    implobj = ImpliedVolatility()
    implobj.getStrike()