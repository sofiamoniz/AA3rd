"""
AA, February 2021
Assignment 3: Contagem dos Itens Mais Frequentes
Author: Ana Sofia Fernandes, 88739
"""

from Reader.File_reader import File_reader
from collections import Counter 
import time
from tabulate import tabulate

##Class that acts as an exact counter and counts the occurences of each char in file

class Exact_counter:

    def __init__(self, file_to_read):
        self.char_counting_dict = {}
        self.file_reader = File_reader(file_to_read)
        self.execution_time = 0

    def count_chars(self):
        """
        Counts the occurence of each char in a given file and saves it in
        a dictionary. The couting is made with an exact counter.
        """
        self.file_reader.read_file()
        chars = self.file_reader.get_final_chars()
        start_time = time.time()
        for w in chars:
            if w not in self.char_counting_dict:
                self.char_counting_dict[w] = 1
            else:
                self.char_counting_dict[w] += 1
        self.execution_time = time.time() - start_time
        self.char_counting_dict = {k: v for k, v in sorted(self.char_counting_dict.items(), key=lambda item: item[1], reverse=True)}

    def write_final_counting(self, output_file):
        """
        Write in file the final counting for exact counter, in descending order
        """
        with open(output_file,"w") as file:
            file.write("\nNumber of chars counted: "+ str(len(self.char_counting_dict.keys()))+"\n")
            file.write("\nFinal char counting:\n")
            for char in self.char_counting_dict:
                file.write("\n"+char+" -> "+str(self.char_counting_dict[char]))        

    def write_top_20_chars(self, output_file):
        """
        Write in file the top 20 chars
        """
        high = self.get_top_20_chars()
        with open(output_file,"w") as output:
            output.write("--- Top 20 chars - exact counter:  " )
            for i in high:
                output.write("\n"+str(i[0])+" -> "+str(i[1]))

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
        Getter for all chars counted by exact counter
        """
        return sum(self.char_counting_dict.values())

    def get_execution_time(self):
        """
        Getter for execution time
        """
        return round(self.execution_time,3)