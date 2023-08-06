# Convx | A conversion tool for binary, hex, decimal.
[![License](https://img.shields.io/pypi/l/convx.svg)](https://github.com/The-Real-Thisas/convx/blob/main/LICENSE)
[![Version](https://img.shields.io/pypi/v/convx.svg)](https://pypi.org/project/convx/)
[![Python](https://img.shields.io/pypi/pyversions/convx.svg)](https://pypi.org/project/convx/)
[![Code Style](https://img.shields.io/badge/codestyle-black-black.svg)](https://github.com/ambv/black)
[![Build Status](https://dev.azure.com/Thisas/convx/_apis/build/status/The-Real-Thisas.convx?branchName=main)](https://dev.azure.com/Thisas/convx/_build/latest?definitionId=1&branchName=main)

![Banner](https://github.com/The-Real-Thisas/convx/blob/main/Convx-Logo/convx-banner.png)

This tool is created for a school lesson regarding Information Representation and conversion between binary, decimal and hex.

Further, this tool has the additional functionality of:
- Adding and subtracting binary. 
- Converting between decimal and binary using two's compliment.
- Converting between decimal and BCD. 

---

## Installation

To install Convx you can use `pip install`.

```bash
pip install convx
```

---

## Usage

Simply import Conx using `import`. The functions available are listed below.

```python
# Decimal to Binary
decimalToBinary(x: int)

# Binary to Decimal
binaryToDecimal(x: str)

# Decimal to Hex 
decimalToHex(x: str)

# Binary to Hex
binaryToHex(x: str)

# Decimal to BCD
decimalToBCD(x: int)

# BCD to Decimal
bcdToDecimal(x: str)

# Adding Binary
addBinary(x: str, y: str)

# Subtracting Binary
subBinary(x:str , y: str)

# Binary to Denary using two's compliment
twoBinaryToDenary(x: str)

# Denary to Binary using two's compliment
twoDenaryToBinary(x: int)
```
An example usage of Convx for a cli is given below :
```python
from convx import *

try:
    if str(sys.argv[1]) == "dtb":
        binary = decimalToBinary(int(sys.argv[2]))
        result = f"[*] {int(sys.argv[2])} to binary = {binary}"
        print(result)
    elif str(sys.argv[1]) == "btd":
        decimal = binaryToDecimal(str(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to decimal = {decimal}"
        print(result)
    elif str(sys.argv[1]) == "dth":
        hex = decimalToHex(str(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to hex = {hex}"
        print(result)
    elif str(sys.argv[1]) == "bth":
        hex = binaryToHex(str(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to hex = {hex}"
        print(result)
   elif str(sys.argv[1]) == "dtbcd":
        bcd = decimalToBCD(str(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to BCD = {bcd}"
        print(result)
   elif str(sys.argv[1]) == "bcdtd":
        decimal = bcdToDecimal(str(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to BCD = {decimal}"
        print(result)
    elif str(sys.argv[1]) == "add":
        binary = addBinary(str(sys.argv[2]), str(sys.argv[3]))
        result = f"[x] {str(sys.argv[2])} + {str(sys.argv[3])} = {binary}"
        print(result)
    elif str(sys.argv[1]) == "sub":
        binary = subBinary(str(sys.argv[2]), str(sys.argv[3]))
        result = f"[x] {str(sys.argv[2])} - {str(sys.argv[3])} = {binary}"
        print(result)
    elif str(sys.argv[1]) == "2btd":
        decimal = twoBinaryToDenary(str(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to decimal = {decimal}"
        print(result)
    elif str(sys.argv[1]) == "2dtb":
        binary = twoDenaryToBinary(int(sys.argv[2]))
        result = f"[*] {str(sys.argv[2])} to binary = {binary}"
        print(result)
    elif str(sys.argv[1]) == "help":
        print(help())
except IndexError:
    print("[*] No arguments inputed. Exiting.")
```
---

## Update Log

### 0.1.2

- Added usage in README.
- Updated example cli code.

### 0.1.1

- Added decimal to BCD and BCD to decimal.
- Added pytest for decimal to BCD and BCD to decimal.
- Added 'help' text at banner information.
