#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import sys
import argparse
import math
import numpy as np
from colorama import init, Fore, Back, Style
from reader import Reader
from calculator import Calculator
from evaluator import Evaluator
from matrixManager import MatrixManager


class Launcher():

    def __init__(self):
        self.m_reader1 = Reader()
        self.m_reader2 = Reader()
        self.m_evaluator = Evaluator()
        self.m_calculator = None

    
    def updateCalculator(self, i, length):
        if (i != 1):
            self.m_calculator.setFirst(False)
        if (i == length - 1):
            self.m_calculator.setLast(True)
        if (args.points != 0):
            self.m_calculator.setPoints(args.points)
        if (args.rep != None):
            self.m_calculator.setRest(args.rep)
            if (args.rep != "fix" and args.n < 15):
                self.m_calculator.setN(15)
            else:
                self.m_calculator.setN(args.n)


    def launch(self, words, length, path="", withnum=False):
        names = []
        wordI = words[0]
        if (withnum):
            name = self.m_reader1.readWithNum(wordI, v=args.verbose)
        else:
            name = self.m_reader1.read(wordI, v=args.verbose)
        names.append(name)
        matrixI = self.m_reader1.initialize()
        matrixResult = []

        for i in range(1, length):
            wordF = words[i]
            if (withnum):
                name = self.m_reader2.readWithNum(wordF, v=args.verbose)
            else:
                name = self.m_reader2.read(wordF, v=args.verbose)
            names.append(name)
            matrixF = self.m_reader2.initialize()

            self.m_calculator = Calculator(matrixI, matrixF)
            self.updateCalculator(i, length)
            expMatrix = self.m_calculator.resolve()

            matrixResult.append(expMatrix)
            self.m_evaluator.addSentenceWord(wordI)

            wordI = wordF
            matrixI = matrixF

        expMatrix = np.concatenate(matrixResult, axis = 0)
        self.m_evaluator.addSentenceWord(wordF)

        fileName = self.m_evaluator.getSentenceFile()
        if (args.verbose):
            print("Generated sentence file %s " %fileName)
        p = "GENERATED\ "
        Reader().write(p[:-1], fileName, expMatrix)
        print(fileName)
        d = Calculator([[]], [[]]).getDistances(MatrixManager(expMatrix))
        return names, d


    def launchEvaluate(self, words, length, path="", withnum=False):
        wordI = words[0]
        for i in range(1, length):
            wordF = words[i]
            self.m_evaluator.addSentenceWord(wordI)
            wordI = wordF

        self.m_evaluator.addSentenceWord(wordF)
        self.m_evaluator.initialize()
        d = Calculator([[]], [[]]).getDistances(MatrixManager(self.m_evaluator.m_test_matrix))
        return d

    
    def generateAllSentences(self, path=""):
        #sentences = Reader().readAllSentences("")
        sentences = Reader().readAllSentencesFileText()
        distMax = []
        distMin = []
        namesL = []
        for i in range(len(sentences)):
            names, d = self.launch(sentences[i], len(sentences[i]), withnum=True)
            namesL.append(names)
            distMax.append(max(d))
            distMin.append(min(d))
        mx = max(distMax)
        mn = min(distMax)
        av = sum(distMax) / len(distMax)
        print(mx, mn, av)
        #Reader().writeList(namesL)


    def generateAllSentencesRandom(self, path=""):
        sentences = Reader().readAllSentences("")
        distMax = []
        distMin = []
        for i in range(len(sentences)):
            _, d = self.launch(sentences[i], len(sentences[i]))
            distMax.append(max(d))
            distMin.append(min(d))
        mx = max(distMax)
        mn = min(distMax)
        av = sum(distMax) / len(distMax)
        print(mx, mn, av)

    
    def generateAllSentencesEvaluate(self, path=""):
        sentences = Reader().readAllSentences("")
        distMax = []
        distMin = []
        for i in range(len(sentences)):
            d = self.launchEvaluate(sentences[i], len(sentences[i]))
            _, dExtra = self.launch(sentences[i], len(sentences[i]))
            print(max(d), max(dExtra))
            distMax.append(max(d))
            distMin.append(min(d))
        mx = max(distMax)
        mn = min(distMax)
        av = sum(distMax) / len(distMax)
        print(mx, mn, av)


    def generateAllWords(self, path=""):
        init()
        distM, distMin, distMeans = [], [], []
        words = Reader().readAllWords()
        r = 5
        if (args.rep == None):
            args.rep = "dual"
            args.n = 15
        elif (args.rep == "fix"):
            r = args.n
        elif (args.rep != "fix" and args.n < 15):
            args.n = 15

        for t in range(5, r+5, 5):
            countI, countF, countT = 0, 0, 0
            countMI, countMF, countMT = 0, 0, 0
            for i in range(len(words)):
                self.m_reader1.readWithNum(words[i], v=args.verbose)
                m = self.m_reader1.initialize()
                self.m_calculator = Calculator([[]], [[]])
                self.updateCalculator(0, 0)
                m = MatrixManager(m)
                count0, count1, count2, count3, count4, count5, dist = self.m_calculator.wordTest(m, thr=t)
                countI = countI + count0
                countF = countF + count1
                countT = countT + count2

                countMI = countMI + count3
                countMF = countMF + count4
                countMT = countMT + count5

                distM.append(max(dist))
                distMin.append(min(dist))
                distMeans.append(sum(dist)/len(dist))
            print(" ")
            print("----------------------------------------")
            print(Fore.GREEN)
            if (args.rep == "fix"):
                print("Umbral:", t, "% Del máximo")
            elif (args.rep == "ind"):
                print("Umbral: 5 -", args.n, "% variable individual del máximo.")
            elif (args.rep == "dual"):
                print("Umbral: 5 -", args.n, "% variable dual del máximo.")
            print("Total palabras", len(words))
            print(Style.RESET_ALL)
            print("Palabras sin reposo inicial", Fore.WHITE+str(countI)+Style.RESET_ALL)
            print("% Sin reposo inicial", Fore.WHITE+str(round((countI * 100) / len(words),2)), "%"+Style.RESET_ALL)
            print("Palabras sin reposo final", Fore.WHITE+str(countF)+Style.RESET_ALL)
            print("% Sin reposo final", Fore.WHITE+str(round((countF * 100) / len(words),2)), "%"+Style.RESET_ALL)
            print("Palabras sin ambos reposos", Fore.WHITE+str(countT)+Style.RESET_ALL)
            print("% Sin reposo ambos reposos", Fore.WHITE+str(round((countT * 100) / len(words),2)), "%"+Style.RESET_ALL)
            print(" ")
            print("Palabras con excesivo reposo inicial", Fore.WHITE+str(countMI)+Style.RESET_ALL)
            print("% Exceso reposo inicial", Fore.WHITE+str(round((countMI * 100) / len(words),2)), "%"+Style.RESET_ALL)
            print("Palabras con excesivo reposo final", Fore.WHITE+str(countMF)+Style.RESET_ALL)
            print("% Exceso reposo final", Fore.WHITE+str(round((countMF * 100) / len(words),2)), "%"+Style.RESET_ALL)
            print("Palabras con excesivo reposo total", Fore.WHITE+str(countMT)+Style.RESET_ALL)
            print("% Exceso reposo total", Fore.WHITE+str(round((countMT * 100) / len(words),2)), "%"+Style.RESET_ALL)
        print(max(distM), min(distMin), sum(distMeans)/len(distMeans))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generation of synthetic phrases in sign language.')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-a', '--allWords', dest='allWords', action='store_true', default=False, 
                    help='Generate repose statistics for all words.')

    group.add_argument('-s', '--allSentences', dest='allSentences', action='store_true', default=False, 
                    help='Generate all sentences.')

    group.add_argument('-t', '--allSentTest', dest='allSentencesT', action='store_true', default=False, 
                    help='Generate all the sentences from a text file.')

    group.add_argument('-e', '--sentenceEv', dest='sentenceEv', action='store_true', default=False, 
                    help='Generate stats for all real sentences.')

    group.add_argument('-w', dest='words', action='store', type=str, nargs='+', 
                    help='Generate this phrase.')

    parser.add_argument('-p', dest='points', action='store', type=int, default=0, choices=[1, 2, 3, 4, 5, 6],
                        help='Number of points to interpolate (3, 6).')

    parser.add_argument('-r', dest='rep', action='store', type=str, choices=["fix", "dual", "ind"],
                        help='Select the method to calculate the repose: fix, dual or individual. Need parameter -n.')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help='Increase output verbosity.')
    
    parser.add_argument('-n', dest='n', action='store', type=int, choices=[5, 10, 15, 20], 
                        help='Number of repose. Fix between 5-20, otherwise 15 or 20.')
      
    args = parser.parse_args()


    if (args.rep != None and args.n == None):
        parser.error("Need parameter -n.")
    elif (args.rep == None and args.n != None):
        print("WARNING: Ignoring parameter -n.")
        print("\n")
    if (args.allWords):
        Launcher().generateAllWords()
    elif (args.allSentences):
        Launcher().generateAllSentencesRandom()
    elif (args.allSentencesT):
        Launcher().generateAllSentences()
    elif (args.sentenceEv):
        Launcher().generateAllSentencesEvaluate()
    elif (args.words != None and len(args.words) >= 2):
        Launcher().launch(args.words, len(args.words))
    else:
        parser.error("Must be two words at least.")

    sys.exit()