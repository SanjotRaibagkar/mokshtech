from optionvaluecalculation.utility import extract_table
import numpy as np
import pandas as pd
import itertools

def get_Data():
    #df, Spot_Price, strike_price_diff, strikelist, Highlist, Lowlist =
    # extract_table.extract_table('index', 'NIFTY')

    Spot_Price, strike_price_diff, strikelist, Highlist, Lowlist =\
        11387.1,50, [11200,11250,11300.0, 11350.0, 11400.0,  11450.0,11500,11550.0],\
        [11200,11250,11300.0, 11350.0],[ 11400.0, 11450.0,11500,11550.0]

    hardpath = "E:\\Prgs\\Code\\mokshtech-1\\stock_predictor\\optionvaluecalculation\\strategies\\df.csv"
    df = pd.read_csv(hardpath)  # This file contains strike price,corrosponding call and put trading prices
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

shares = 1

payoff_columns = ['payoff','Spot_Price','sT[maxindex]', 'max_profit', 'sT[minindex]', 'max_loss','min_loss', 'risk_reward_ratio','strgy','data']

def addRow(ls,df,multilple=False):
    """
    Given a dataframe and a list, append the list as a new row to the dataframe.

    :param df: <DataFrame> The original dataframe
    :param ls: <list> The new row to be added
    :param multilple : <list> if ls contains multiple rows
    :return: <DataFrame> The dataframe with the newly appended row
    """
    if not multilple:
        ls = [ls]

    for i in range(len(ls)):
        numEl = len(ls[i])

        newRow = pd.DataFrame(np.array(ls[i]).reshape(1,numEl), columns = list(df.columns))

        df = df.append(newRow, ignore_index=True)

    return df

def reduce_df(payoff_df):
    # payoff_df['risk_reward_ratio'] =  payoff_df['risk_reward_ratio'].apply(lambda x:x*100)
    # payoff_df['max_profit'] =  payoff_df['max_profit'].apply(lambda x:x*100)

    max_rr = payoff_df[payoff_df['risk_reward_ratio'] == payoff_df['risk_reward_ratio'].max()]
    max_pft = payoff_df[payoff_df['max_profit'] == payoff_df['max_profit'].max()]
    #min_loss = payoff_df[payoff_df['min_loss'] == payoff_df['min_loss'].min()]

    frames = [max_rr,max_pft]
    temp_df = pd.concat(frames)
    # temp_df['risk_reward_ratio'] = temp_df['risk_reward_ratio'].apply(lambda x: int(x) / 100)
    # temp_df['max_profit'] = temp_df['max_profit'].apply(lambda x: int(x) / 100)
    return temp_df

def calculate_max_reward(payoff):
    '''
    :param payoff:
    :return:
    '''

    max_profit = np.nanmax(payoff)
    max_loss = abs(np.nanmin(payoff))
    min_loss = 0 #max([n for n in payoff if n < 0])

    maxindex = np.where(payoff == max_profit)[0][0]
    minindex = np.where(payoff == np.nanmin(payoff))[0][0]
    # print(sT[maxindex],sT[minindex])

    risk_reward_ratio = max_profit / max_loss
    return maxindex,max_profit,minindex,max_loss,min_loss,risk_reward_ratio

def validate_sum(sum):
    if sum < 0:

        print("add a long option")
    elif sum > 0 \
            :
        print("add a short option")

def get_nearest_strkprice(Spot_Price,Highlist,Lowlist):
    if abs(Highlist[-1]-Spot_Price) > abs(Lowlist[0]- Spot_Price) :
        S0 = Lowlist[0]
        Lowlist.pop(0)
    else:
        S0 = Highlist[-1]
        Highlist.pop(-1)
    return S0
#
# def call_payoff(sT, strike_price, premium):
#     return np.where(sT > strike_price, sT - strike_price, 0) - premium



def put_payoff(sT, strike_price, premium):
    return np.where(sT < strike_price, strike_price - sT, 0) - premium

def call_payoff(sT,strike_price,premium,shares=1,n=1,short=0):
    if short:
        n = n * -1
        return np.where(sT > strike_price,
                        ((sT - strike_price) - premium) * n * shares,
                        -premium * n * shares), n
    else:
        return np.where(sT > strike_price,
                        ((sT - strike_price) - premium) * n * shares,
                        -premium * n * shares), n

