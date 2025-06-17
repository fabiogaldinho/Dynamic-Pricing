try:
    import pandas as pd
    import holidays
    from datetime import datetime, timedelta  
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

def get_holiday_data(purchase_date) -> pd.DataFrame:
    purchase_date = pd.to_datetime(purchase_date)
    df = pd.date_range(start = '2024-01-01', end = (purchase_date + timedelta(days = 180)), freq = 'D')
    df = pd.DataFrame({'date': df})

    df['is_holiday'] = df['date'].apply(lambda x: 1 if x in holidays.Brazil(state = 'SP') else 0)
    df.loc[df['date'] == '2024-08-01', 'is_holiday'] = 1
    
    k = 1
    df.loc[0, 'days_until_holiday'] = 0
    
    for i in range(1, len(df)):
        if (df.loc[i, 'is_holiday'] == 1):
            h = df.loc[i, 'date']
    
            for j in range(k, i):
                df.loc[j, 'days_until_holiday'] = abs((h - df.loc[j, 'date']).days)
    
            k = i + 1
    
    df['days_until_holiday'] = df['days_until_holiday'].fillna(0).astype(int)
    df = df.drop('is_holiday', axis = 1)
    
    
    # Creating 'is_weekend' and 'month' features
    df['month'] = df['date'].dt.month
    df['is_weekend'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['is_weekend'].apply(lambda x: True if x > 4 else False)
    
    
    # Filtering dataframe
    return df[df['date'] <= purchase_date]