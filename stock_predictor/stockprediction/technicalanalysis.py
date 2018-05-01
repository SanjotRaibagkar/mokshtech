from property import *
import talib
import itertools
from utility import Load_Csv as lcsv



class ta(lcsv.Load_csv):
    # coding: utf-8

    '''this class contains functions fto predict label with the help of technical indicators'''
    
    def __init__(self,symbol='NIFTY'):
        file=symbol+'.csv'
        self.filename=os.path.join(stockdata,symbol+'.csv')


    

    def loadcsv(self):
        '''load 'Date','Close', 'Volume' data from databse and return dataframe
        '''
        
        self.dataset=self.LoadData(self.filename).loc[:, ['Close','Open','Date','Volume']]
        self.dataset['Date'] = pd.to_datetime(self.dataset['Date'])
        self.dataset = self.dataset.fillna(self.dataset.mean())

        return self.dataset
    

    def loadfeaturesdata(self,x):
        '''load features detailed data from databse'''
        self.featuresdata=self.LoadfeaData(featuresdata)
        self.featuresdata.index=self.featuresdata[0]
        #self.featuresdata=self.featuresdata.loc[x]
        return list(self.featuresdata.loc[x,1:])
    
    
    def ti_Combinations(self):
        '''takes input as list of list and  gives output as comninations '''
        
        #print("ti_Combinations")

        self.paneldict={}
        def comb_r(row):
            
            #print(self.dataset)
            #print('row',row)
            comb_dataset=self.dataset.copy()#deep=True)  #Copy basic dataset to comb_dataset
            for i in row:
                #print('i',i)
                comb_dataset['MA'+str(i)]=self.tdf['MA'+str(i)] # add MA rows from tdf to comb_dataset as per the combination .
                #print('comb_dataset',comb_dataset)
            #print('c',comb_dataset)    #To print dataset with all combinations of MA
            
            #print('self.paneldict',self.paneldict)
            row_s=str(row)
            self.paneldict[row_s]=comb_dataset.copy()#deep=True)  # Now xfer dataframe from comb_dataset to panel_dict 
            #print('self.paneldict2',self.paneldict)


        try:
            a=self.tidict['MA']
            #print('combinations_input',a)
            #[[10],[50],[60-64]]
            comb_df=pd.Series(list(itertools.product(*a)))##get combinatons 
            #print('comb_df',comb_df)
            comb_df.apply(comb_r)
            #panel_dataset=pd.Panel(self.paneldict)
            #print('panel_dataset',panel_dataset)
         
            '''
            ### Error: Panel is not working here . 
            On printing panel it is printing merge of all unique columns for each dataframe.
            
            
            #print(item for item in panel_dataset.items])  # to print item name of panel
            #print('(2, 4, 60)',panel_dataset[(2, 4, 60)])
            
            '''
            
            
        except Exception as e:
            print('e2',e)         
       
        
    def loadfeatures(self):
        '''load feature label data from databse
        '''
        self.featurestilist=[]
        self.misc=[]
        self.label=[]
        self.tilist=dir(talib)
        self.featuredict={}
        self.tidict={}
        self.features=self.LoadfeaData(featurescsv)

         
        def func(value,args):
           

            if str(value).find("-")>-1:   #tocheck if range is given 
                a,b=value.split("-")
                a=int(a)
                b=int(b)

                self.featuredict[args].extend(list(range(a,b)))   #if range is given then replace it by list
                self.tidict[args].append(list(range(a,b))) 
               
            else:
                try:
                    var=str(args)+'-'+str(int(value))              #togenerate name like MA-1,MA-2  

                    self.featuredict[args].extend(self.loadfeaturesdata(var))
                    
                    self.tidict[args].append(self.loadfeaturesdata(var))
                except Exception as e:
                    pass  
        
        
        def funr(row):
            r_len=len(row)
            ti=row[0]
            rowdf=pd.Series(row[1:])
            
                     
            if ti in self.tilist:
                self.featuredict[ti]=[]
                self.tidict[ti]=[]
                self.featurestilist.append(ti)
                
                rowdf.apply(func,args=(ti,))    #Vectorize function over each element
                
            elif ti=='label':
                self.label.append(row[1])
            elif ti == 'predict_days':
                self.predict_days = row[1:].tolist()
            else:
                self.misc.append(row)
    
                
                                                 #vectorize approach to speed up process        
        self.features.apply(funr, axis=1)
        #print(self.featuredict)                  #To be removed after development
        #print(self.features)
        #print("end")
        
        
        
        #return(self.featurestilist,self.label,self.misc,self.MA_comb)
        
        
        
    def get_MA(self,x):
        malist=self.featuredict['MA']
        for i in malist:
            if ('MA'+str(i)) in self.tdf:
                continue
            else: 
                try:
                    self.tdf['MA'+str(i)]=talib.SMA(self.dataset[x],i)
                except Exception as e:
                    pass
        return(self.tdf)
        
    def get_RSI(self,x):
        rsilist=self.featuredict['RSI']
        for i in rsilist:
            if ('RSI'+str(i)) in self.tdf:
                continue
            else:
                try:
                    self.dataset['RSI'+str(i)]=talib.RSI(self.dataset[x],i)
                except Exception as e:
                    pass

    
    def get_BBANDS(self,x):
        tperiod=int(self.featuredict['BBANDS'][0])
        upper , middle , lower = talib.BBANDS(self.dataset[x],timeperiod=tperiod,nbdevup=2,nbdevdn=2)
        self.dataset['BBu-'+str(tperiod)]=upper
        self.dataset['BBl']=lower
        self.dataset['BBs']=upper-lower

    def get_technical_indi(self):
        
        self.tdf=self.LoadData(self.filename).loc[:, ['Close']]
        for i in self.featurestilist:
            if i=='MA':
                self.get_MA('Close')
            if i=='RSI':
                self.get_RSI('Close')
            if i == 'BBANDS':
                self.get_BBANDS('Close')
                
                
    def get_return(self):
        self.dataset['DailyReturn'] = self.dataset['Close'].pct_change()
        
        
    def get_label(self):
        print("start technical analysis and  Calculate technical indicators")
        if self.label[0]=='return':
            self.get_return()
        #print(self.dataset)
        #print(self.tdf)
        #print(self.tidict)
       
    def get_panel_data(self):
        self.loadcsv()
        self.loadfeatures()
        self.get_technical_indi()
        self.get_label()
        self.ti_Combinations()
        return self.paneldict

        
