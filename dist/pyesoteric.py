# encoding mapping
MAPPING = {'(':0,')':1,'=':2,'c':3,'e':4,'x':5,'%':6}
MAPPING_INV = {0:'(',1:')',2:'=',3:'c',4:'e',5:'x',6:'%'}

# variable names
VARS = {
    43: "e", # ord("+")
    "data": "x", # encoded program
    "mapping": "c", # encoding mapping
    "decoder": "xx", # decoder program
    1: "cc", # 2^0
    2: "ce", # 2^1
    4: "cx", # 2^2
    8: "ec", # 2^3
    16: "ee", # 2^4
    32: "ex", # 2^5
    64: "xc", # 2^6
    128: "xe", # 2^7
}

# decoder
DECODER = f"exec(''.join(chr({VARS['mapping']}[{VARS['data']}[i]]+{VARS['mapping']}[{VARS['data']}[i+1]]*7+{VARS['mapping']}[{VARS['data']}[i+2]]*7*7)for i in range(0,len({VARS['data']}),3)))"
DECODER += " " * (6 - (len(DECODER) % 6))

# extra variable namespaces
NAMESPACES = ["".join("cex"[(j//(3**k))%3] for k in range(i)) for i in range(3, 6) for j in range(3**i)]

# starting variables
OUTPUT = f"{VARS['data']}='%c%%c%%%%c%%%%%%%%c%%%%%%%%%%%%%%%%c%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%c'\n" # string formatting template for 6 characters at a time
OUTPUT += f"{VARS[43]}=''==()\n" # 0 (False)
OUTPUT += f"{VARS[1]}=()==()\n" # 1 (True)
OUTPUT += f"exec('{VARS[2]}=%x%%x%%%%x'%{VARS[1]}%{VARS[43]}%{VARS[1]})\n" # 101
OUTPUT += f"exec('{VARS[2]}%%%%=%x%%x'%{VARS[1]}%{VARS[1]})\n" # 2 (101 % 11)
OUTPUT += f"exec('{VARS[43]}=%x%%x%%%%x%%%%%%%%x'%{VARS[1]}%{VARS[1]}%{VARS[1]}%{VARS[1]})\n" # 1111
OUTPUT += f"exec('{VARS[43]}%%%%%%%%=%x%%x%%%%x'%{VARS[1]}%{VARS[1]}%{VARS[2]})\n" # 103 (1111 % 112)
OUTPUT += f"exec('{VARS[43]}=%x'%{VARS[43]})\n" # 67 (103 = 0x67)
OUTPUT += f"exec('{VARS[43]}=%x'%{VARS[43]})\n" # 43 (67 = 0x43)

# create powers of 2
for x in [4, 8, 16, 32, 64, 128]:
    OUTPUT += f"exec('{VARS[x]}={VARS[x>>1]}%c{VARS[x>>1]}'%{VARS[43]})\n"

# encoding for decoder
COUNT = 0
for c in map(ord, sorted(set(DECODER+":{|}"))):
    if c in VARS:
        continue
    VARS[c] = NAMESPACES[COUNT]
    COUNT += 1
    # 2k decomp
    rem = c
    pows = []
    while rem:
        pows.append(rem&-rem)
        rem -= rem&-rem
    # first 4 powers
    OUTPUT += f"exec('{VARS[c]}={VARS[pows[0]]}{''.join('%'*(2**i) + 'c' + VARS[p] for i, p in enumerate(pows[1:4]))}'{('%' + VARS[43])*min(3, len(pows)-1)})\n"
    # subsequent 4 powers
    if len(pows) > 4:
        OUTPUT += f"exec('{VARS[c]}%c={VARS[pows[4]]}{''.join('%'*(2**(i+1)) + 'c' + VARS[p] for i, p in enumerate(pows[5:]))}'{('%' + VARS[43])*(len(pows)-4)})\n"

# encode decoder
OUTPUT += "xx=''\n"
for i in range(0, len(DECODER), 6):
    OUTPUT += f"exec('{VARS['decoder']}%c={VARS['data']}{''.join('%%'+VARS[ord(DECODER[i+j])] for j in range(6))}'%{VARS[43]})\n"

# include mapping dict
OUTPUT += f"exec('''{VARS['mapping']}=%c'%%%%%%%%%%%%%%%%'%%c{VARS[4]}%%%%c{VARS[2]}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[43]}%{VARS[125]})\n" # %: 4+2=6
OUTPUT += f"exec('''{VARS['mapping']}%%%%c=%c'('%%c{VARS[43]}=={VARS['data']}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[124]}%{VARS[125]})\n" # (: 0 (False)
OUTPUT += f"exec('''{VARS['mapping']}%%%%c=%c')'%%c{VARS[1]}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[124]}%{VARS[125]})\n" # ): 1
OUTPUT += f"exec('''{VARS['mapping']}%%%%c=%c'='%%c{VARS[2]}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[124]}%{VARS[125]})\n" # =: 2
OUTPUT += f"exec('''{VARS['mapping']}%%%%c=%c'c'%%c{VARS[2]}%%%%%%%%%%%%%%%%c{VARS[1]}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[124]}%{VARS[125]}%{VARS[43]})\n" # c: 2+1=3
OUTPUT += f"exec('''{VARS['mapping']}%%%%c=%c'e'%%c{VARS[4]}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[124]}%{VARS[125]})\n" # e: 4
OUTPUT += f"exec('''{VARS['mapping']}%%%%c=%c'x'%%c{VARS[4]}%%%%%%%%%%%%%%%%c{VARS[1]}%%%%%%%%c'''%{VARS[123]}%{VARS[58]}%{VARS[124]}%{VARS[125]}%{VARS[43]})\n" # x: 4+1=5

def decode(src):
    src = src.split("\n")[76][3:-1]
    return ''.join(chr(MAPPING[src[i]]+MAPPING[src[i+1]]*7+MAPPING[src[i+2]]*7*7)for i in range(0,len(src),3))

def encode(source):
    if len(set(source)) <= 9:
        return source # already 9 or less unique characters
    return OUTPUT + f"{VARS['data']}='{''.join(MAPPING_INV[ord(c)%7]+MAPPING_INV[ord(c)//7%7]+MAPPING_INV[ord(c)//49%7] for c in source)}'\nexec({VARS['decoder']})"

