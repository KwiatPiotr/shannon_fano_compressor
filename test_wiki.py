#!/usr/bin/python3
from collections import Counter
from math import log
from math import ceil



def create_results(filename: str) -> int:
    result_file_name = filename.split('.')[0] + '_res.txt'
    result_file = open(result_file_name, 'w')

    result_file.write(filename + ' resuts\n\n')

    d, word_count, characters_count = count_letters(filename)
    result_file.write(filename + ' has:\n')
    result_file.write('\t - words: ' + str(word_count) + '\n')
    result_file.write('\t - characters: ' + str(characters_count) + '\n')
    result_file.write('\n\n')

    result_file.write('Characters probability:\n')
    for x, y in d.items():
        if x == '\t':
            result_file.write('\t\\t: ' + str(y) + '\n')
        elif x == '\n':
            result_file.write('\t\\n: ' + str(y) + '\n')
        else:
            result_file.write('\t' + str(x) + ': ' + str(y) + '\n')
    result_file.write('\n')

    el, h = entropy(d)

    result_file.write('Characters entropy:\n')
    for x, y in el.items():
        if x == '\t':
            result_file.write('\t\\t: ' + str(y) + '\n')
        elif x == '\n':
            result_file.write('\t\\n: ' + str(y) + '\n')
        else:
            result_file.write('\t' + str(x) + ': ' + str(y) + '\n')
    result_file.write('\n')

    result_file.write('H = ' + str(h))
    result_file.close()
    return 0


def count_letters(filename: str) -> (dict, int, int):
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        print('No file named: ' + filename)
        return -1
    txt = f.read()
    l = list(txt)
    wc = len(txt.split(' '))
    c = Counter(l)
    f.close()

    d = dict(c.most_common())
    return {x: y/len(l) for x, y in d.items()}, wc, len(l)


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
        res[x] = (code, int(code, 2))
        
        old_len = len(code)
        code = str(bin(int(code, 2) + 1))[2:]
        while old_len > len(code):
            code = '0' + code

    return res


d = {
    "A": 0.389,
    "B": 0.222,
    "C": 0.167,
    "D": 0.111,
    "E": 0.056,
    "F": 0.056
}
print(entropy(d))
code_len = calculate_code_len(d)
print(code_len)
print(create_code(code_len))
