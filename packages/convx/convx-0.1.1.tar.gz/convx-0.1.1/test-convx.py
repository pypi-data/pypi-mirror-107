from convx import *


def test_convx_decimalToBinary():
    assert decimalToBinary(25) == "11001"


def test_convx_binaryToDecimal():
    assert binaryToDecimal("11001") == 25


def test_convx_decimalToHex():
    assert decimalToHex(25) == "19"


def test_convx_binaryToHex():
    assert binaryToHex("11001") == "19"


def test_convx_addBinary():
    assert addBinary("101", "101") == "1010"


def test_convx_subBinary():
    assert subBinary("1010", "101") == "101"


def test_convx_twoDenaryToBinary():
    assert twoDenaryToBinary(-25) == "100111"


def test_convx_twoBinaryToDenary():
    assert twoBinaryToDenary("100111") == -25

def test_convx_decimalToBCD():
    assert decimalToBCD(12) == "0001 0010"

def test_convx_bcdToDecimal():
    assert bcdToDecimal("00010010") == 12
