#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt  
import math
import numpy as np
import statistics
from random import random
from matrixManager import MatrixManager


class Calculator():

    def __init__(self, m1, m2):
        self.m_matrix1 = MatrixManager(m1)
        self.m_matrix2 = MatrixManager(m2)
        self.m_first = True
        self.m_last = False
        self.m_points = 3
        self.m_rest = "dual"
        self.m_n = 15

    
    def setPoints(self, p):
        self.m_points = p

    
    def setFirst(self, f):
        self.m_first = f


    def setLast(self, l):
        self.m_last = l


    def setRest(self, r):
        self.m_rest = r

    
    def setN(self, n):
        self.m_n = n


    def resolve(self):

        mI, mF = self.cleanMatrixes()

        finalFrame = self.framesCleanedMatrix(mI) - 1
        #self.setPointsInterpolate(mI[finalFrame], mF[0])
        mIntermediate = self.interpolateEquidistance(self.m_points, mI[finalFrame], mF[0])

        if (self.m_first):
            return np.concatenate((mI, mIntermediate, mF), axis = 0)
        return np.concatenate((mIntermediate, mF), axis = 0)


    def setPointsInterpolate(self, vectorI, vectorF):
        m = np.concatenate((np.asmatrix(vectorI), np.asmatrix(vectorF)), axis = 0)
        m = np.asmatrix(m)
        num = float(self.getDistances(MatrixManager(m))[0])
        if (num < 20):
            self.m_points = 3
        elif (num >= 20 and num < 40):
            self.m_points = 4
        elif (num >= 40 and num < 60):
            self.m_points = 5
        elif (num >= 60):
            self.m_points = 6

            
    def middleVector(self, vectorI, vectorF):
        middleVector = np.zeros(42)
        for i in range(41):
            middleVector[i] = (vectorI[i] + vectorF[i]) / 2
        return middleVector


    def euclideanDistance3D(self, point1, point2):
        x = pow(point1[0] - point2[0], 2)
        y = pow(point1[1] - point2[1], 2)
        z = pow(point1[2] - point2[2], 2)
        return math.sqrt(x + y + z)

    
    def getGesture(self, distances, thresholdInit = 10, thresholdFinal = 10, prints = False):
        thresholdInit, thresholdFinal = thresholdInit * 0.01, thresholdFinal * 0.01
        m = max(distances)
        repI, repF, gest = [], [], []
        for i in range(len(distances)):
            i = 0
            while (i<len(distances)-1 and distances[i] <thresholdInit*m):
                i += 1
            j = len(distances)-1
            while (j>1 and distances[j] < thresholdFinal*m):
                j -= 1
        for k in range(i):
            repI.append(distances[k])
        for k in range(i, j+1):
            gest.append(distances[k])
        for k in range(j+1, len(distances)):
            repF.append(distances[k])

        if (prints):
            print("RepI: ", repI)
            print("Gest: ", gest)
            print("RepF: ", repF)
            print(" ")
        return repI, gest, repF

    
    def getGestureDual(self, distances, is20):
        repI, gest, repF = self.getGesture(distances, 5, 5)
        if (len(repI) == 0 and len(repF) == 0):
            repI, gest, repF = self.getGesture(distances, 10, 10)
            if (len(repI) == 0 and len(repF) == 0):
                repI, gest, repF = self.getGesture(distances, 15, 15)
                if (len(repI) == 0 and len(repF) == 0 and is20):
                    repI, gest, repF = self.getGesture(distances, 20, 20)
        return repI, gest, repF

    #No esta en la memoria
    def getGestureIndividual2(self, distances):
        repI, gest, repF = self.getGesture(distances, 5, 5)
        if (len(repI) == 0 and len(repF) == 0):
            repI, gest, repF = self.getGesture(distances, 10, 10)
            if (len(repI) == 0 and len(repF) == 0):
                repI, gest, repF = self.getGesture(distances, 15, 15)
                if (len(repI) == 0 and len(repF) == 0):
                    repI, gest, repF = self.getGesture(distances, 20, 20)

        if (len(repI) == 0 and len(repF) != 0):
            repI, gest, repF = self.getGesture(distances, thresholdInit=10)
            if (len(repI) == 0 and len(repF) != 0):
                repI, gest, repF = self.getGesture(distances, thresholdInit=15)
                if (len(repI) == 0 and len(repF) != 0):
                    repI, gest, repF = self.getGesture(distances, thresholdInit=20)

        if (len(repF) == 0 and len(repI) != 0):
            repI, gest, repF = self.getGesture(distances, thresholdFinal=10)
            if (len(repF) == 0 and len(repI) != 0):
                repI, gest, repF = self.getGesture(distances, thresholdFinal=15)
                if (len(repF) == 0 and len(repI) != 0):
                    repI, gest, repF = self.getGesture(distances, thresholdFinal=20)
        
        return repI, gest, repF
 

    def getGestureIndividual(self, distances, limit = 15):
        ini, fin = 5, 5
        while (fin <= limit and ini <= limit):
            repI, gest, repF = self.getGesture(distances, ini, fin)
            if (len(repI) == 0 and len(repF) == 0):
                ini += 5
                fin += 5
                continue
            if (len(repI) == 0 and len(repF) != 0):
                ini += 5
                continue
            if (len(repF) == 0 and len(repI) != 0):
                fin += 5
                continue
            if (len(repI) != 0 and len(repF) != 0):
                break
        return repI, gest, repF

    
    def getDistances(self, matrix):
        frames = matrix.frames()
        pv = matrix.selectFrame(0)
        pv = np.squeeze(np.asarray(pv))
        distances = []
        for row in range(1, frames):
            d = 0
            cv = matrix.selectFrame(row)
            cv = np.squeeze(np.asarray(cv))
            for col in range(42):
                d = d + (pv[col]-cv[col])*(pv[col]-cv[col])
            distances.append(d)
            pv = matrix.selectFrame(row)
        return distances


    def cleanAll(self, matrix, repI, repF):
        rowsRepI, rowsRepF = len(repI), len(repF)
        rows = matrix.frames()
        m = matrix.matrix()
        return m[rowsRepI:rows-rowsRepF,:]

    
    def cleanFirst(self, repF):
        rowsRepF = len(repF)
        rows = self.m_matrix1.frames()
        m = self.m_matrix1.matrix()
        return m[0:rows-rowsRepF,:]


    def cleanLast(self, repI):
        rowsRepI = len(repI)
        m = self.m_matrix2.matrix()
        return m[rowsRepI:,:]


    def interpolateEquidistance(self, points, vectorI, vectorF):
        midpointsT = np.zeros((42, points))
        points = points + 2
        for i in range(41):
            values = np.linspace(vectorI[i], vectorF[i], num = points)   #valores intermedios de la columna i
            midpointsT[i] = values[1:-1] 
        return np.transpose(midpointsT)

    
    def interpolateRandom(self, points, vectorI, vectorF):
        midpoints = np.zeros((points, 42))
        for p in range(points):
            for i in range(41):
                midpoints[p][i] = np.random.uniform(vectorI[i], vectorF[i])
        return midpoints


    def interpolate3equidistancePoints(self, vectorI, vectorF):
        midpoints = np.zeros((3, 42))
        middle = self.middleVector(vectorI, vectorF)
        midpoints[0] = self.middleVector(vectorI, middle)
        midpoints[1] = middle
        midpoints[2] = self.middleVector(middle, vectorF)
        print(midpoints)
        return midpoints


    def cleanMatrixes(self):
        distI = self.getDistances(self.m_matrix1)
        distF = self.getDistances(self.m_matrix2)

        repII, _, repFI = self.getRest(distI)
        repIF, _, repFF = self.getRest(distF)

        if (self.m_first and self.m_last):
            return self.cleanFirst(repFI), self.cleanLast(repIF)
        if (self.m_first):
            return self.cleanFirst(repFI), self.cleanAll(self.m_matrix2, repIF, repFF)
        if (self.m_last): 
            return self.cleanAll(self.m_matrix1, repII, repFI), self.cleanLast(repIF)
        return self.cleanAll(self.m_matrix1, repII, repFI), self.cleanAll(self.m_matrix2, repIF, repFF)


    def wordTest(self, matrix, thr, prin = False):
        countI, countF, countTotal = 0, 0, 0
        countMI, countMF, countMTotal = 0, 0, 0
        dist = self.getDistances(matrix)

        repI, gest, repF = self.getRest(dist, thr)
        numDist = len(repI) + len(repF) + len(gest)
        if (prin):
                print("max ", mx)
                print("av ", av)
                print("stdev ", stdev)
                print("max / stdev ", mx / stdev)
                print("repI ", len(repI))
                print("gest ", len(gest))
                print("repF ", len(repF))
                print("---------------------------")
        if (len(repI) == 0):
            countI += 1
        if (len(repF) == 0):
            countF += 1
        if (len(repI) == 0 and len(repF) == 0):
            countTotal += 1

        if (len(repI) > int(numDist/3)):
            countMI += 1
        if (len(repF) > int(numDist/3)):
            countMF += 1
        if (len(repI) + len(repF) > int(numDist/6)):
            countMTotal += 1
        return countI, countF, countTotal, countMI, countMF, countMTotal, dist


    def getRest(self, dist, thr=5):
        if (self.m_rest == "fix"):
            return self.getGesture(dist, thr, thr)
        if (self.m_rest == "ind"):
            return self.getGestureIndividual(dist, self.m_n)
        if (self.m_rest == "dual"):
            if (self.m_n == 20):
                return self.getGestureDual(dist, True)
            else:
                return self.getGestureDual(dist, False)
    

    def average(self, distances):
        mx = max(distances)
        mn = min(distances)
        av = statistics.mean(distances)
        stdev = statistics.stdev(distances)
        return mx, mn, av, stdev


    def selectThreshold(self, maximum, stdev):
        umbral = maximum / stdev
        if (umbral >= 5.5):
            return 15
        elif (umbral >= 3 and umbral < 5.5):
            return 10
        else:
            return 5


    def framesCleanedMatrix(self, matrix):
        f = matrix.shape
        return f[0]


    def euclideanDistance42D(self, vectorIni, vectorEnd):
        sumatory = []
        for i in range(42):
            sumatory.append(pow(vectorIni[i] - vectorEnd[i], 2))
        sumator = sum(sumatory)
        return math.sqrt(sumator)


    def show(self):
        last_frame = self.m_matrix2.frames() - 1

        x = self.m_matrix1.fingerDirection(1, 0, 0)
        y = self.m_matrix2.fingerDirection(1, 0, last_frame)
        
        fig = plt.figure()
        cube = fig.add_subplot(projection='3d')

        cube.scatter(x[0], x[1], x[2], c='r', marker='o')
        cube.scatter(y[0], y[1], y[2], c='b', marker='o')

        cube.set_xlabel('X Axis')
        cube.set_ylabel('Y Axis')
        cube.set_zlabel('Z Axis')

        plt.show()
