try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

def get_sell_data() -> pd.DataFrame:
    sell_df = pd.read_csv("data/sql_exports/sell_records.csv")
    sell_df['sell_date'] = pd.to_datetime(sell_df['sell_date']).dt.normalize()
    sell_df = sell_df.rename(columns = {'sell_date': 'date'})
    sell_df = sell_df.groupby('date').agg({'sell_quantity': 'sum', 'sell_value': 'mean'}).reset_index()
    sell_df['sell_value'] = np.round(sell_df['sell_value'], 2)
    
    sell_df = sell_df[sell_df['sell_value'] > 25]
    sell_df = sell_df[sell_df['sell_quantity'] < 1000]
    
    sell_df['sell_quantity_lag_7'] = sell_df['sell_quantity'].shift(7)
    sell_df['rolling_std_sell_value'] = sell_df['sell_value'].rolling(window = 3).std()
    sell_df['lag_7_bin'] = pd.qcut(sell_df['sell_quantity_lag_7'], q = 4, labels = [0, 1, 2, 3]).fillna(0).astype(int)

    return sell_df