import numpy as np
import pandas as pd


def get_maxriskrwward():
    import numpy as np
    import pandas as pd
    #
    # import matplotlib.pyplot as plt
    # import seaborn

    file = 'stddle_ip.csv'


    df = pd.read_csv(file)
    tot_data = len(df)
    df = df.to_dict('record')
    for i in range(0,tot_data):
        data_ut = df[i]

        Symbol, Spot_Price, Long_put_StPr, Long_put_prm, \
        Short_put_StPr, Short_put_prm,\
        Long_call_StPr, Long_call_prm, put_exp_range, \
        Short_call_StPr, Short_call_prm= \
            data_ut['Symbol'], data_ut['Spot_Price'], data_ut['Long_put_StPr'],\
            data_ut['Long_put_prm'],data_ut['Short_put_StPr'], data_ut['Short_put_prm'],\
            data_ut['Long_call_StPr'], data_ut['Long_call_prm'],\
            data_ut['put_exp_range'], data_ut[put_exp_range],
        data_ut['Short_call_StPr'], data_ut['Short_call_prm']

    sT = np.arange((1-put_exp_range)*Spot_Price,(1+put_exp_range)*Spot_Price,1)

    def call_payoff(sT, strike_price, premium):
        print(strike_price)
        return np.where(sT > strike_price, sT - strike_price, 0) - premium

    payoff_long_call = call_payoff (sT, Long_call_StPr, Long_call_prm)

    payoff_short_call = call_payoff(sT, Short_call_StPr, Short_call_prm) * -1.0

    def put_payoff(sT, strike_price, premium):
        print(strike_price)
        return np.where(sT < strike_price, strike_price - sT, 0) - premium



    payoff_long_put = put_payoff(sT, Long_put_StPr, Long_put_prm)
    payoff_Short_put = put_payoff(sT, Short_put_StPr, Short_put_prm)*-1.0
    stock_payoff = (sT - Spot_Price)*-1.0

    print(payoff_long_put)

    payoff_straddle = payoff_long_call + payoff_long_call


    max_profit = np.nanmax(payoff_straddle)
    max_loss = abs(np.nanmin(payoff_straddle))

    maxindex = np.where(payoff_straddle==max_profit)[0][0]
    minindex = np.where(payoff_straddle==np.nanmin(payoff_straddle))[0][0]
    print("ok")
    print(sT[maxindex],sT[minindex])


    risk_reward_ratio = max_profit/max_loss

    print(max_profit,max_loss,risk_reward_ratio)
    # Plot
    # fig, ax = plt.subplots()
    # ax.spines['top'].set_visible(False) # Top border removed
    # ax.spines['right'].set_visible(False) # Right border removed
    # ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
    # ax.plot(sT,payoff_long_call,label='Long Call',color='r')
    # plt.xlabel('Stock Price')
    # plt.ylabel('Profit and loss')
    # plt.legend()
    # plt.show()


class Strategies():
    def __init__(self):
        pass

    def call_payoff(self,sT, strike_price, premium):
        '''
        1. Long Pay off
        When to Use: Investor is very bullish on the stock / index.
        Risk: Limited to the Premium.
        (Maximum loss if market expires at or below the option strike price).
        Reward: Unlimited
        Breakeven: Strike Price + Premium

        :param sT: Spot price list
        :param strike_price: strike price
        :param premium: premium
        :return: List for call payoff for each spot price.
        '''
        return np.where(sT > strike_price, sT - strike_price, 0) - premium

    payoff_long_call = call_payoff (sT, Long_call_StPr, Long_call_prm)

    payoff_short_call = call_payoff(sT, Short_call_StPr, Short_call_prm) * -1.0
