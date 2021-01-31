"""
AA, February 2021
Assignment 3: Contagem dos Itens Mais Frequentes
Author: Ana Sofia Fernandes, 88739
"""

##Class that reads a file and returns a list with all the words present

class File_reader:
    
    def __init__(self, file_to_read):
        self.file_to_read = file_to_read
        self.final_words = []
        self.final_chars = []

    def read_file(self):
        """
        Read words from file - only saves a word if it is >3 (so that we can avoid words like "a", "the", etc.)
        and if it doesn't contain pontuation (is alpha)
        """
        with open(self.file_to_read,"r") as file:
            for line in file:
                for word in line.split():
                    if len(word)>3 and word.isalpha():
                        self.final_words.append(word.lower())
    
    def get_final_words(self):
        """
        Getter for the final readen words
        """
        return self.final_words

    def get_final_chars(self):
        for word in self.final_words:
            for char in word:
                self.final_chars.append(char)
        return self.final_chars
