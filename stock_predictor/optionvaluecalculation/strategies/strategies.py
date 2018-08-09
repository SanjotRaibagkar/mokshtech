from optionvaluecalculation.utility import extract_table
import numpy as np
import pandas as pd

def get_Data():
    #df, Spot_Price, strike_price_diff, strikelist, Highlist, Lowlist =
    # extract_table.extract_table('index', 'NIFTY')

    Spot_Price, strike_price_diff, strikelist, Highlist, Lowlist =\
        11387.1,50, [11200.0, 11250.0, 11300.0, 11350.0, 11400.0, 11350.0, 11400.0, 11450.0, 11500.0, 11550.0],\
    [11200.0, 11250.0, 11300.0, 11350.0, 11400.0],[11350.0, 11400.0, 11450.0, 11500.0, 11550.0]

    df = pd.read_csv('df.csv')
    print(strikelist)
    tot_data = len(df)
    df = df.to_dict('record')
    df_dict = {}
    for i in range(0, tot_data):
        if float(df[i]['Strike_Price']) in set(strikelist):
            data_ut = df[i]
            strike_price, C_LTP, P_LTP = data_ut['Strike_Price'], data_ut['C_LTP'], data_ut['P_LTP']
            df_dict[float(strike_price)] = float(strike_price), float(C_LTP), float(P_LTP)
        else:
            pass
    return Spot_Price,strikelist, Highlist, Lowlist,df_dict
def calculate_max_reward(payoff):
    max_profit = np.nanmax(payoff)
    max_loss = abs(np.nanmin(payoff))

    maxindex = np.where(payoff == max_profit)[0][0]
    minindex = np.where(payoff == np.nanmin(payoff))[0][0]
    # print(sT[maxindex],sT[minindex])

    risk_reward_ratio = max_profit / max_loss
    return maxindex,max_profit,minindex,max_loss,risk_reward_ratio

def call_payoff(sT, strike_price, premium):
    return np.where(sT > strike_price, sT - strike_price, 0) - premium


def put_payoff(sT, strike_price, premium):
    print(strike_price)
    return np.where(sT < strike_price, strike_price - sT, 0) - premium

def get_maxriskrwward():

    #
    # import matplotlib.pyplot as plt
    # import seaborn

    # file = 'NIFTY.csv'
    #
    #
    # df = pd.read_csv(file)
    Spot_Price, strikelist, Highlist, Lowlist, df_dict = get_Data()
    put_exp_range = 0.2

    sT = np.arange((1-put_exp_range)*Spot_Price,(1+put_exp_range)*Spot_Price,1)

    getPayoffALL={}
    def getPayoffALL(sT,strike_price,C_LTP,P_LTP):

        maxindex, max_profit, minindex, max_loss, risk_reward_ratio = calculate_max_reward(call_payoff (sT, strike_price, C_LTP))
        payoff_list.append([Spot_Price,sT[maxindex], max_profit, sT[minindex], max_loss, risk_reward_ratio ,'payoff_long_call'])

        maxindex, max_profit, minindex, max_loss, risk_reward_ratio = calculate_max_reward(call_payoff(sT, strike_price, C_LTP) * -1.0)
        payoff_list.append([Spot_Price,sT[maxindex], max_profit, sT[minindex], max_loss, risk_reward_ratio ,'payoff_short_call'])

        # payoff_long_put = put_payoff(sT, strike_price, P_LTP)
        # payoff_Short_put = put_payoff(sT, strike_price, P_LTP)*-1.0
        # stock_payoff = (sT - Spot_Price)*-1.0
        #
        # payoff_straddle = payoff_long_call + payoff_long_call
        #
        #
        # maxindex, max_profit, minindex, max_loss, risk_reward_ratio = calculate_max_reward(call_payoff(sT, strike_price, C_LTP) * -1.0)


    columns = ['Spot_Price','sT[maxindex]', 'max_profit', 'sT[minindex]', 'max_loss', 'risk_reward_ratio' ,'payoff']
    payoff_df = pd.DataFrame(columns=columns)
    payoff_list =[]
    for i in strikelist:
        #strike_price = float(i)
        C_LTP = df_dict[i][1]
        P_LTP = df_dict[i][2]
        getPayoffALL(sT,i,C_LTP,P_LTP)
        payoff_df=pd.DataFrame(payoff_list,columns=columns)
    print(payoff_df.head(3))
        # print(max_profit,max_loss,risk_reward_ratio)
        # # Plot
        # # fig, ax = plt.subplots()
        # # ax.spines['top'].set_visible(False) # Top border removed
        # # ax.spines['right'].set_visible(False) # Right border removed
        # # ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
        # # ax.plot(sT,payoff_long_call,label='Long Call',color='r')
        # # plt.xlabel('Stock Price')
        # # plt.ylabel('Profit and loss')
        # # plt.legend()
        # # plt.show()


get_maxriskrwward()