
# coding: utf-8

# In[1]:


import os,sys
import pandas as pd
import numpy as np


# In[2]:


'''to be modified and shift into property files'''

currentpath=os.getcwd()
dbpath=os.path.join(currentpath,'..','database')
stockcsv=os.path.join(dbpath,'stockpath.csv')


# In[3]:


class Load_csv(object):
    '''This will load data from csv and will return the values.
    It will skip any outliers in between.
    To handle this need select statement from database.'''
    def LoadData(self,filename):

        data=pd.read_csv(filename, error_bad_lines=False)
        return data
    
    
    def LoadfeaData(self,filename):
        data=pd.read_csv(filename, error_bad_lines=False,header=None)
        return data
    
        
        

