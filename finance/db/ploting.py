import pandas as pd
from sqlalchemy import create_engine
from config import host, user, password, database
import mplfinance as mpf


# Create SQLAlchemy engine
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# Your SQL query
query = "SELECT * FROM cryptocurrency_data WHERE ticker = 'USDTARS' ORDER BY date ASC ;"

# Fetch data and convert to DataFrame
with engine.connect() as connection:
    df = pd.read_sql(query, connection)
    
# Inspect the DataFrame
df['date'] = pd.to_datetime(df['date'])

# Set the 'date' column as the index of the DataFrame
df.set_index('date', inplace=True)


print(df.head())
print(df.dtypes)

mpf.plot(df, type='candle', style='charles', volume=True, title='USDT/ARS')

    
    