import pandas as pd
import numpy as np

# Load CSV
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

# Parameters
window = 20
threshold = 1.5

# Rolling statistics
df["RollingMean"] = df["Price"].rolling(window).mean()
df["RollingStd"] = df["Price"].rolling(window).std()

# Z-score
df["ZScore"] = (
    (df["Price"] - df["RollingMean"])
    / df["RollingStd"]
)

# Signal column
df["Signal"] = 0

df.loc[df["ZScore"] < -threshold, "Signal"] = 1   # Buy
df.loc[df["ZScore"] > threshold, "Signal"] = -1   # Sell

#print(df[["Date", "Price", "ZScore", "Signal"]].tail())
print(df[["Date", "Price", "ZScore", "Signal"]])

# Save signals
df.to_csv("signals_mean_reversion.csv", index=False)
