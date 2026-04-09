"""
Created on Thu Apr  2 11:12:52 2026

@author: Oskar
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "combined_log_2.txt")

#Load Data
df = pd.read_csv(FILE_PATH, parse_dates=["Timestamp"])
print(df.columns.tolist())


#Fix  Data
df[" Temperature_C"] = df[" Temperature_C"].replace(0, np.nan)
df[" Temperature_C"] = df[" Temperature_C"].interpolate(method='linear')
#Verify
print(f"Zeros remaining:{(df[' Temperature_C'] == 0).sum()}")



# Fills the 0s with the last value recorded before the drop
#df[" Temperature_C"] = df[" Temperature_C"].replace(0, np.nan).ffill()

#Plot
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(df["Timestamp"], df[" Pressure_mbar"], color="blue", label="Pressure")
ax1.set_xlabel("Timestamp")
plt.yscale('log')
ax1.set_ylabel("Pressure (mbar)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.tick_params(axis="x", rotation=45)
plt.grid(True, which="both", ls="--", alpha=0.5)

ax2 = ax1.twinx()
ax2.plot(df["Timestamp"], df[" Temperature_C"], color="red", label="Temperature", alpha = 0.5)
ax2.set_ylabel("Temperature (°C)", color="red")
ax2.tick_params(axis="y", labelcolor="red")


plt.title("Bakeout Monitoring")
fig.tight_layout()
plt.show()

