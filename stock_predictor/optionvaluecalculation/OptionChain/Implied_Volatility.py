import datetime

import pandas as pd
from nsepy.derivatives import get_expiry_date

import property as p
from optionvaluecalculation.OptionChain import optionChainData
import dask.dataframe as dd
import mibian

from optionvaluecalculation.OptionChain.optionChainData import get_tradingDay


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
            Df = dd.read_csv(self.Dffile)
        else:
            optionChainData.appendData()  # get the Latest data.
            currentFile = optionChainData.get_OptionFile(True) # Get current month Option Data File.
            Df = pd.read_csv(currentFile)
            return Df

    def getSymbolStrike(self,symbol="NIFTY",Df=pd.DataFrame()):
        def getDateStrike(i):
            temp_Close = Df_F.loc[Df_F['Date'] == i]['CLOSE'].tolist()[0]
            exp_date = Df_F.loc[Df_F['CLOSE'] == temp_Close]['EXPIRY_DT'].tolist()[0]
            temp_OI = DF_O.loc[DF_O['Date'] == i]['STRIKE_PR'].tolist()[-2:]
            diff = abs(temp_OI[0] - temp_OI[1])
            Strike_High = temp_Close + (diff - (temp_Close % diff))  # Get smallest no from larger no then Close
            Strike_Low = temp_Close + - (temp_Close % diff)  # Get largest no from smaller then Close
            Strike_High_mask_CE = (DF_O['Date'] == i)\
                                  & (DF_O['STRIKE_PR'] == Strike_High)\
                                  & (DF_O['EXPIRY_DT'] == exp_date)\
                                  & (DF_O['OPTION_TYP'] == 'CE')

            Strike_High_mask_PE = (DF_O['Date'] == i) \
                                  & (DF_O['STRIKE_PR'] == Strike_High) \
                                  & (DF_O['EXPIRY_DT'] == exp_date) \
                                  & (DF_O['OPTION_TYP'] == 'PE')

            Strike_Low_mask_CE = (DF_O['Date'] == i) \
                                  & (DF_O['STRIKE_PR'] == Strike_Low) \
                                  & (DF_O['EXPIRY_DT'] == exp_date) \
                                  & (DF_O['OPTION_TYP'] == 'CE')

            Strike_Low_mask_PE = (DF_O['Date'] == i) \
                                  & (DF_O['STRIKE_PR'] == Strike_Low) \
                                  & (DF_O['EXPIRY_DT'] == exp_date) \
                                  & (DF_O['OPTION_TYP'] == 'PE')


            CE_High = DF_O.loc[Strike_High_mask_CE]['CLOSE'].tolist()[0]
            CE_Low = DF_O.loc[Strike_Low_mask_CE]['CLOSE'].tolist()[0]
            PE_High = DF_O.loc[Strike_High_mask_PE]['CLOSE'].tolist()[0]
            PE_Low = DF_O.loc[Strike_Low_mask_PE]['CLOSE'].tolist()[0]
            days_to_expire = int(get_tradingDay(i,exp_date,False))

            CE_H_I = mibian.Me([temp_Close, Strike_High, 7, 0, days_to_expire], callPrice=CE_High).impliedVolatility
            CE_L_I = mibian.Me([temp_Close, Strike_Low, 7, 0, days_to_expire], callPrice=CE_Low).impliedVolatility
            PE_H_I = mibian.Me([temp_Close, Strike_High, 7, 0, days_to_expire], putPrice=PE_High).impliedVolatility
            PE_L_I = mibian.Me([temp_Close, Strike_Low, 7, 0, days_to_expire], putPrice=PE_Low).impliedVolatility

            self.striklist.append([i, symbol, exp_date, temp_Close, Strike_High,
            Strike_Low, CE_H_I, CE_L_I, PE_H_I, PE_L_I,days_to_expire])

        mask_F = (Df['SYMBOL'] == symbol) & (Df['INSTRUMENT']  == 'FUTIDX')
        mask_O = (Df['SYMBOL'] == symbol) & (Df['INSTRUMENT'] == 'OPTIDX')
        Df_F = Df.loc[mask_F]
        DF_O = Df.loc[mask_O]

        Dates_F = pd.Series(Df.loc[mask_F]['Date'].unique())
        Dates_F.apply(getDateStrike)

    def getStrike(self):
        header = str("")
        # print(header)
        Df = self.load_Data()
        #symbols = Df['SYMBOL']
        symbolstest=['NIFTY']#,'BANKNIFTY','NIFTYCPSE']
        symbols = pd.Series(symbolstest)
        symbols.apply(self.getSymbolStrike,Df=Df)
        self.striklist = pd.DataFrame(
            self.striklist,
            columns=['Date', 'symbol', 'exp_date', 'temp_Close', 'Strike_High',
                     'Strike_Low', 'CE_H_I', 'CE_L_I', 'PE_H_I', 'PE_L_I', 'days_to_expire'])
        # print(self.striklist)
        self.striklist.to_csv("strikelist.csv")








implobj = ImpliedVolatility()
implobj.getStrike()