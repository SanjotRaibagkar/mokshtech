import pandas as pd
import matplotlib.pyplot as plt
import os
import property as p

path=p.repobasepath

def mac_reporting(repostr=(),report='ma_cross'):
    reportname=report+'.csv'
    reportname=os.path.join(path,reportname)
    # Check if file exist.
    # If not then create a file and write header
    if os.path.exists(reportname):
        f = open(reportname, mode='a')

    else:
        header = 'Symbol,EndTotal,MA_Long,MA_Short,Total_Transactions'
        f = open(reportname, mode='a')
        f.writelines(header)
        f.write('\n')

    # Write data to csv
    f.writelines(str(repostr)[1:-1])
    f.write('\n')
    f.close()
    return reportname


def max_return_value(reportname):
    df=pd.read_csv(reportname)
    mod_df = df.loc[df.groupby(['Symbol'])['EndTotal'].idxmax()]
    print(mod_df)
    mod_reort=reportname[:-4]+'_max_gain.csv'
    mod_df.to_csv(mod_reort)


def mac_visualise(bars,signals,returns,imgname):
    imgpath = os.path.join(path,'backtestimg',imgname)

    fig = plt.figure()
    fig.patch.set_facecolor('white')  # Set the outer colour to white
    ax1 = fig.add_subplot(211, ylabel='Price in $')

    # Plot the AAPL closing price overlaid with the moving averages
    bars['Close'].plot(ax=ax1, color='g', lw=2.)
    signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

    # Plot the "buy" trades against AAPL
    ax1.plot(signals.ix[signals.positions == 1.0].index,
             signals.short_mavg[signals.positions == 1.0],
             '^', markersize=10, color='m')

    # Plot the "sell" trades against AAPL
    ax1.plot(signals.ix[signals.positions == -1.0].index,
             signals.short_mavg[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Plot the equity curve in dollars
    ax2 = fig.add_subplot(212, ylabel='Portfolio value in $')
    returns['total'].plot(ax=ax2, lw=2.)

    # Plot the "buy" and "sell" trades against the equity curve
    ax2.plot(returns.ix[signals.positions == 1.0].index,
             returns.total[signals.positions == 1.0],
             '^', markersize=10, color='m')
    ax2.plot(returns.ix[signals.positions == -1.0].index,
             returns.total[signals.positions == -1.0],
             'v', markersize=10, color='k')

    # Plot the figure
    fig.savefig(imgpath)
