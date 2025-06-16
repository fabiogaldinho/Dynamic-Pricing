# **DYNAMIC PRICING**

In today’s highly volatile market environment, setting the right price at the right time is critical to maximizing profit margins. Traditional pricing strategies are no longer sufficient in the face of rapid changes in demand, supply chain disruptions, and fluctuating economic indicators.

Dynamic Pricing emerges as a powerful solution, leveraging data-driven models to adjust prices based on a combination of internal and external factors. Internally, this includes basic variables such as purchase cost and sales volume over time, as well as more complex metrics like price elasticity. Externally, macroeconomic variables such as inflation, weather patterns, and holidays have a significant impact on consumer behavior and product demand.

This project proposes a data-driven Dynamic Pricing system that leverages supervised Machine Learning techniques to model and predict optimal selling prices. The approach integrates:
- Basic internal features, such as historical sales volume per period and acquisition cost;
- Advanced internal variables, including price elasticity of demand;
- External drivers, such as inflation indices, weather conditions, and holidays — all of which have measurable effects on consumer behavior.

By incorporating both internal operational metrics and exogenous market signals, the model aims to generate pricing recommendations that adapt to market conditions in real time, maximizing revenue while maintaining competitiveness.
<br>
<br>

## **PROJECT OBJECTIVE**

The goal of this project is to develop a predictive pricing model capable of supporting dynamic pricing strategies in a retail environment. The model is designed to estimate optimal product prices by learning from both internal historical performance data and external contextual variables.

Design a profit-optimized pricing recommendation model that:
- Predicts expected product demand based on internal and external contextual variables;
- Simulates total profit and profit per unit across a realistic range of prices;
- Identifies the optimal price that maximizes revenue while preserving demand volume;
- Integrates easily with real purchase events from the ERP system.

This solution aims to serve as a robust foundation for real-time, automated pricing systems that respond dynamically to market conditions.
<br>
<br>

## **LANGUAGES AND TOOLS**

- **Programming Language**: Python;
- **Data Handling**: `pandas`, `numpy`;
- **Modeling**: `XGBoostRegressor`;
- **Visualization**: `matplotlib`;
- **Hyperparameter Tuning**: `Optuna`.
<br>

## **PROJECT WORKFLOW**

### 1. Data Collection and Consolidation
- Joined raw purchase, sales, and inventory data from the ERP system;
- Added external context from weather APIs, INCC scraping, and ANP diesel prices;
- Created a daily consolidated dataset from **2024-01-01 to 2025-04-30**.

### 2. Data Cleaning and Preprocessing
- Performed exploratory inspection of missing values across all sources;
- Treated outliers individually based on business context;
- Standardized column types, normalized date formats, and resolved inconsistencies across datasets;
- Prepared a unified daily DataFrame for feature engineering and modeling.

### 3. Feature Engineering
- Created lagged demand, rolling volatility, inventory turnover and price differential indicators;
- Engineered macroeconomic features;
- Binned numerical features into quantiles to capture nonlinear effects.

### 4. Modeling
- Trained an `XGBoostRegressor` model with Optuna hyperparameter tuning;
- Evaluated performance using MAE, RMSE, and WAPE;
- Final model (v2) achieved a **WAPE of 8.3% on the test set**.

### 5. Profit Simulation
- Given a purchase date, the model generates all context features automatically;
- A price range is simulated (e.g., R$25 to R$45), predicting demand and calculating:
  - **Total profit** = (price - cost) × predicted quantity;
  - **Profit per unit** = profit / predicted quantity;
- The optimal price is identified and plotted, with business constraints applied.
<br>

## **PROJECT STRUCTURE**

```bash
├── data/                 
├── models/
├── notebooks/    
├── visuals/       
├── README.md
└── requirements.txt
```
<br>

## **RESULTS**

- Model predicted demand with WAPE of 8.3%;
- Optimal price simulation returned R$41.55 as the most profitable, compared to R$39.90 practiced;
- Profit per unit improved from R$9.05 to R$11.60, with minimal impact on demand.
<br>

## **NEXT STEPS**

- Begin weekly collection of competitor prices (local and major players);
- Introduce constraints such as minimum margin and maximum price deviation;
- Simulate profit over 30-day fixed-price windows for negotiation planning;
- Perform A/B testing comparing baseline and model-driven prices;
- Monitor monthly drift and residual patterns to prevent overfitting.
<br>

## **AUTHOR**

**Fábio Galdino**