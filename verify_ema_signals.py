import pandas as pd
import numpy as np

# ==========================
# LOAD FILE
# ==========================

df = pd.read_csv("signals_EMA.csv")

print("=" * 60)
print("EMA SIGNAL VERIFICATION")
print("=" * 60)

# ==========================
# BASIC INFO
# ==========================

print("\nRows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

# ==========================
# SIGNAL COUNTS
# ==========================

print("\n" + "=" * 60)
print("SIGNAL DISTRIBUTION")
print("=" * 60)

print(df["Signal"].value_counts().sort_index())

# ==========================
# VERIFY BUY SIGNALS
# ==========================

print("\n" + "=" * 60)
print("VERIFYING BUY SIGNALS")
print("=" * 60)

buy_rows = df[df["Signal"] == 1]

incorrect_buy = buy_rows[
    ~(
        (buy_rows["EMA_12"] > buy_rows["EMA_26"])
    )
]

print("Total BUY signals:", len(buy_rows))
print("Incorrect BUY signals:", len(incorrect_buy))

if len(incorrect_buy) > 0:
    print(incorrect_buy.head())

# ==========================
# VERIFY SELL SIGNALS
# ==========================

print("\n" + "=" * 60)
print("VERIFYING SELL SIGNALS")
print("=" * 60)

sell_rows = df[df["Signal"] == -1]

incorrect_sell = sell_rows[
    ~(
        (sell_rows["EMA_12"] < sell_rows["EMA_26"])
    )
]

print("Total SELL signals:", len(sell_rows))
print("Incorrect SELL signals:", len(incorrect_sell))

if len(incorrect_sell) > 0:
    print(incorrect_sell.head())

# ==========================
# SHOW BUYS
# ==========================

print("\n" + "=" * 60)
print("FIRST 10 BUY SIGNALS")
print("=" * 60)

print(
    buy_rows[
        ["Date", "Price", "EMA_12", "EMA_26"]
    ].head(10)
)

# ==========================
# SHOW SELLS
# ==========================

print("\n" + "=" * 60)
print("FIRST 10 SELL SIGNALS")
print("=" * 60)

print(
    sell_rows[
        ["Date", "Price", "EMA_12", "EMA_26"]
    ].head(10)
)

# ==========================
# CHECK CONSECUTIVE SIGNALS
# ==========================

print("\n" + "=" * 60)
print("CONSECUTIVE SIGNAL CHECK")
print("=" * 60)

df["PrevSignal"] = df["Signal"].shift(1)

consecutive_buy = (
    (df["Signal"] == 1) &
    (df["PrevSignal"] == 1)
).sum()

consecutive_sell = (
    (df["Signal"] == -1) &
    (df["PrevSignal"] == -1)
).sum()

print("Consecutive BUY signals :", consecutive_buy)
print("Consecutive SELL signals:", consecutive_sell)

# ==========================
# SHOW LAST 20 ROWS
# ==========================

print("\n" + "=" * 60)
print("LAST 20 ROWS")
print("=" * 60)

print(
    df[
        ["Date", "Price", "EMA_12", "EMA_26", "Signal"]
    ].tail(20)
)

print("\nVerification Complete.")
