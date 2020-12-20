#!/usr/bin/python3
from collections import Counter
from math import log, ceil


def count_bytes(filename: str) -> (dict, int, int):
    try:
        f = open(filename, 'rb')
    except FileNotFoundError:
        print('No file named: ' + filename)
        return -1
    txt = f.read()
    l = list(txt)
    #wc = len(txt.split(' '))
    c = Counter(l)
    f.close()

    d = dict(c.most_common())
    return {x: y/len(l) for x, y in d.items()}, len(l), d


def entropy(letters: dict) -> (dict, float):
    res = {}
    entropy_sum = 0.0
    for x, y in letters.items():
        temp = y * log((1/y), 2)
        res[x] = temp
        entropy_sum += temp

    return res, entropy_sum


def calculate_code_len(letters: dict) -> dict:
    res = {}

    for x, y in letters.items():
        res[x] = ceil(-log(y, 2))

    return res


def create_code(code_len: dict) -> dict:
    res = {}
    code = '0'

    for x, y in code_len.items():
        while len(code) <  y:
            code = code + '0'
        res[x] = code
        
        old_len = len(code)
        code = str(bin(int(code, 2) + 1))[2:]
        while old_len > len(code):
            code = '0' + code

    return res


def calculate_padding(code_len: dict, occurrence: dict) -> int:
    length = 0

    for x, y in zip(code_len.values(), occurrence.values()):
        length += x * y

    return length % 8


def compress(filename: str, code: dict, pad: int, filename_out: str) -> str:
    f_in = open(filename, 'rb')
    f_out = open(filename_out, 'wb')
    text = f_in.read()
    buffor = ''

    temp_code = {chr(x): y for x, y in code.items()}
    code['pad'] = 8-pad
    temp_code['pad'] = 8-pad
    str_code = str(temp_code)

    str_code = str(temp_code).encode('utf-8')

    f_out.write((str(len(str_code)) + '|').encode('utf-8'))
    f_out.write(str_code)

    f_str = b''
    for c in text:
        buffor += code[c]

    for i in range(0, len(buffor), 8):
        f_str += bytes([int(buffor[i:i+8], 2)])

    f_out.write(f_str)

    f_in.close()
    f_out.close()

    return "ok"


def extract(filename: str, filename_out: str) -> str:
    f = open(filename, 'rb')
    s = f.read()

    i = 0
    code_size = ''
    while s[i] != ord('|'):
        code_size += str(int(chr(s[i])))
        i += 1
    
    code_str = s[i+1:int(code_size) + i + 1]

    code = eval(code_str)

    pad = code['pad']
    del(code['pad'])
    s = s[int(code_size) + i + 1:]
    
    #for b in s:
    #    print(hex(b))

    file_str = b''
    buffor = ''
    for i in range(len(s)):
        byte = bin(s[i])[2:]
        for _ in range(8 - len(byte)):
            byte = '0' + byte
        if i == (len(s) - 1):
            byte = byte[:(8-pad)]
        buffor += byte
        
        flag = False
        while buffor and not flag:
            for c in code.items():
                if buffor[:len(c[1])] == c[1]:
                    char = c[0]
                    file_str += bytes([ord(char)])
                    buffor = buffor[len(c[1]):]
                    flag = False
                    break
                else:
                    flag = True
                    
    f.close()
    f_out = open(filename_out, 'w')
    f_out.write(file_str.decode('utf-8'))
    f_out.close()


def test():
    d, bc, occurrence = count_bytes('makbet-pl.txt')
    information_gain, input_entropy = entropy(d)
    code_len = calculate_code_len(d)
    code = create_code(code_len)
    compress('makbet-pl.txt', code, calculate_padding(code_len, occurrence))
    extract('makbet-pl.txt.sf')


