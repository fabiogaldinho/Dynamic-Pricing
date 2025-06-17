try:
    import pandas as pd
    import numpy as np
    from datetime import timedelta
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

def get_incc_data(purchase_date) -> pd.DataFrame:
    purchase_date = pd.to_datetime(purchase_date)

    url = "https://www.dadosdemercado.com.br/indices/incc-di"
    i = pd.read_html(url)
    incc_df = i[0].copy()
    incc_df = incc_df.rename(columns = {'Unnamed: 0': 'Year', 'Fev': 'Feb', 'Abr': 'Apr', 'Mai': 'May', 'Ago': 'Aug', 'Set': 'Sep', 'Out': 'Oct', 'Dez': 'Dec'})
    incc_df = incc_df.set_index('Year')
    
    incc_df = incc_df.reset_index().melt(id_vars = 'Year', 
                                         value_vars = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                         var_name = 'Month', 
                                         value_name = 'incc')
    
    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    incc_df['Month'] = incc_df['Month'].map(month_map)
    incc_df['date'] = pd.to_datetime(dict(year = incc_df['Year'], month = incc_df['Month'], day = 1))
    
    incc_df['date'] = pd.to_datetime(incc_df['date'])
    incc_df = incc_df.sort_values(by = 'date')
    
    incc_df = incc_df.drop(columns = {'Year', 'Month'})
    incc_df = incc_df[(incc_df['date'] >= '2024-01-01') & (incc_df['date'] < purchase_date)].reset_index(drop = True)
    
    incc_df['incc'] = incc_df['incc'].str.replace('%', '', regex = False).str.replace(',', '.', regex = False)
    incc_df['incc'] = incc_df['incc'].astype(float)
    incc_df['incc'] = incc_df['incc'] / 100
    
    i = pd.DataFrame([{
        'date': purchase_date + timedelta(days = 1),
        'incc': np.nan
    }])
    incc_df = pd.concat([incc_df, i], ignore_index = True)
    incc_df = incc_df.set_index('date')
    incc_df = incc_df.asfreq('D', method = 'ffill')
    incc_df = incc_df.rename_axis('date').reset_index()

    incc_df['incc_monthly_change'] = incc_df['incc'] - incc_df['incc'].shift(30)
    incc_df = incc_df.drop('incc', axis = 1)
    
    return incc_df