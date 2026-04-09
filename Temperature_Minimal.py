import serial



# --- CONFIG ---
COM_PORT   = 'COM13'
BAUD       = 9600
SLAVE_ID   = '01'
REGISTER   = '4700'
FUNC_CODE  = '03'  # 03 = Read Holding Registers
NUM_REGS   = '0001'
SCALE      = 10    # CN740 scales values by x10
INTERVAL   = 1

#BUILD FRAME
data = SLAVE_ID + FUNC_CODE + REGISTER + NUM_REGS
lrc  = f"{(-sum(int(data[i:i+2], 16) for i in range(0, len(data), 2))) & 0xFF:02X}"
frame = f":{data}{lrc}\r\n"              #Device 01, please read 1 register from address 4700"
       
# --- SEND & RECEIVE ---
with serial.Serial(COM_PORT, BAUD, bytesize=7, parity='E', stopbits=1, timeout=1) as ser:
    ser.write(frame.encode())
    response = ser.readline().decode().strip()

raw_value   = int(response[7:11], 16)               #16 as in Base-16. Hex. Index 7:11 contain temp information
temperature = raw_value / SCALE

print(f"Sent:        {frame.strip()}")
print(f"Received:    {response}")
print(f"Temperature: {temperature:.1f} °C")

ser.close()



            