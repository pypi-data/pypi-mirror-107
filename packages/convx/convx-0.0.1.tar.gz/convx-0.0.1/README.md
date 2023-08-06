[![License](https://img.shields.io/pypi/l/convx.svg)](https://github.com/The-Real-Thisas/convx/blob/main/LICENSE)

[![Version](https://img.shields.io/pypi/v/convx.svg)](https://pypi.org/project/convx/)

[![Python](https://img.shields.io/pypi/pyversions/convx.svg)](https://pypi.org/project/convx/)

[![Code Style](https://img.shields.io/badge/codestyle-black-black.svg)](https://github.com/ambv/black)


# Convx | A conversion tool for binary, hex, decimal.

This tool is created for a school lesson regarding Information Representation and conversion between binary, decimal and hex.

Further, this tool has the additional functionality of adding and subtracting decimals, and converting between decimal and binary using two's compliment.

...

## Installation

To install Convx you can use `pip install`.

```bash
pip install convx
```

...

## Usage

Simply import Conx using `import`. Then use as seen in the example of a cli program below.

```bash
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

