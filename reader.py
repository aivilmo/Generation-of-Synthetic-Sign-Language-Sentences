#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import sys
import os
import numpy as np
from unipath import Path
from random import randint
from matrixManager import MatrixManager

class Reader():

    def __init__(self):
        self.m_word = None


    def word(self):
        return self.m_word


    def read(self, file, path="", v=False):
        #PRUEBAS
        if (path == ""):
            path = "..\datos\modificados\palabras\ "
            path = path[:-1]
        #--------
        name = file + str(randint(1, 40)) + ".txt"
        file_ = path + name
        f = Path(file_)
        if (f.exists()):
            f = open(file_, "r")
            content = f.read()
            self.m_word = content.split()
            if (v):
                print("Reading file %s" %file_)
            return name
        else:
            print("File %s not exist" % file_)
            sys.exit()

    
    def readWithNum(self, file, path="", v=False):
        #PRUEBAS
        if (path == ""):
            path = "..\datos\modificados\palabras\ "
            path = path[:-1]
        #--------
        name = file + ".txt"
        file_ = path + name
        f = Path(file_)
        if (f.exists()):
            f = open(file_, "r")
            content = f.read()
            self.m_word = content.split()
            if (v):
                print("Reading file %s" %file_)
            return name
        else:
            print("File %s not exist" % file_)
            sys.exit()
    

    def write(self, directory, file, matrix):
        if (not os.path.exists(directory)):
            os.mkdir(directory)
        np.savetxt(directory + file, matrix, '%5f')


    def writeList(self, list_):
        with open("lista.txt", 'a+') as f:
            for i in list_:
                for j in i:
                    f.write(j[:-4])
                    f.write(" ")
                f.write("\n")


    def initialize(self):
        columns = 42
        rows = (int)(len(self.m_word)/columns)
        matrix = np.zeros((rows, columns))
        row = 0
        col = -1
        cont = -1
        for number in self.m_word:
            if(cont < columns - 1):
                cont += 1
                col += 1
            else:
                cont = 0
                col = 0
                row += 1
            matrix[row] [col] = float(number)
        return matrix


    def readAllSentences(self, path):
        path = "..\datos\modificados\ "
        path = path[:-1] + "frases"
        numSentence = 0
        sentences = np.zeros((274),dtype=list)
        for _,_,files in os.walk(path):
            for filename in files:
                sentences[numSentence] = filename[:-4].split("_")
                numSentence += 1
        return sentences

    
    def readAllSentencesFileText(self):
        sentences = []
        with open("lista.txt", 'r') as f:
            for line in f:
                sentences.append(line.split(" ")[:-1])
        return sentences


    def readAllWords(self, path=""):
        path = "..\datos\modificados\ "
        path = path[:-1] + "palabras"
        numword = 0
        words = np.zeros((3680),dtype=list)
        for _,_,files in os.walk(path):
            for filename in files:
                words[numword] = filename[:-4]
                numword += 1
        return words

        
