import decimal
import re

# set the precision to a relatively large number
# otherwise, the flag might not be decoded correctly
decimal.getcontext().prec = 100

opened_file = open("miniRSA")

content = opened_file.read()

# n contains 1 or more digits, therefore, [0-9]+
n = decimal.Decimal(re.search(r'N: ([0-9]+)', content).group(1))
# in this case, e only contains 1 digit, thus, [0-9]
e = decimal.Decimal(re.search(r'e: ([0-9])', content).group(1))
# c contains 1 or more digits, so we use the same regex as n
c = decimal.Decimal(re.search(r'\(c\): ([0-9]+)', content).group(1))

# round the result, otherwise, it won't return the correct type
m = round(c ** (1/e))

# convert the message to hex with hex(m)
# remove the prefix 0x with hex(m)[2:]
# create a bytearray so that it can be decoded back to string
flag = bytearray.fromhex(hex(m)[2:]).decode()

print(flag)
