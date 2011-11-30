#### SPASSM ###################
## Siverv's Password Manager ##
################# svrv.net ####

help = """
#### SPASSM ###################
## Siverv's Password Manager ##
################# svrv.net ####

How to use:
    python3.2 spassm.py <file> <masterkey> add <sitecode> <pass>
    python3.2 spassm.py <file> <masterkey> overwrite <sitecode> <pass>
    python3.2 spassm.py <file> <masterkey> [show]
    python3.2 spassm.py <file> <masterkey> showonly <sitecode>
    python3.2 spassm.py <file> <masterkey> remove <sitecode>
    python3.2 spassm.py <file> <masterkey> help

    In Bash, one can use the command "unset HISTFILE" to stop the terminal from saving the commands when it closes.

The Masterkey:
    [bodx6ae]:E_1[,[bodx6ae]:E_2,...]
    E_n depends on the parameter before the colon. If no parameter or colon given, it is assumed that the key is an Latin-1 string.
        b: A binary number.
        o: An octal number.
        d: A decimal number.
        x: A hexadecimal number.
        6: A base 64 number.
        a: An Latin-1 string. The key will be the binary value of the string
        e: A mathematical expression using the following operators *, **(power), /, +, - and can make use of parentheses.
                ex: 5*(2**(7-2/6))-4

    Keep in mind this is uses XOR to encrypt, which can be analyzed to figure out the hidden content. To make the analyzing harder, use multiple keys, preferebly large prime numbers or huge numbers like 242**223+14221
"""

import sys
import re
import base64

RJUSTCONSTANT = 30
SPLITTER = " : " 

def readFile(path):
    f = open(path,'rb')
    r = f.read()
    f.close()
    return r

def writeFile(data,path):
    f = open(path,'wb')
    f.write(data)
    f.close()

def generateKey(raw):
    keys = raw.split(',')
    parsedKeys = [];
    for key in keys:
        data = key.split(':')
        if len(data) == 1:
            code = "a"
            data = data[0]
        else:
            code,data = data;
        if code == "b":
            parsedKeys.append(code)
        elif code in "odx":
            parsedKeys.append(bin(int(data,10 if code=="d" else (8 if code=="o" else 16)))[2:])
        elif code == "6":
            parsedKeys.append(base64.decodestring(data))
        elif code == "a":
            parsedKeys.append("".join([bin(x)[2:] for x in data.encode("Latin-1")]))
        elif code == "e":
            parsedKeys.append(bin(eval(re.sub(r'[^()0-9+\-*/]','',data)))[2:])
        else:
            return print("Invalid masterkey")
    return parsedKeys

def switch(bytes,key):
    l = len(key)
    i = 0
    output = ""
    for byte in bytes:
        newbyte = ""
        for bit in bin(byte)[2:].zfill(8):
            newbyte += str(int(bit)^int(key[i%l]))
            i += 1
        output += chr(int(newbyte,2))
    return output

def stitch(pairs,masterkey):
    data = ";".join([(code+":"+pairs[code]) for code in pairs]).encode("Latin-1")
    for key in masterkey:
        data = switch(data,key).encode("Latin-1")
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No File")
    elif len(sys.argv) < 3:
        print("No Masterkey")
    else:
        masterkey = generateKey(sys.argv[2])
        if masterkey != None:
            data = readFile(sys.argv[1])
            for key in masterkey:
                data = switch(data,key).encode("Latin-1")
            data = data.decode("Latin-1")
            rawpairs = data.split(";")
            if len(data) != 0 and (len(data.split(":")) != 1) and not (len(data.split(";")) == len(data.split(":"))-1):
                print(data)
            elif len(sys.argv) == 3 or sys.argv[3] == "show":
                print("\n".join([x.split(":")[0].rjust(RJUSTCONSTANT)+SPLITTER+x.split(":")[1] for x in rawpairs]))
            elif sys.argv[3] == "help":
                print(help)
            else:
                pairs = {}
                if len(rawpairs[0]) != 0:
                    for pair in rawpairs:
                        if len(pair.split(":")) != 2:
                            print(repr(pair))
                        code,passw = pair.split(":")
                        pairs[code] = passw;
                if sys.argv[3] == "add" and len(sys.argv) == 6:
                    if sys.argv[4] not in pairs.keys():
                        pairs[sys.argv[4]] = sys.argv[5]
                elif sys.argv[3] == "overwrite" and len(sys.argv) == 6:
                    pairs[sys.argv[4]] = sys.argv[5]
                elif sys.argv[3] == "showonly" and len(sys.argv) == 5:
                    if sys.argv[4] in pairs.keys():
                        print(sys.argv[4].rjust(RJUSTCONSTANT)+SPLITTER+pairs[sys.argv[4]])
                elif sys.argv[3] == "remove" and len(sys.argv) == 5:
                    if sys.argv[4] in pairs.keys():
                        del pairs[sys.argv[4]]
                writeFile(stitch(pairs,masterkey),sys.argv[1])

