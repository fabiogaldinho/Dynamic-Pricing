try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

def get_buy_data() -> pd.DataFrame:
    buy_df = pd.read_csv("data/sql_exports/buy_records.csv")
    buy_df['buy_date'] = pd.to_datetime(buy_df['buy_date']).dt.normalize()
    buy_df = buy_df.rename(columns = {'buy_date': 'date'})
    buy_df = buy_df.groupby('date').agg({'buy_quantity': 'sum', 'buy_value': 'mean'}).reset_index()
    buy_df['buy_value'] = np.round(buy_df['buy_value'], 2)

    return buy_df