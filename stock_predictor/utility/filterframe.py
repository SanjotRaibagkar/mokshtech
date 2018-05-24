import pandas as pd


def filtered_frame(dataframe,skipdays=0):
    dataframe = dataframe.drop_duplicates()  # Drop duplicate row
    dataframe = dataframe.dropna(how='all')  # Drop row with all columns as NA
    dataframe = dataframe.fillna(dataframe.mean())
    dataframe = dataframe.set_index('Date')
    dataframe = dataframe.iloc[skipdays:, :]
    return dataframe