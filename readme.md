## Spassm.py <span style="color:#CCC"> - Siverv's Password Manager</span>

#### How to use:
    python3.2 spassm.py <file> <masterkey> add <sitecode> <pass>
    python3.2 spassm.py <file> <masterkey> overwrite <sitecode> <pass>
    python3.2 spassm.py <file> <masterkey> [show]
    python3.2 spassm.py <file> <masterkey> showonly <sitecode>
    python3.2 spassm.py <file> <masterkey> remove <sitecode>
    python3.2 spassm.py <file> <masterkey> help

In Bash, you may use the command "unset HISTFILE" to stop the terminal from saving the commands when it closes.

#### The Masterkey:
    [bodx6ae]:E_1[,[bodx6ae]:E_2,...]
        b: A binary number.
        o: An octal number.
        d: A decimal number.
        x: A hexadecimal number.
        6: A base 64 number.
        a: An Latin-1 string. The key will be the binary value of the string
        e: A mathematical expression using the following operators *,
           **(power), /, +, - and can make use of parentheses.
                ex: 5*(2**(7-2/6))-4

E_n depends on the parameter before the colon. If no parameter or colon given, it is assumed that the key is an Latin-1 string.

Keep in mind this is uses XOR to encrypt, which can be analyzed to figure out the hidden content. To make the analyzing harder, use multiple keys, preferebly large prime numbers or huge numbers like 242**223+14221.
<br/><br/>
This password manager was made purely for personal use, but feel free to use and edit it in any manner you would like.
#### - Siverv
