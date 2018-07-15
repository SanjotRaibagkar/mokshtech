def filtered_frame(dataframe,skipdays=0,Options=False):
    '''
    :param dataframe:
    :param skipdays:
    :return: dataframe
    1. DropDuplicates
    2. Drop row with all columns as NA
    3. set index as Date column
    4. truncate skipdays (truncate starting x days)
    '''
    dataframe = dataframe.drop_duplicates()  # Drop duplicate row
    dataframe = dataframe.dropna(how='all')  # Drop row with all columns as NA
    if Options:
        dataframe = dataframe.set_index('Date',append=True,drop=False)
    else:
        dataframe = dataframe.fillna(dataframe.mean())
        dataframe = dataframe.set_index('Date')
    dataframe = dataframe.iloc[skipdays:, :]
    return dataframe