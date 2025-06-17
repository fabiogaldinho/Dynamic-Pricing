import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import pandas as pd
    import joblib
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Error: Required library is not installed.")
    print("Please run: pip install -r requirements.txt")
    exit()

from tqdm import tqdm
from context_feature_generator.generate_context_features import generate_context_features
from context_feature_generator.get_buy_data import get_buy_data

def simulate_profit(sell_price, context_features, model, buy_price):
    input_features = context_features.copy()
    input_features['sell_value'] = sell_price

    predicted_quantity = np.expm1(model.predict(input_features.values)[0]).astype(int)
    profit = (sell_price - buy_price) * predicted_quantity
    
    return profit, predicted_quantity


def plot_optimal(prices, profits, demands, optimal_price, buy_price, profit_per_unit, progress):
    corViridis = ['#440154', '#414487', '#2a788e', '#22a884', '#7ad151']
    colorss = ['#b2c3d4', '#414487', '#B01756']

    fig, ax = plt.subplots(figsize = (12, 5.5))
    fig.patch.set_facecolor("0.85")

    # Profit
    ax.grid(visible = True, color = '0.81')
    ax.set_xlabel('Sell Price (BRL)')
    ax.set_ylabel('Profit (BRL)', color = '#197d60')
    ax.plot(prices, profits, color = corViridis[3])
    ax.tick_params(axis = 'y', labelcolor = '#197d60')
    ax.set_facecolor("0.85")
    ax.spines.top.set_visible(False)
    ax.set_ylim(0,max(profits)+100)


    # Optimal Price
    ax.axvline(x = optimal_price, color = colorss[2], linestyle = '--', linewidth = 1)
    ax.text(
        optimal_price + 0.1,
        ax.get_ylim()[1] * 0.98,
        f"Buy Price: R$ {buy_price:.2f}"\
        f"\nOptimal Sell Price: R$ {optimal_price:.2f}"\
        f"\n\n" + r"$\bf{Expected\ Profit\ Per\ Unit:\ R\$" + f"{profit_per_unit:.2f}" + r"}$",
        color = colorss[2],
        fontsize = 9,
        va = 'top'
    )


    # Demand
    ax2 = ax.twinx()
    ax2.set_ylabel('\nPredicted Demand (Units)', color = corViridis[0])
    ax2.plot(prices, demands, color = corViridis[0])
    ax2.tick_params(axis = 'y', labelcolor = corViridis[0])
    ax2.set_facecolor("0.85")
    ax2.spines.top.set_visible(False)


    fig.suptitle('Profit and Demand Simulation vs. Sell Price\n')
    fig.tight_layout()
    progress.update(1)
    progress.close()
    plt.show()


if __name__ == "__main__":
    print("Available purchase dates with recorded product purchases:\n")
    
    df = get_buy_data()
    df = df[((df['date'] >= '2025-04-01') & (df['date'] < '2025-06-01')) & (df['buy_quantity'] > 0)].reset_index(drop = True).copy()
    df['date'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m-%d")

    for i in range(len(df)):
        print(f"{i+1}. {df.loc[i, 'date']} - {df.loc[i, 'buy_quantity'].astype(int)} units - R${df.loc[i, 'buy_value']}")
    
    choice = int(input("\nSelect the purchase date number: ")) - 1
    purchase_date = df.loc[choice, 'date']
    buy_price = df.loc[choice, 'buy_value']
    
    suggested_price = float(input("\nEnter the suggested selling price (e.g., 39.90): "))

    print(f"\nGenerating context features for {purchase_date}...")
    context = generate_context_features(purchase_date)

    print("\nRunning profit optimization function...")
    progress = tqdm(total = 3, desc = "Running profit optimization function", unit = "step")
    progress.set_description("Loading ML Model")
    model = joblib.load("models/model_v2.pkl")
    progress.update(1)


    progress.set_description("Running predictions")
    price_range = np.arange(suggested_price - 15, suggested_price + 5, 0.05)

    profits = []
    demands = []
    prices = []

    for price in price_range:
        p, d = simulate_profit(price, context, model, buy_price)
        if (p > 0):
            profits.append(p)
            demands.append(d)
            prices.append(price)
    progress.update(1)


    progress.set_description("Plotting profit curve")
    optimal_price = prices[np.argmax(profits)]
    optimal_profit = max(profits)
    optimal_demand = demands[np.argmax(profits)]
    profit_per_unit = optimal_profit / optimal_demand

    plot_optimal(prices, profits, demands, optimal_price, buy_price, profit_per_unit, progress)


