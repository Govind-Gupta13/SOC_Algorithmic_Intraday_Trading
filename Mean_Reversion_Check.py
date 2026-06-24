import pandas as pd
import numpy as np

# ==========================
# LOAD FILES
# ==========================

price_df = pd.read_csv("Bitcoin_Historical_Data.csv")
signal_df = pd.read_csv("signals_mean_reversion.csv")

print("=" * 60)
print("FILES LOADED SUCCESSFULLY")
print("=" * 60)

# ==========================
# BASIC INFO
# ==========================

print("\nOriginal Data Shape:")
print(price_df.shape)

print("\nSignal Data Shape:")
print(signal_df.shape)

print("\nSignal File Columns:")
print(signal_df.columns.tolist())

# ==========================
# CHECK SIGNAL COUNTS
# ==========================

print("\n" + "=" * 60)
print("SIGNAL DISTRIBUTION")
print("=" * 60)

signal_counts = signal_df["Signal"].value_counts().sort_index()

print(signal_counts)

buy_count = (signal_df["Signal"] == 1).sum()
sell_count = (signal_df["Signal"] == -1).sum()
hold_count = (signal_df["Signal"] == 0).sum()

print(f"\nBUY Signals  (1): {buy_count}")
print(f"SELL Signals (-1): {sell_count}")
print(f"HOLD Signals (0): {hold_count}")

# ==========================
# VERIFY BUY SIGNALS
# ==========================

print("\n" + "=" * 60)
print("VERIFYING BUY SIGNALS")
print("=" * 60)

buy_rows = signal_df[signal_df["Signal"] == 1]

incorrect_buy = buy_rows[buy_rows["ZScore"] >= -1.5]

print(f"Total BUY signals: {len(buy_rows)}")
print(f"Incorrect BUY signals: {len(incorrect_buy)}")

if len(incorrect_buy) > 0:
    print("\nIncorrect BUY rows:")
    print(
        incorrect_buy[
            ["Date", "Price", "ZScore", "Signal"]
        ].head(10)
    )

# ==========================
# VERIFY SELL SIGNALS
# ==========================

print("\n" + "=" * 60)
print("VERIFYING SELL SIGNALS")
print("=" * 60)

sell_rows = signal_df[signal_df["Signal"] == -1]

incorrect_sell = sell_rows[sell_rows["ZScore"] <= 1.5]

print(f"Total SELL signals: {len(sell_rows)}")
print(f"Incorrect SELL signals: {len(incorrect_sell)}")

if len(incorrect_sell) > 0:
    print("\nIncorrect SELL rows:")
    print(
        incorrect_sell[
            ["Date", "Price", "ZScore", "Signal"]
        ].head(10)
    )

# ==========================
# SHOW SAMPLE SIGNALS
# ==========================

print("\n" + "=" * 60)
print("FIRST 20 SIGNAL ROWS")
print("=" * 60)

print(
    signal_df[
        ["Date", "Price", "ZScore", "Signal"]
    ].head(20)
)

print("\n" + "=" * 60)
print("LAST 20 SIGNAL ROWS")
print("=" * 60)

print(
    signal_df[
        ["Date", "Price", "ZScore", "Signal"]
    ].tail(20)
)

# ==========================
# SHOW ALL BUYS
# ==========================

print("\n" + "=" * 60)
print("FIRST 10 BUY SIGNALS")
print("=" * 60)

print(
    signal_df[signal_df["Signal"] == 1][
        ["Date", "Price", "ZScore"]
    ].head(10)
)

# ==========================
# SHOW ALL SELLS
# ==========================

print("\n" + "=" * 60)
print("FIRST 10 SELL SIGNALS")
print("=" * 60)

print(
    signal_df[signal_df["Signal"] == -1][
        ["Date", "Price", "ZScore"]
    ].head(10)
)

# ==========================
# CHECK CONSECUTIVE SELLS
# ==========================

print("\n" + "=" * 60)
print("CONSECUTIVE SIGNAL ANALYSIS")
print("=" * 60)

signal_df["PrevSignal"] = signal_df["Signal"].shift(1)

consecutive_sells = (
    (signal_df["Signal"] == -1)
    & (signal_df["PrevSignal"] == -1)
).sum()

consecutive_buys = (
    (signal_df["Signal"] == 1)
    & (signal_df["PrevSignal"] == 1)
).sum()

print(f"Consecutive SELL signals: {consecutive_sells}")
print(f"Consecutive BUY signals : {consecutive_buys}")

# ==========================
# SAVE REPORT
# ==========================

signal_df.to_csv(
    "signals_verified.csv",
    index=False
)

print("\nVerification complete.")
print("Output saved as signals_verified.csv")
