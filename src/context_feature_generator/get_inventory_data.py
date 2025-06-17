try:
    import pandas as pd
    from datetime import timedelta
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

def get_inventory_data(purchase_date, sell_df, buy_df) -> pd.DataFrame:
    purchase_date = pd.to_datetime(purchase_date)

    inventory_df = pd.read_csv("data/sql_exports/inventory_records.csv")
    inventory_df['date_inventory'] = pd.to_datetime(inventory_df['date_inventory']).dt.normalize()
    inventory_df = inventory_df.rename(columns = {'inventory': 'stock_count'})
    
    inventory_df.loc[0, 'date_inventory'] = '2024-01-01'
    i = pd.DataFrame([[purchase_date + timedelta(days = 1), 0]], columns = ['date_inventory', 'stock_count'])
    inventory_df = pd.concat([inventory_df, i], ignore_index = True)
    
    inventory_df['date_inventory'] = pd.to_datetime(inventory_df['date_inventory'])
    inventory_df = inventory_df.set_index('date_inventory')
    inventory_df = inventory_df.asfreq('D', fill_value = 0)
    
    inventory_df = inventory_df.rename_axis('date').reset_index()
    
    initial_inv = inventory_df.loc[0, 'stock_count']
    
    inventory_df = inventory_df.merge(sell_df[['date', 'sell_quantity']], on = 'date', how = 'left').fillna(0)
    inventory_df = inventory_df.merge(buy_df[['date', 'buy_quantity']], on = 'date', how = 'left').fillna(0)
    
    inventory_df['daily_balance'] = inventory_df['buy_quantity'] - inventory_df['sell_quantity']
    inventory_df.loc[0, 'inventory'] = initial_inv
    
    for i in range(1, len(inventory_df)):
        if (inventory_df.loc[i, 'stock_count'] == 0):
            inventory_df.loc[i, 'inventory'] = inventory_df.loc[i-1, 'inventory'] + inventory_df.loc[i, 'daily_balance']
        else:
            inventory_df.loc[i, 'inv_correction'] = inventory_df.loc[i-1, 'inventory'] + inventory_df.loc[i, 'daily_balance'] - inventory_df.loc[i, 'stock_count']
            inventory_df.loc[i, 'inventory'] = inventory_df.loc[i, 'stock_count']
        
    inventory_df['inv_correction'] = inventory_df['inv_correction'].fillna(0)

    inventory_df['inventory_lag_1'] = inventory_df['inventory'].shift(1)
    inventory_df['inventory_turnover'] = inventory_df['sell_quantity'] / (inventory_df['inventory_lag_1'] + 1e-6)
    inventory_df['turnover_bin'] = pd.qcut(inventory_df['inventory_turnover'], q = 4, labels = [0, 1, 2 ,3]).fillna(0).astype(int)

    inventory_df = inventory_df.drop(columns = {'stock_count', 'sell_quantity', 'buy_quantity', 'inv_correction'}, axis = 1)
    
    return inventory_df