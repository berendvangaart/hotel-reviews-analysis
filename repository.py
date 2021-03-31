from sqlalchemy import create_engine
import config
import pandas as pd

engine = create_engine(config.database_uri)

def save_dataframe(dataframe, table="reviews"):
    dataframe.to_sql(name=table, con=engine, if_exists='fail', index=False, chunksize=1000)

def read_dataframe(tablename):
    return pd.read_sql("SELECT * FROM " + tablename, con=engine)







