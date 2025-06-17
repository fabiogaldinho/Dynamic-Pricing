try:
    import pandas as pd
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

import urllib.request

def get_fuel_data() -> pd.DataFrame:
    url = "https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/precos-revenda-e-de-distribuicao-combustiveis/shlp/semanal/semanal-estados-desde-2013.xlsx"
    local_backup = "data/raw/fuel_data.xlsx"

    try:
        response = urllib.request.urlopen(url, timeout = 10)
        file = response.read()
        fuel_df = pd.read_excel(file)
    except Exception as e:
        print(f"\nWarning: Could not fetch data from URL. Reason: {e}")
        print("Loading backup from local file.")
        fuel_df = pd.read_excel(local_backup)
    
    i = fuel_df[fuel_df.iloc[:, 0].astype(str).str.contains("DATA INICIAL", case = False, na = False)].index[0]
    fuel_df = fuel_df[i:len(fuel_df)].copy()
    fuel_df.columns = fuel_df.iloc[0]
    fuel_df = fuel_df.drop(fuel_df.index[0]).reset_index(drop = True)
    
    fuel_df = fuel_df[(fuel_df['ESTADO'] == 'SAO PAULO') & (fuel_df['PRODUTO'] == 'OLEO DIESEL S10')][['DATA INICIAL', 'PREÇO MÉDIO REVENDA']].copy().reset_index(drop = True)\
                        .rename(columns = {'DATA INICIAL': 'date', 'PREÇO MÉDIO REVENDA': 'fuel_price'})
    
    fuel_df['date'] = pd.to_datetime(fuel_df['date'])
    fuel_df['fuel_price'] = fuel_df['fuel_price'].astype(float)
    
    fuel_df = fuel_df.set_index('date')
    fuel_df = fuel_df.asfreq('D', method = 'ffill')
    fuel_df = fuel_df.rename_axis('date').reset_index()

    fuel_df['fuel_price_lag_60'] = fuel_df['fuel_price'].shift(60)
    
    return fuel_df