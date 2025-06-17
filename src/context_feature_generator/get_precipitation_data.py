try:
    import pandas as pd
    from datetime import datetime
    from meteostat import Point, Daily
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

def get_precipitation_data(purchase_date) -> pd.DataFrame:
    purchase_date = pd.to_datetime(purchase_date)

    city = Point(-22.31553, -49.070822)
    city.radius = 120000
    start_date = datetime(2024, 1, 1)
    end_date = purchase_date
    
    df = Daily(city, start_date, end_date)
    df = df.fetch()[['prcp']].fillna(0)
    df = df.rename_axis('date').reset_index()
    df = df.rename(columns = {'prcp': 'precipitation'})

    df['no_rain'] = (df['precipitation'] > 0.1).astype(int)

    return df