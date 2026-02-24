import src.utils as utils
import pandas as pd
import numpy as np





# test Wind farm database loading and aggregation
def test_WT_USagg():
    uswt_file='data/US_Wind_Turbine_Database.csv'
    uswt_db=pd.read_csv(uswt_file,
                        low_memory=False,
                        nrows=1000) #only load a subset for testing
    Df,location=utils.WT_USagg(uswt_db,'state','CA')
    assert uswt_db is not None
    assert Df is not None
    assert location is not None
    assert len(location[0])==4


def test_get_market():
    uswt_file='data/US_Wind_Turbine_Database.csv'
    eia_file='data/eia_generator_202506.xlsx'
    uswt_db=pd.read_csv(uswt_file,
                        low_memory=False,
                        nrows=1000) #only load a subset for testing
    uswt_db=uswt_db .drop(uswt_db[uswt_db['eia_id']<0].index)
    uswt_db=uswt_db .drop(uswt_db[uswt_db['t_cap']<0].index)
    uswt_db=utils.get_market(uswt_db,eia_file)

    assert 'Market' in uswt_db.columns
    assert uswt_db['Market'].isnull().sum()==0 #no null values in Market column