def put_payoff(sT,strike_price,premium,shares=1,n=1,short=0):
    if short:
        n = n * -1

    return (np.where(sT < strike_price, strike_price - sT, 0) - premium) * n,n


def call_atm_short_payoff(sT,strike_price,premium,shares=1,n=1):
    return np.where(sT > strike_price, ((strike_price - sT) + premium) * n * shares, premium * n * shares)


def get_diag(y, sT, title):
    pycharm = 0
    if pycharm:
        return 0
    else:
        from matplotlib import pyplot as plt
        # Create a plot using matplotlib
        fig, ax = plt.subplots()
        ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling
        ax.spines['top'].set_visible(False)  # Top border removed
        ax.spines['right'].set_visible(False)  # Right border removed
        ax.spines['bottom'].set_position('zero')  # Sets the X-axis in the center
        ax.tick_params(top=False, right=False)  # Removes the tick-marks on the RHS

        try:
            plt.plot(sT, y, lw=1.5)
            plt.title(title)
            plt.xlabel('Stock Prices')
            plt.ylabel('Profit/loss')

            plt.grid(True)
            plt.axis('tight')
            plt.show()
            return fig
        except Exception as e:
            print(e)


def get_comb(a):
    col = list(map(lambda x : 'K'+str(x),range(len(a))))
    return pd.DataFrame(list(itertools.product(*a)),columns=col)


def exec_strategy(comb,test,payoff_df):
    payoff_list=[]
    payoff_list.append(comb.apply(test,axis=1))
    # map(lambda x : addRow(x,payoff_df),payoff_list[0])
    payoff_df = addRow(payoff_list[0],payoff_df,multilple=True)
    payoff_df = reduce_df(payoff_df)
    return payoff_df


def Long_call_butterfly(sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df,short = False):

    S0 = get_nearest_strkprice(Spot_Price,Highlist,Lowlist)
    a = [Lowlist,[S0],Highlist]
    comb = get_comb(a)
    sT = np.arange(0, 2 * S0, 5)

    def test(x):
        k1 = x[0]
        k2 = x[1]
        k3 = x[2]
        c1 = df_dict[k1][1]
        c2 = df_dict[k2][1]
        c3 = df_dict[k3][1]
        sum = 0

        strgy = "long {0},2* short{1} , long {2}".format(k1,k2,k3)
        # Stock Price at expiration of the Call

        # Payoff from the Lower Strike ITM Long Call Option
        y1, cnt1 = call_payoff(sT,k1,c1,shares=shares,short=0)

        # Payoff from ATM Short Call Option
        y2, cnt2 = call_payoff(sT,k2,c2,shares=shares,short=1,n=2)

        # Payoff from the Higher Strike OTM Long Call Option
        y3, cnt3 = call_payoff(sT,k3,c3,shares=shares)

        sum = sum + cnt1 + cnt2 + cnt3
        validate_sum(sum)

        # Payoff for the Long Call Butterfly
        payoff = y1 + y2 + y3
        title ='Long_call_butterfly '+strgy
        diag = get_diag(payoff,sT,title)
        # print(type(diag))

        maxindex, max_profit, minindex, max_loss,min_loss, risk_reward_ratio = calculate_max_reward(payoff)

        aseries = ['Long_call_butterfly',Spot_Price, sT[maxindex], max_profit, sT[minindex],
                          max_loss,min_loss, risk_reward_ratio,strgy,str([payoff])]
        return aseries
    #
    # def apply_and_concat(dataframe, series, func, column_names):
    #     return pd.concat((
    #         dataframe,
    #         series.apply(
    #             lambda cell: pd.Series(func(cell), index=column_names))), axis=1)
    # print(apply_and_concat(payoff_df,comb,test,payoff_columns))

    return exec_strategy(comb,test,payoff_df)


