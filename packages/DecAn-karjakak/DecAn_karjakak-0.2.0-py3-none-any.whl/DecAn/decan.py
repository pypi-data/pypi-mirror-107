# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import time
import os
import argparse
import json
import functools
from functools import partial
import re
import string
import pickle
import io
from GenPy import Fixstr
import concurrent.futures

"""
Snippet from:
https://docs.python.org/3/library/pickle.html
"""
class RestrictedUnpickler(pickle.Unpickler):
    """Restriction for running modules and functions"""
    
    def find_class(self, module, name):
        if module and name:
            raise pickle.UnpicklingError(f"{module}.{name} not allowed!!!")

def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    
    try:
        return RestrictedUnpickler(io.BytesIO(s)).load()
    except Exception as e:
        raise e

def timer(func):
    """
    Print the runtime of the decorated function
    https://realpython.com/primer-on-python-decorators
    """
    
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"\nFinished {func.__name__!r} in {run_time:.4f} secs\n")
        return(value)    
    return wrapper_timer

def reconst(text: str) -> dict:
    """Deconstruct by reconstruct the text."""
    
    sd = {i: text.count(i) for i in tuple(set(text))}
    try:
        for i in tuple(sd):
            if i in string.punctuation:
                regex = re.compile(rf'\{i}')
            else:
                regex = re.compile(rf'{i}')
            gt = tuple(j.span()[0] for j in regex.finditer(text))
            sd[i] = gt
            text = text.replace(i, '')
            del gt
        return sd
    except Exception as e:
        raise e

def lookwd(text: str, alp: str) -> tuple:
    """Looking for an alphabet or a words positions."""
    
    try:
        if alp in text:
            regex = re.compile(rf'{alp}')
            if len(alp) > 1:
                pos = tuple(i.span() for i in regex.finditer(text))
            else:
                pos = tuple(i.span()[0] for i in regex.finditer(text))
            del text, regex
            return alp, pos
        else:
            del text
            return alp, None
    except Exception as e:
        raise e
    
@timer
def deconstruct(text: str, filename: str, path: str):
    """To deconstruct a text file or sentences to json."""
    
    if os.path.isfile(text):
        if text.rpartition('.')[2] == 'txt':
            with open(text) as rd:
                text = rd.read()
        else:
            raise Exception('Cannot read non-.txt file!!!')
    text = Fixstr(text).fixingfs(False)
    dics = reconst(text)
    if os.path.isdir(path) and filename.rpartition('.')[2] == 'pickle':
        with open(os.path.join(path, filename), 'wb') as dc:
            pickle.dump(dics, dc)
    elif os.path.isdir(path) and filename.rpartition('.')[2] == 'json':
        with open(os.path.join(path, filename), 'w') as dc:
            json.dump(dics, dc)
    else:
        raise Exception('Be specific on file extension, either ".json", or ".pickle"!!!')
    del dics, text, filename, path


@timer
def construct(file: str) -> str:
    """To construct back the deconstruct text that saved in json file."""
    
    rd = None
    if os.path.isfile(file) and file.rpartition('.')[2] == 'pickle':
        with open(file, 'rb') as rjs:
            rd = restricted_loads(rjs.read())
    elif os.path.isfile(file) and file.rpartition('.')[2] == 'json':
        with open(file) as rjs:
            rd = json.load(rjs)        
    else:
        raise Exception('Either file not exist or file is not .pickle/.json!!!')
    if rd:
        try:
            strng = ''
            for i in list(rd)[::-1]:
                for j in rd[i]:
                    strng = f'{strng[:j]}{i}{strng[j:]}'
                del rd[i]
            return strng
        except:
            raise Exception('WARNING-ERROR: Please choose a deconstructed file!!!')

def prres(txts: str, ch: str, n: tuple):
    """Printing the results from Analyze."""
    
    regex = re.compile(r"\S?\w+\S+")
    dics = {}
    if n:
        dics = dics | {ch: {len(n): n}}
        del n
        if len(ch) > 1:
            print(f'"{ch}": {dics[ch]}')
            print(f'"{ch}" is {len(dics[ch][list(dics[ch])[0]])} out of total {len(tuple(regex.finditer(txts)))} words!\n')
            del dics[ch]
        else:
            print(f'{repr(ch)}: {dics[ch]}')
            print(f'{repr(ch)} is {len(dics[ch][list(dics[ch])[0]])} out of total {len(txts)} chars!\n')
            del dics[ch]
    else:
        print(f'No such word {repr(ch)} in text!!!')
    del txts, dics, regex

