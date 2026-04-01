# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:54:00 2026

@author: Claude + ChatGPT
"""

import serial
import time
import os


# --- CONFIG ---
COM_PORT   = 'COM3'
BAUD       = 9600
SLAVE_ID   = '01'
REGISTER   = '4700'
FUNC_CODE  = '03'  # 03 = Read Holding Registers
NUM_REGS   = '0001'
SCALE      = 10    # CN740 scales values by x10
INTERVAL   = 60

#BUILD FRAME
data = SLAVE_ID + FUNC_CODE + REGISTER + NUM_REGS
lrc  = f"{(-sum(int(data[i:i+2], 16) for i in range(0, len(data), 2))) & 0xFF:02X}"
frame = f":{data}{lrc}\r\n"              #Device 01, please read 1 register from address 4700"


# --- Logging Code ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("Directory of script:" , BASE_DIR)
FILE_PATH = os.path.join(BASE_DIR, "Temp_Test.txt")



if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:                 #"w" 
        f.write("Timestamp, Temperature / °C\n")

count = 0
try:    
    while count <= 100:
        count += 1
    #print(count, "count")
        with serial.Serial(COM_PORT, BAUD,  bytesize=7, parity='E', stopbits=1, timeout=1) as ser:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            
            ser.write(frame.encode())
            time.sleep(INTERVAL) 
            response = ser.readline().decode('ascii', errors='replace').strip()
            
            raw_value   = int(response[7:11], 16)               #16 as in Base-16. Hex. Index 7:11 contain temp information
            temperature = raw_value / SCALE
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp}, {temperature:.1f} °C"
            #print(log_entry)
            with open(FILE_PATH, "a") as f:             #"a" append to file
                f.write(log_entry + "\n")
except KeyboardInterrupt:
   print("\nLogging stopped by user")
           
                        
