"""
AA, February 2021
Assignment 3: Contagem dos Itens Mais Frequentes
Author: Ana Sofia Fernandes, 88739
"""

#Code adapted from the file "count_min_sketch.py" given by the professor
#
# Adapted from https://github.com/rafacarrascosa/countminsketch
#
# J. Madeira --- December 2018


import array

import hashlib

import math
from Reader.File_reader import File_reader
from collections import Counter 
import sys


class CountMinSketch(object):
    """
    A class for counting hashable items using the Count-min Sketch strategy.

    The Count-min Sketch is a randomized data structure that uses a constant
    amount of memory and has constant insertion and lookup times at the cost
    of an arbitrarily small overestimation of the counts.

    It has two parameters:
     - `m` the size of the hash tables, larger implies smaller overestimation
     - `d` the number of hash tables, larger implies lower probability of
           overestimation.

    Note that this class can be used to count *any* hashable type, so it's
    possible to "count apples" and then "ask for oranges". Validation is up to
    the user.
    """

    def __init__(self, file_to_read, m=None, d=None, delta=None, epsilon=None):
        """
        Parameters
        ----------
        m : the number of columns in the count matrix
        d : the number of rows in the count matrix
        delta : (not applicable if m and d are supplied) the probability of query error
        epsilon : (not applicable if w and d are supplied) the query error factor
        """
        self.file_reader = File_reader(file_to_read)
        self.char_counting_dict = {}
        if m is not None and d is not None:
            self.m = m
            self.d = d
        elif delta is not None and epsilon is not None:
            # Computing the size of the sketch
            self.m = math.ceil(2.0 / epsilon)
            self.d = math.ceil(math.log(1.0 / delta))
        else:
            raise ValueError( "You must either supply both m and d or delta and epsilon.")

        #print("CM Sketch with " + str(self.m) + " columns and " + str(self.d) + " rows")

        self.n = 0

        self.tables = []
        for _ in range(self.d):
            table = array.array("l", (0 for _ in range(self.m)))   # signed long integers
            self.tables.append(table)

    def _hash(self, x, hash_func='md5'):
        #['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']
        assert type(hash_func)==str
        if hash_func == 'md5':
            md5 = hashlib.md5(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
            for i in range(self.d):
                md5.update(str(i).encode("utf-8"))              # concatenate
                yield int(md5.hexdigest(), 16) % self.m
        elif hash_func == 'sha256':
            sha256 = hashlib.sha256(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
            for i in range(self.d):
                sha256.update(str(i).encode("utf-8"))              # concatenate
                yield int(sha256.hexdigest(), 16) % self.m
        elif hash_func == 'sha1':
            sha1 = hashlib.sha1(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
            for i in range(self.d):
                sha1.update(str(i).encode("utf-8"))              # concatenate
                yield int(sha1.hexdigest(), 16) % self.m
        elif hash_func == 'blake2s':
            blake2s = hashlib.blake2s(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
            for i in range(self.d):
                blake2s.update(str(i).encode("utf-8"))              # concatenate
                yield int(blake2s.hexdigest(), 16) % self.m
        elif hash_func == 'dsaEncryption':
            dsaEncryption = hashlib.blake2s(str(hash(x)).encode("utf-8"))     # handle bytes, not strings
            for i in range(self.d):
                dsaEncryption.update(str(i).encode("utf-8"))              # concatenate
                yield int(dsaEncryption.hexdigest(), 16) % self.m
        else:
            print("INVALID HASH FUNCTION "+hash_func+" !")
            print("Please use ['md5', 'sha256', 'sha1', 'blake2s', 'dsaEncryption']")
            sys.exit()

    def update(self, x, value=1, hash='md5'):
        """
        Count element `x` as if had appeared `value` times.
        By default `value=1` so:

            sketch.add(x)

        Effectively counts `x` as occurring once.
        """
        self.n += value
        for table, i in zip(self.tables, self._hash(x, hash_func=hash)):
            table[i] += value

    def query(self, x):
        """
        Return an estimation of the amount of times `x` has ocurred.
        The returned value always overestimates the real value.
        """
        return min(table[i] for table, i in zip(self.tables, self._hash(x)))

    def __getitem__(self, x):
        """
        A convenience method to call `query`.
        """
        return self.query(x)

    def __len__(self):
        """
        The number of things counted. Takes into account that the `value`
        argument of `add` might be different from 1.
        """
        return self.n

    def count_chars(self, exact_counter_result, hash_function='md5'):
        """
        Counts the occurence of each char in a given file and saves it in
        a dictionary. The couting is made with an exact counter.
        """
        self.file_reader.read_file()
        chars = self.file_reader.get_final_chars()
        for w in chars:
            self.update(w, hash=hash_function)
        
        for char, counting in exact_counter_result.items():
            self.char_counting_dict[char] = self.query(char)
        
        self.char_counting_dict = {k: v for k, v in sorted(self.char_counting_dict.items(), key=lambda item: item[1], reverse=True)}

    def get_final_counting(self):
        """
        Getter for the dictionary with the final counting
        """
        return self.char_counting_dict

    def get_top_20_chars(self):
        """
        Getter for the most 20 counted chars
        """
        k = Counter(self.char_counting_dict) 
        return k.most_common(20)

    def get_total_counted_chars(self):
        """
        Getter for all chars counted by count min sketch
        """
        return sum(self.char_counting_dict.values())
    
    def clear(self):
        self.char_counting_dict.clear()