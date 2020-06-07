#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt  
from scipy.interpolate import RegularGridInterpolator
from numpy import linspace, zeros, array
from reader import Reader


class Evaluator():

    def __init__(self):
        self.m_words = []
        self.m_reader = Reader()
        self.m_test_matrix = None


    def initialize(self):
        test_sentence = self.getSentenceFile()
        path = "..\datos\modificados\ "
        path = path[:-1] + "frases\ "
        self.m_reader.readWithNum(test_sentence, path[:-1])
        self.m_test_matrix = self.m_reader.initialize()

    
    def getSentenceFile(self):
        name = self.m_words[0]
        for i in range(1, len(self.m_words)):
            word = self.m_words[i]
            name = name + "_" + word
        #name = name + "_GENERATED" + ".txt"
        self.m_words = []
        return name

    
    def cleanWord(self, word):
        last = len(word)-1
        numbers = "1 2 3 4 5 6 7 8 9"
        word = word[:last]
        if (word[last-1] in numbers):
            word = word[:last-1]
        return word

    
    def addSentenceWord(self, word):
        word = word.split(".")
        word = word[0]
        self.m_words.append(word)
    