def iron_condor(sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df):
    S0 = get_nearest_strkprice(Spot_Price, Highlist, Lowlist)
    # a = [Lowlist, [S0], Highlist]
    a = [Highlist, Lowlist, Lowlist, Highlist]
    comb = get_comb(a)
    sT = np.arange(0, 2 * S0, 5)

    def test(x):
        k1 = x[0]
        k2 = x[1]
        k3 = x[2]
        k4 = x[3]

        p1 = df_dict[k1][2]
        c2 = df_dict[k2][1]
        p3 = df_dict[k3][2]
        c4 = df_dict[k4][1]
        strgy = "Sell Put {0} ,Sell Call {1}, Buy  Put {2}, Buy Call {3}".\
            format(k1,k2,k3,k4)
        sum = 0
        y1, cnt1 = call_payoff(sT,k1,p1)
        y2, cnt2 = call_payoff(sT,k2,c2,short=1)
        y3, cnt3 = put_payoff(sT,k3,p3)
        y4, cnt4 =  put_payoff(sT,k4,c4,short=1)

        payoff = y1 + y2 + y3 + y4
        title = 'iron condor '+strgy
        diag = get_diag(payoff,sT,title)

        sum = sum + cnt1 + cnt2 + cnt3 + cnt4
        validate_sum(sum)

        maxindex, max_profit, minindex, max_loss, min_loss, risk_reward_ratio = calculate_max_reward(payoff)

        aseries = ['iron_condor', Spot_Price, sT[maxindex], max_profit, sT[minindex],
                   max_loss, min_loss, risk_reward_ratio, strgy, str([payoff])]
        return aseries

    return exec_strategy(comb,test,payoff_df)


def get_All():
    pass

def get_strategy_payoff(i,sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df):
    return(i(sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df))


def get_maxriskrwward(*args):


    Spot_Price, strikelist, Highlist, Lowlist, df_dict = get_Data()
    put_exp_range = 0.2

    sT = np.arange((1-put_exp_range)*Spot_Price,(1+put_exp_range)*Spot_Price,1)

    # def getPayoffALL(sT,strike_price,C_LTP,P_LTP):
    #
    #     maxindex, max_profit, minindex, max_loss,min_loss, risk_reward_ratio = calculate_max_reward(call_payoff (sT, strike_price, C_LTP))
    #     payoff_list.append(['payoff_long_call',Spot_Price,sT[maxindex], max_profit, sT[minindex], max_loss, risk_reward_ratio,strgy])
    #
    #     maxindex, max_profit, minindex, max_loss,min_loss, risk_reward_ratio = calculate_max_reward(call_payoff(sT, strike_price, C_LTP) * -1.0)
    #     payoff_list.append(['payoff_short_call',Spot_Price,sT[maxindex], max_profit, sT[minindex], max_loss, risk_reward_ratio,strgy ])
    #

        # payoff_long_put = put_payoff(sT, strike_price, P_LTP)
        # payoff_Short_put = put_payoff(sT, strike_price, P_LTP)*-1.0
        # stock_payoff = (sT - Spot_Price)*-1.0
        #
        # payoff_straddle = payoff_long_call + payoff_long_call
        #
        #
        # maxindex, max_profit, minindex, max_loss, risk_reward_ratio = calculate_max_reward(call_payoff(sT, strike_price, C_LTP) * -1.0)


    payoff_df = pd.DataFrame(columns=payoff_columns)
    if args:
        payoff_list=[]
        for i in args:
            payoff_list.append(eval(i)(sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df))
            print(payoff_list)
            payoff_df = reduce_df(pd.concat(payoff_list))
            print(payoff_df)

    else:
        print('no args')
        payoff_long_call_butterfly = Long_call_butterfly(sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df)
        payoff_iron_condor = iron_condor(sT,Spot_Price,strikelist, Highlist, Lowlist,df_dict,payoff_df)

        # payoff_df = reduce_df(pd.concat([payoff_df_a,payoff_df_b]))
        payoff_df = pd.concat([payoff_long_call_butterfly,payoff_iron_condor])
        print(payoff_df)

    # payoff_list =[]
    # for i in strikelist:
    #     #strike_price = float(i)
    #     C_LTP = df_dict[i][1]
    #     P_LTP = df_dict[i][2]
    #     getPayoffALL(sT,i,C_LTP,P_LTP)
    #     payoff_df=pd.DataFrame(payoff_list,columns=payoff_columns)
    # print(payoff_df.head(3))
    #     # print(max_profit,max_loss,risk_reward_ratio)
    #     # # Plot
    #     # # fig, ax = plt.subplots()
    #     # # ax.spines['top'].set_visible(False) # Top border removed
    #     # # ax.spines['right'].set_visible(False) # Right border removed
    #     # # ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
    #     # # ax.plot(sT,payoff_long_call,label='Long Call',color='r')
    #     # # plt.xlabel('Stock Price')
    #     # # plt.ylabel('Profit and loss')
    #     # # plt.legend()
    #     # # plt.show()


# get_maxriskrwward('Long_call_butterfly','iron_condor')
get_maxriskrwward()