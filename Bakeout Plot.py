"""
Created on Thu Apr  2 11:12:52 2026

@author: Oskar
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Configuration for file path
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "combined_log_2.txt")

#Functions
#Load Data
def load_data(filepath):
    '''Reads CSV file with date and returns list of column names'''
    df = pd.read_csv(FILE_PATH, parse_dates=["Timestamp"])
    print(f"Loaded {len(df)} rows. Columns: {df.columns.tolist()}")
    return df
    
def clean_temperature_data(df, col=" Temperature_C"):
    df = df.copy()
    df[col] = df[col].replace(0, np.nan).interpolate(method='linear')
    return df

def verify_clean(df, col=" Temperature_C"):
    '''Print check for zeros and nans'''
    zeros = (df[col]==0).sum()
    nans = df[col].isna().sum()
    return print(f"Zeros remaining: {zeros} | NaNs remaining: {nans} ")
    
def plot_bakeout(df):
   """Plot pressure and temperature on twin axes"""
   fig, ax1 = plt.subplots(figsize=(10, 5))
   
   ax1.plot(df["Timestamp"], df[" Pressure_mbar"], color="blue", label="Pressure")
   ax1.set_xlabel("Timestamp")
   ax1.set_yscale('log')
   ax1.set_ylabel("Pressure (mbar)", color="blue")
   ax1.tick_params(axis="y", labelcolor="blue")
   ax1.tick_params(axis="x", rotation=45)
   ax1.grid(True, which="both", ls="--", alpha=0.5)

   ax2 = ax1.twinx()
   ax2.plot(df["Timestamp"], df[" Temperature_C"], color="red", label="Temperature", alpha = 0.5)
   ax2.set_ylabel("Temperature (°C)", color="red")
   ax2.tick_params(axis="y", labelcolor="red")
   
   fig.suptitle("Bakeout Monitoring")
   fig.tight_layout()
   plt.show()
   
def main():
    df = load_data(FILE_PATH)
    df = clean_temperature_data(df)
    verify_clean(df)
    plot_bakeout(df)

    
if __name__ == "__main__":
    main()
    






