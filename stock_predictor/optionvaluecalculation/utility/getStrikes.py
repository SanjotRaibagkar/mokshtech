def getStrikes(CloseValue,strikeList):
    """
    :param CloseValue: Strike Price under evaluation.
    :param strikeList: List of Sttike Prices
    :return: diff of two strike prices, value greater than given strike prie and value less than given strike price
    """
    CloseValue = float(CloseValue)
    diff = abs(int(float(strikeList[0])) - int(float(strikeList[1])))
    Strike_High = CloseValue + (diff - (CloseValue % diff))  # Get smallest no from larger no then Close
    Strike_Low = CloseValue + -(CloseValue % diff)  # Get largest no from smaller then Close
    return diff,Strike_High,Strike_Low



def get_Strikelist(strike_price_diff,Strike_High, Strike_Low,strike_price_start, strike_price_end,no_of_strikes):
    """
    :param strike_price_diff: diff of two consecutive strikes
    :param Strike_High: Strike greater than spot price
    :param Strike_Low: Strike lower than spot price
    :param strike_price_start: First strike price
    :param strike_price_end: Last known strike price
    :param no_of_strikes: total strikes above/below spot prices
    :return: list of strike prices around spot price
    """
    x, y = Strike_Low, Strike_High
    lowlist, highList = [], []
    i, j = 0, 0

    while(x <= strike_price_end and i < no_of_strikes):
        lowlist.append(x)
        x += strike_price_diff
        i+=1

    while (y >= strike_price_start and j < no_of_strikes):
        highList.append(y)
        y -= strike_price_diff
        j += 1
    highList = (sorted(highList,reverse=False))

    totalstrikes = highList.copy()
    totalstrikes.extend(lowlist)
    return totalstrikes, highList, lowlist


if __name__ == '__main__':
    print(getStrikes(11244.70,['9100.00', '9150.00', '9200.00', '9250.00', '9300.00', '9350.00', '9400.00', '9450.00', '9500.00', '9550.00', '9600.00', '9650.00', '9700.00', '9750.00', '9800.00', '9850.00', '9900.00', '9950.00', '10000.00', '10050.00', '10100.00', '10150.00', '10200.00', '10250.00', '10300.00', '10350.00', '10400.00', '10450.00', '10500.00', '10550.00', '10600.00', '10650.00', '10700.00', '10750.00', '10800.00', '10850.00', '10900.00', '10950.00', '11000.00', '11050.00', '11100.00', '11150.00', '11200.00', '11250.00', '11300.00', '11350.00', '11400.00', '11450.00', '11500.00', '11550.00', '11600.00', '11650.00', '11700.00', '11750.00', '11800.00', '11850.00', '11900.00', '11950.00', '12000.00', '12050.00', '12100.00', '12150.00', '12200.00', '12250.00', '12300.00', '12350.00', '12400.00', '12450.00', '12500.00', '12550.00', '12600.00', '12650.00', '12700.00', '12750.00', '12800.00', '12850.00']
))

    print(get_Strikelist(2, 4,6,0, 12,5))