from riposte import Riposte

print(
"""
 ________  ________  ________   ___      ___ ___    ___ 
|\   ____\|\   __  \|\   ___  \|\  \    /  /|\  \  /  /|
\ \  \___|\ \  \|\  \ \  \\\\ \  \ \  \  /  / | \  \/  / /
 \ \  \    \ \  \\\\\  \ \  \\\\ \  \ \  \/  / / \ \    / / 
  \ \  \____\ \  \\\\\  \ \  \\\\ \  \ \    / /   /     \/  
   \ \_______\ \_______\ \__\\\\ \__\ \__/ /   /  /\   \  
    \|_______|\|_______|\|__| \|__|\|__|/   /__/ /\ __\ 
                                            |__|/ \|__| 
                                                        
"""
)
calculator = Riposte(prompt="▲:~$ ")

MEMORY = []


@calculator.command("dtb")
def decimalToBinary(x: int):
    binary = format(x, "b")
    # binary = "{0:b}".format(int(x))
    result = f"{x} to binary = {binary}"
    return binary
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("btd")
def binaryToDecimal(x):
    # i,integer = 0,0
    # size = len(x)
    # while i < len(x):
    #    integer += int(x[size - 1 - i])*pow(2,i)
    #     i+=1
    integer = int(x, 2)
    result = f"{x} to integer = {integer}"
    return integer
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("dth")
def decimalToHex(x):
    hex = format(int(x), "X")
    result = f"{x} to hex = {hex}"
    return hex
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("bth")
def binaryToHex(x):
    integer = int(x, 2)
    calculator.status("Converting to integer: ", x, "to", integer)
    hex = format(integer, "X")
    result = f"{x} to hex = {hex}"
    return hex
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("add")
def add(x: str, y: str):
    max_len = max(len(x), len(y))
    x = x.zfill(max_len)
    y = y.zfill(max_len)
    calculator.status("Initializing Result")
    result = ""
    calculator.status("Initializing Carry")
    carry = 0
    calculator.status("Traversing String")
    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if x[i] == "1" else 0
        r += 1 if y[i] == "1" else 0
        result = ("1" if r % 2 == 1 else "0") + result
        calculator.info("- Result (", i, ") :", result)
        # calculator.info("- [/] Computing Carry")
        carry = 0 if r < 2 else 1
        calculator.info("- Carry :", r)
    if carry != 0:
        calculator.info("- Carry !=0, adding 1 to start of", result)
        result = "1" + result
    result = f"{x} + {y} = {result.zfill(max_len)}"
    # With Internal Functions
    # sum = bin(int(x, 2) + int(y, 2))
    # print(sum[2:])
    return result.zfill(max_len)
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("sub")
def sub(x: str, y: str):
    binary = bin(int(x, 2) - int(y, 2))[2:]
    result = f"{x} - {y} = {binary}"
    return binary
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("2dtb")
def twoDenaryToBinary(x: int):
    calculator.status("Checking if Positive or Negative")
    if x >= 0:
        calculator.info("[*] Binary is Positive, using normal conversion process")
        binary = format(x, "b")
    else:
        calculator.info("[*] Binary is Negative, using two's compliment")
        denary = str(x)[1:]
        valueList = list(str(bin(int(denary))[2:]))
        calculator.status("Adding MSB")
        valueList.insert(0, "0")
        valueList = [int(i) for i in valueList]
        calculator.status("Inverting value array (finding one's compliment)")
        for i in range(len(valueList)):
            if valueList[i] == 1:
                valueList[i] = "0"
            elif valueList[i] == 0:
                valueList[i] = "1"
            else:
                calculator.error("Error Inverting Value")
        calculator.info("[*] Joining Array into String")
        binary = "".join(str(element) for element in valueList)
        calculator.info("[*] Converting to binary and adding 1 ... for some reason")
        binary = bin(int(binary, 2) + 1)[2:]

    result = f"{x} to binary = {binary}"
    return binary
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("2btd")
def twoBinaryToDenary(x: str):
    valueList = list(x)
    integer = ""
    calculator.status("Checking MSB")
    if valueList[0] == "0":
        calculator.info("[*] Binary is Positive, using normal conversion process")
        integer = int(x, 2)
    elif valueList[0] == "1":
        calculator.info("[*] Binary is Negative, using two's compliment")
        calculator.status("Inverting value array (finding one's compliment)")
        valueList = [int(i) for i in valueList]
        for i in range(len(valueList)):
            if valueList[i] == 1:
                valueList[i] = "0"
            elif valueList[i] == 0:
                valueList[i] = "1"
            else:
                calculator.error("Error Inverting Value")
        calculator.info(
            "[*] Converting to string, adding '-' and adding 1 ... for some reason."
        )
        binary = "".join(str(element) for element in valueList)
        integer = "-" + str(int(binary, 2) + 1)
    else:
        calculator.error("Invalid Value")
    result = f"{x} to integer = {integer}"
    return integer
    MEMORY.append(result)
    calculator.success(result)


@calculator.command("help")
def help():
    calculator.print(
        """ 
  Commands:
    - Conversions
      - Decimal to Binary : dtb
      - Binary to Decimal : btd
      - Decimal to hex    : dth
      - Binary to hex     : bth  

    - Adding Binary
      - Command           : add
      - Usage             : add x y

    - Subtracting Binary
      - Command           : sub
      - Usage             : sub x y

    - Two's complement
      - Decimal to Binary : 2dtb
      - Binary to Decimal : 2btd
    
    - Memory
      - Command           : memory
      - Usage             : memory
      """
    )
    return """ 
  Commands:
    - Conversions
      - Decimal to Binary : dtb
      - Binary to Decimal : btd
      - Decimal to hex    : dth
      - Binary to hex     : bth  

    - Adding Binary
      - Command           : add
      - Usage             : add x y

    - Subtracting Binary
      - Command           : sub
      - Usage             : sub x y

    - Two's complement
      - Decimal to Binary : 2dtb
      - Binary to Decimal : 2btd
    
    - Memory
      - Command           : memory
      - Usage             : memory
      """


@calculator.command("memory")
def memory():
    for entry in MEMORY:
        calculator.print(entry)


@calculator.command("exit")
def close():
    exit()


if __name__ == "__main__":
    calculator.run()

