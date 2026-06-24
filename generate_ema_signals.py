import pandas as pd
import numpy as np

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("Bitcoin_Historical_Data.csv")

# Clean Price column
df["Price"] = (
    df["Price"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Sort oldest -> newest
df = df.sort_values("Date").reset_index(drop=True)

# ==========================
# EMA PARAMETERS
# ==========================

short_window = 12
long_window = 26

# ==========================
# CALCULATE EMAs
# ==========================

df["EMA_12"] = df["Price"].ewm(
    span=short_window,
    adjust=False
).mean()

df["EMA_26"] = df["Price"].ewm(
    span=long_window,
    adjust=False
).mean()

# ==========================
# GENERATE SIGNALS
# ==========================

df["Signal"] = 0

# Buy signal
buy_condition = (
    (df["EMA_12"] > df["EMA_26"]) &
    (df["EMA_12"].shift(1) <= df["EMA_26"].shift(1))
)

# Sell signal
sell_condition = (
    (df["EMA_12"] < df["EMA_26"]) &
    (df["EMA_12"].shift(1) >= df["EMA_26"].shift(1))
)

df.loc[buy_condition, "Signal"] = 1
df.loc[sell_condition, "Signal"] = -1

# ==========================
# SAVE OUTPUT
# ==========================

output_cols = [
    "Date",
    "Price",
    "EMA_12",
    "EMA_26",
    "Signal"
]

df[output_cols].to_csv(
    "signals_EMA.csv",
    index=False
)

print("EMA signals saved to signals_EMA.csv")

print("\nSignal Counts:")
print(df["Signal"].value_counts())