@timer
def textsortchrs(txts: str, alph: list = None, tm: bool = False):
    """
    Doing analysis of finding each char or words for their position in text.
    * References:
    * https://stackoverflow.com/questions/26184100/
    * how-does-v-differ-from-x0b-or-x0c
    * https://stackoverflow.com/questions/6785226/
    * pass-multiple-parameters-to-concurrent-futures-executor-map
    * \v == VT [vertical tab (\x0b)]
    * \f == FF [form feed (\x0c)]
    * In string.printable appearing "\x0b" and "\x0c"
    """    
    if os.path.isfile(txts):
        if txts.rpartition('.')[2] == 'txt':
            with open(txts) as rd:
                txts = rd.read()
        else:
            raise Exception('Cannot read non-.txt file!!!')
    txts = Fixstr(txts).fixingfs(False)
    try:
        if isinstance(alph, list):
            if tm:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    for result in executor.map(partial(lookwd, txts), alph):
                        i, gtp = result
                        prres(txts, i, gtp)
                        del i, gtp, result
            else:
                for i in alph:
                    i, gtp = lookwd(txts, i)
                    prres(txts, i, gtp)
                    del i, gtp
            del txts, alph
        else:
            alph = dict(sorted(reconst(txts).items(), key = lambda k: len(k[1]), reverse = True))
            once = tuple()
            maxi = ('', 0)
            space = 0
            asci = tuple()
            punct = tuple()
            digi = tuple()
            uni = tuple()
            pri = tuple()
            for i, j in alph.items():
                print(f'{repr(i)}: sub-total: {len(j)}')
                if len(j) == 1:
                    once += (i,)
                if len(j) >= maxi[-1] and i not in ['\n','\t','\r','\v','\f', ' ']:
                    if maxi[0] == '':
                        maxi = (i, len(j))
                    else:
                        maxi = maxi[:-1] + (i,) + (maxi[-1],)
                if i in ['\n','\t','\r','\v','\f', ' ']:
                    space += len(j)
                    pri += (i,)
                elif i in string.ascii_letters:
                    asci += (i,)
                elif i in string.digits:
                    digi += (i,)
                elif i in string.punctuation:
                    punct += (i,)            
                else:
                    uni += (i,)
            del alph
            print(f'Total of {len(txts)} chars.')
            print(f'Total of {len(txts)-space} chars, exclude space and printable.')
            print(f'Space and printable occured {space} in the text.')
            print(f'Chars that occur once in text: {", ".join(repr(i) for i in once)}.')
            if len(maxi) > 2:
                print(f'Chars that used most in text: [{", ".join(sorted(repr(i) for i in maxi[:-1]))}], {maxi[-1]} occurences.')
            else:
                print(f'Char that used most in text: {repr(maxi[0])}, {maxi[1]} occurences.')
            print(f"Construction of the text's chars:\n")
            print(f"- ASCII letters: [{', '.join(sorted(repr(i) for i in asci))}].\n")
            print(f"- Unicode letters: [{', '.join(sorted(repr(i) for i in uni))}].\n")
            print(f"- Numerical: [{', '.join(sorted(repr(i) for i in digi))}].\n")
            print(f"- Punctuation: [{', '.join(sorted(repr(i) for i in punct))}].\n")
            print(f"- Printable: [{', '.join(sorted(repr(i) for i in pri))}].")
            del once, maxi, space, asci, punct, uni, digi, pri, txts
    except Exception as e:
        raise e
    
def fixedsaving(text: str, path: str, name: str):
    """Saving text that has been fixed to a new file."""
    
    if os.path.isfile(text):
        if text.rpartition('.')[2] == 'txt':
            with open(text) as rd:
                text = rd.read()
        else:
            raise Exception('Cannot read non-.txt file!!!')
    
    if os.path.isdir(path):
        path = os.path.join(path, name := name if name.rpartition('.')[2] == 'txt' else f'{name}.txt')
        Fixstr(text).savefix(path)
        print(f'file [{path}] has been created and saved!')
        del path
    else:
        raise Exception('Path need to be a directory!')
            
def main():
    parser = argparse.ArgumentParser(prog = 'DecAn',description = 'Analyze and Deconstruct words')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--deconstruct', type = str, nargs = 3, help = 'Save deconstruct as json file')
    group.add_argument('-c', '--construct', type = str, help = 'Construct back the deconstruct in json file')
    group.add_argument('-f', '--fix_saved', type = str, nargs = 3, help = 'Fixing text and saved to a new file.')
    parser.add_argument('-a', '--analyze', type = str, help = 'Analyzing chars in a text')
    parser.add_argument('-s', '--search', type = str, action = 'extend', nargs = '+', help = 'Search list [only use after "-a"]')
    parser.add_argument('-m', '--multi_threading', action = 'store_true', help = 'Activate multi-threading [only use after "-s"]')
    args = parser.parse_args()
    if args.analyze:
        if args.search:
            if args.multi_threading:
                textsortchrs(args.analyze, args.search, True)
            else:
                textsortchrs(args.analyze, args.search)
        else:
            textsortchrs(args.analyze)
    elif args.deconstruct:
        deconstruct(args.deconstruct[0], args.deconstruct[1], args.deconstruct[2])
    elif args.construct:
        print(construct(args.construct))
    elif args.fix_saved:
        fixedsaving(args.fix_saved[0], args.fix_saved[1], args.fix_saved[2])

if __name__ == '__main__':
    main()