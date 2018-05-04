from property import *



def create_reportfile(path, header):
    f = open(path, "w+")
    f.write(reportcol)
    f.write('\n')
    f.close


def create_basic_report(report_dict,header):
    rep_header = str(header).split("_")

    ##Sample header  NIFTY_60_RSI10_BBu-10_BBl_BBs_DailyReturn_MA20_MA50_MA252

    report_dict[header] = pd.DataFrame(
        columns=['symbol', 'Days', 'RSI', 'BBANDS', 'MA1', 'MA2', 'MA3', 'MA4', 'MSE', 'RMSE', 'Actual', 'Forcasted'])
    try:
        report_dict[header].set_value(header, 'symbol', rep_header[0])
        report_dict[header].set_value(header, 'Days', rep_header[1])
        report_dict[header].set_value(header, 'RSI', rep_header[2][3:])
        report_dict[header].set_value(header, 'BBANDS', rep_header[3][4:])
        report_dict[header].set_value(header, 'MA1', rep_header[6][2:])
        report_dict[header].set_value(header, 'MA2', rep_header[7][2:])
        report_dict[header].set_value(header, 'MA3', rep_header[8][2:])
        if len(rep_header) > 10:
            report_dict[header].set_value(header, 'MA4', rep_header[9][2:])
        else:
            report_dict[header].set_value(header, 'MA4', '-')
    except Exception as e:
        print('basicreporting error',e)
    finally:

        return(report_dict)


def create_report(report_dict,header,x,y):
    try:
        report_dict[header].set_value(header, str(x),y)
    except Exception as e:
        print('reporting error', e)
    finally:
        return(report_dict)

def mod_report(old=reportpath,new=mod_reportpath):
    df = pd.read_csv(old)
    mod_df=df.loc[df.groupby(['symbol', 'Days'])['RMSE'].idxmin()]
    mod_df.to_csv(new,index=False)
    return(mod_df)


