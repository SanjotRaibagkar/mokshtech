import datetime


def getURL(strSymbol,sym,expiry='-'):
    """
    :param strSymbol: index or STK
    :param sym: symbol code
    :param expiry: expiry date like "27SEP2018" OR "27Sep2018" OR "27-09-2018" OR "27-09-18" OR "2018-09-27"
    :return: URL
    """
    if expiry != '-':
        if len(str(expiry).split('-')[-1])==4:
            expiry = datetime.datetime.strptime(expiry,"%d-%m-%Y").strftime("%d%b%Y").upper()
        elif len(str(expiry).split('-')[0])==4:
            expiry = datetime.datetime.strptime(expiry, "%Y-%m-%d").strftime("%d%b%Y").upper()
        elif len(str(expiry).split('-')[-1])==2:
            expiry = datetime.datetime.strptime(expiry,"%d-%m-%y").strftime("%d%b%Y").upper()
        elif len(expiry) == 9:
            expiry=expiry.upper()

    if (strSymbol == "index"):
        if (sym == "select"):
            print("Please select underlying Indices")
            return False
        else:
            href = '/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?' \
                   'segmentLink=17&instrument=OPTIDX&symbol={0}&date={1}'.format(sym,expiry)

    if (strSymbol == "STK"):
        if (sym == "select"):
            print("Please select underlying symbol")
            return False
        else:
            href = '/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?' \
                   'segmentLink=17&instrument=OPTSTK&symbol={0}&date={1}'.format(sym,expiry)
    baseNSE = 'https://www.nseindia.com'
    return baseNSE+href


if __name__ == '__main__':
    print(getURL('index','NIFTY','27SEP2018'))