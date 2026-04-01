### How Modbus ASCII communication works (step by step)
'''
**1. Frame structure**

: 01 03 4700 0001 B4 \r\n
│ │  │  │    │    │
│ │  │  │    │    └─ LRC checksum (2 hex chars)
│ │  │  │    └────── number of registers to read (1)
│ │  │  └─────────── register address (0x4700)
│ │  └────────────── function code 03 = "read holding registers"
│ └───────────────── slave ID (device address)
└─────────────────── start-of-frame marker
```

**2. Serial port settings (7E1)**

| Setting | Value | Why |
|---|---|---|
| Baud | 9600 | CN740 default |
| Data bits | **7** | ASCII mode uses 7-bit chars |
| Parity | **Even** | Error detection |
| Stop bits | 1 | Standard |

**3. LRC checksum**
Add all data bytes together → negate → keep lowest 8 bits:
```
01 + 03 + 47 + 00 + 00 + 01 = 0x4C  →  negate → 0xB4
```

**4. Response frame**
```
: 01 03 02 01F4 XX \r\n
         │  │
         │  └── raw value: 0x01F4 = 500 → 500/10 = 50.0 °C
         └───── byte count (2 bytes = 1 register)
'''