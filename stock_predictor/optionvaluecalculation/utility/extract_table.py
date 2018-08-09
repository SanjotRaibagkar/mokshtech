import requests
import pandas as pd
import time

from optionvaluecalculation.utility import getURL
from optionvaluecalculation.utility import getStrikes
from bs4 import BeautifulSoup
from optionvaluecalculation.utility.getStrikes import get_Strikelist

def extract_table(strSymbol,sym,expiry='-'):
    # print('0',time.time())

    Base_url = getURL.getURL(strSymbol,sym)

    page = requests.get(Base_url)
    #print(page.status_code,page.content)

    soup = BeautifulSoup(page.content,'html.parser')
    # print('1',time.time())


    spot_price = float(soup.find("span").text.split(" ")[-1].strip())

    table_it = soup.find_all(class_ = 'opttbldata')
    table_cls_1 = soup.find_all(id = 'octable')

    col_list = []
    for mytable in table_cls_1:
        table_head = mytable.find('thead')
        try:
            rows = table_head.find_all('tr')
            for tr in rows:
                cols =tr.find_all('th')
                for th in cols:
                    er = th.text
                    col_list.append(er)
        except:
            print("no thead")


    col_list_fnl = [e for e in col_list if e not in ('CALLS','PUTS','Chart','\\xc2\\xa0','\xa0')]

    table_cls_2 = soup.find(id = 'octable')
    all_trs = table_cls_2.find_all('tr')
    req_row = table_cls_2.find_all('tr')

    new_table = pd.DataFrame(index=range(0,len(req_row)-3),columns=col_list_fnl)
    row_marker = 0
    # print('2',time.time())
    for row_number, tr_nos in enumerate(req_row):
        # This ensures we use only rows with values:
        if row_number <=1 or row_number == len(req_row)-1:
            continue
        td_columns = tr_nos.find_all('td')

        #This removes graph columns
        select_cols= td_columns[1:22]
        cols_horizontal = range(0,len(select_cols))

        for nu, column in enumerate(select_cols):
            tr = column.get_text()
            tr = tr.strip('\n\r\t": ')
            tr =tr.replace(',', '')
            new_table.ix[row_marker,[nu]] = tr

        row_marker +=1

    # print('3',time.time())

    strike_list = list(new_table['Strike Price'])
    strike_price_start = float(strike_list[0])
    strike_price_end = float(strike_list[-1])
    strike_price_len = len(strike_list)
    new_table =new_table.loc[:,['Strike Price','LTP']]#.set_index('Strike Price',drop=True)
    new_table.columns = ['Strike_Price','C_LTP','P_LTP']

    # print('4',time.time())
    strike_price_diff,Strike_High,Strike_Low = getStrikes.getStrikes(spot_price,strike_list)
    strikelist,Highlist,Lowlist = (getStrikes.get_Strikelist(strike_price_diff, Strike_High, Strike_Low,strike_price_start, strike_price_end,5))
    #new_table = new_table[new_table.index.isin(strikelist)]
    new_table.index.astype('float')
    # print(new_table.index.astype)
    # new_table = new_table.to_dict(orient='records')
    # print(new_table[2200.00])
    fname=sym+'.csv'
    new_table.to_csv(fname)
    return new_table,spot_price,strike_price_diff,strikelist,Highlist,Lowlist

if __name__ == '__main__':
    a = extract_table('index','NIFTY')
    # b = extract_table('STK','TCS')
    # print(a,b)