import pandas as pd
import numpy as np

# =====================================
# LOAD BITCOIN PRICE DATA
# =====================================

price_df = pd.read_csv("Bitcoin_Historical_Data.csv")

price_df["Price"] = (
    price_df["Price"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(float)
)

price_df["Date"] = pd.to_datetime(price_df["Date"])
price_df = price_df.sort_values("Date").reset_index(drop=True)

# Daily returns
price_df["Return"] = price_df["Price"].pct_change()

# =====================================
# LOAD SIGNAL FILES
# =====================================

mean_df = pd.read_csv("signals_mean_reversion.csv")
ema_df = pd.read_csv("signals_EMA.csv")

mean_df["Date"] = pd.to_datetime(mean_df["Date"])
ema_df["Date"] = pd.to_datetime(ema_df["Date"])

# =====================================
# MERGE RETURNS
# =====================================

mean_df = mean_df.merge(
    price_df[["Date", "Return"]],
    on="Date",
    how="left"
)

ema_df = ema_df.merge(
    price_df[["Date", "Return"]],
    on="Date",
    how="left"
)

# =====================================
# BACKTEST FUNCTION
# =====================================

def evaluate_strategy(df, strategy_name):

    # Execute signal next day
    df["Position"] = df["Signal"].shift(1)

    # Strategy return
    df["StrategyReturn"] = (
        df["Position"] * df["Return"]
    )

    df["StrategyReturn"] = df["StrategyReturn"].fillna(0)

    # Equity curve
    df["Equity"] = (
        1 + df["StrategyReturn"]
    ).cumprod()

    # Metrics

    total_return = (
        df["Equity"].iloc[-1] - 1
    )

    annual_return = (
        df["Equity"].iloc[-1]
        ** (252 / len(df))
        - 1
    )

    sharpe = 0

    if df["StrategyReturn"].std() != 0:
        sharpe = (
            np.sqrt(252)
            * df["StrategyReturn"].mean()
            / df["StrategyReturn"].std()
        )

    # Drawdown

    running_max = df["Equity"].cummax()

    drawdown = (
        df["Equity"] - running_max
    ) / running_max

    max_drawdown = drawdown.min()

    # Trades

    trades = (
        df["Signal"] != 0
    ).sum()

    # Win rate

    winning_days = (
        df["StrategyReturn"] > 0
    ).sum()

    losing_days = (
        df["StrategyReturn"] < 0
    ).sum()

    total_days = winning_days + losing_days

    if total_days > 0:
        win_rate = winning_days / total_days
    else:
        win_rate = 0

    return {
        "Strategy": strategy_name,
        "Total Return (%)": round(total_return * 100, 2),
        "Annual Return (%)": round(annual_return * 100, 2),
        "Sharpe Ratio": round(sharpe, 3),
        "Max Drawdown (%)": round(max_drawdown * 100, 2),
        "Trades": int(trades),
        "Win Rate (%)": round(win_rate * 100, 2)
    }


# =====================================
# EVALUATE BOTH
# =====================================

mean_results = evaluate_strategy(
    mean_df.copy(),
    "Mean Reversion"
)

ema_results = evaluate_strategy(
    ema_df.copy(),
    "EMA Crossover"
)

results = pd.DataFrame(
    [mean_results, ema_results]
)

# =====================================
# DISPLAY RESULTS
# =====================================

print("\n")
print("=" * 80)
print("STRATEGY COMPARISON")
print("=" * 80)

print(results.to_string(index=False))

# =====================================
# DETERMINE WINNER
# =====================================

print("\n")
print("=" * 80)
print("WINNER")
print("=" * 80)

if mean_results["Sharpe Ratio"] > ema_results["Sharpe Ratio"]:
    print("Mean Reversion has the better risk-adjusted performance.")
elif mean_results["Sharpe Ratio"] < ema_results["Sharpe Ratio"]:
    print("EMA Crossover has the better risk-adjusted performance.")
else:
    print("Both strategies have identical Sharpe ratios.")

# =====================================
# SAVE RESULTS
# =====================================

results.to_csv(
    "strategy_comparison.csv",
    index=False
)

print("\nResults saved to strategy_comparison.csv")
