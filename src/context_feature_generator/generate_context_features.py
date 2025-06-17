try:
    import pandas as pd
    from tqdm import tqdm
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

from .get_holiday_data import get_holiday_data
from .get_precipitation_data import get_precipitation_data
from .get_incc_data import get_incc_data
from .get_fuel_data import get_fuel_data
from .get_sell_data import get_sell_data
from .get_buy_data import get_buy_data
from .get_inventory_data import get_inventory_data

def generate_context_features(purchase_date) -> pd.DataFrame:
    purchase_date = pd.to_datetime(purchase_date)
    features = ["sell_value",
                "sell_quantity_lag_7",
                "rolling_std_sell_value",
                "daily_balance",
                "inventory_turnover",
                "buy_quantity",
                "inventory_lag_1",
                "precipitation",
                "incc_monthly_change",
                "fuel_price_lag_60",
                "is_weekend",
                "days_until_holiday",
                "month",
                "no_rain",
                "turnover_bin",
                "lag_7_bin"
]
    progress = tqdm(total = 7, desc = "Generating context features", unit = "step")

    # Creating base dataframe, getting holidays and creating 'days_until_holiday', 'month', 'is_weekend' features
    progress.set_description("Fetching holiday data")
    df = get_holiday_data(purchase_date)
    progress.update(1)
    
    # Fetching precipitation data
    progress.set_description("Fetching weather data")
    weather_df = get_precipitation_data(purchase_date)
    progress.update(1)
    
    # Fetching INCC data and creating 'incc_monthly_change' feature
    progress.set_description("Fetching INCC data")
    incc_df = get_incc_data(purchase_date)
    progress.update(1)
    
    # Fetching fuel price data and creating 'fuel_price_lag_60' feature 
    progress.set_description("Fetching fuel data")
    fuel_df = get_fuel_data()
    progress.update(1)
    
    # Fetching sell records data from exported SQL Database and creating 'sell_quantity_lag_7', 'rolling_std_sell_value', and 'lag_7_bin' features
    progress.set_description("Loading sell data")
    sell_df = get_sell_data()
    progress.update(1)
    
    # Fetching buy records data from exported SQL Database
    progress.set_description("Loading buy data")
    buy_df = get_buy_data()
    progress.update(1)
    
    # Fetching inventory records data from exported SQL Database and creating 'inventory_lag_1', 'inventory_turnover', and 'turnover_bin' features
    progress.set_description("Loading inventory position data")
    inventory_df = get_inventory_data(purchase_date, sell_df, buy_df)
    progress.update(1)
    progress.close()

    # Merging
    df = df.merge(weather_df, on = 'date', how = 'left') \
            .merge(incc_df, on = 'date', how = 'left') \
            .merge(fuel_df, on = 'date', how = 'left') \
            .merge(sell_df, on = 'date', how = 'left') \
            .merge(buy_df, on = 'date', how = 'left') \
            .merge(inventory_df, on = 'date', how = 'left')


    # Filtering context vector
    df = df[df['date'] == purchase_date][features].reset_index(drop = True).copy()

    df['daily_balance'] = df['daily_balance'].astype(int)
    df['days_until_holiday'] = df['days_until_holiday'].astype(float)
    
    
    return df