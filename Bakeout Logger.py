# -*- coding: utf-8 -*-
"""
Combined Serial Logger
Logs Temperature (OMEGA CN740 via RS485) and Pressure (Leybold COMBIVAC CM52)
Output: Timestamp, Pressure (mbar), Temperature (°C)
"""

import serial
import time
import os
import threading

# --- Temperature Config (OMEGA CN740) ---
TEMP_PORT     = 'COM13'
TEMP_BAUD     = 9600
SLAVE_ID      = '01'
REGISTER      = '4700'
FUNC_CODE     = '03'
NUM_REGS      = '0001'
SCALE         = 10
TEMP_INTERVAL = 2   # seconds

# --- Pressure Config (Leybold COMBIVAC CM52) ---
PRES_PORT     = 'COM11'
PRES_BAUD     = 19200
COMMAND       = "RPV3\r"
PRES_INTERVAL = 2    # seconds

# --- Output File ---
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "combined_log_2.txt")

# --- Shared State ---
latest_temperature = None
latest_pressure    = None
data_lock          = threading.Lock()

# --- Build Modbus ASCII frame for temperature ---
data_field = SLAVE_ID + FUNC_CODE + REGISTER + NUM_REGS
lrc        = f"{(-sum(int(data_field[i:i+2], 16) for i in range(0, len(data_field), 2))) & 0xFF:02X}"
TEMP_FRAME = f":{data_field}{lrc}\r\n"


def write_row():
    """Write a combined row when both values are available."""
    with data_lock:
        temp = latest_temperature
        pres = latest_pressure

    if temp is None or pres is None:
        return  # Wait until both sensors have reported at least once

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}, {pres:.2E}, {temp:.1f}\n"

    with open(FILE_PATH, "a") as f:
        f.write(log_entry)
    print(f"[{timestamp}]  P= {pres:.2E} mbar  |  T= {temp:.1f} °C")


def temperature_logger():
    global latest_temperature
    print(f"Temperature logger started on {TEMP_PORT}")
    while True:
        try:
            with serial.Serial(TEMP_PORT, TEMP_BAUD,
                               bytesize=7, parity='E', stopbits=1, timeout=1) as ser:
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(TEMP_FRAME.encode())
                response = ser.readline().decode('ascii', errors='replace').strip()

                raw_value = int(response[7:11], 16)
                temperature = raw_value / SCALE

                with data_lock:
                    latest_temperature = temperature

                write_row()

        except Exception as e:
            print(f"[Temperature] Error: {e}")

        time.sleep(TEMP_INTERVAL)


def pressure_logger():
    global latest_pressure
    print(f"Pressure logger started on {PRES_PORT}")
    while True:
        try:
            with serial.Serial(PRES_PORT, PRES_BAUD, timeout=1) as ser:
                ser.reset_input_buffer()
                ser.reset_output_buffer()
                ser.write(COMMAND.encode('ascii'))
                time.sleep(0.2)
                response = ser.readline().decode('ascii', errors='replace').strip()

                if len(response) >= 10:
                    data_str = response[-10:]
                    pressure = float(data_str)

                    with data_lock:
                        latest_pressure = pressure

                    write_row()
                else:
                    print(f"[Pressure] Response too short: '{response}'")

        except serial.SerialException as e:
            print(f"[Pressure] Serial Error: {e}")
        except ValueError:
            print(f"[Pressure] Format Error. Raw response: '{response}'")

        time.sleep(PRES_INTERVAL)


if __name__ == "__main__":
    # Initialise log file with header
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            f.write("Timestamp, Pressure_mbar, Temperature_C\n")
    print(f"Logging to: {FILE_PATH}")
    print("Press Ctrl+C to stop.\n")

    t_temp = threading.Thread(target=temperature_logger, daemon=True)
    t_pres = threading.Thread(target=pressure_logger,    daemon=True)

    t_temp.start()
    t_pres.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
        