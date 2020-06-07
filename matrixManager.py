#!/usr/bin/env python
#! -*- encoding: utf-8 -*-

import numpy as np

class MatrixManager():

    def __init__(self, matrix):
        self.m_matrix = matrix


    def matrix(self):
        return self.m_matrix


    def rightHand(self):
        return self.m_matrix[:,21:]


    def leftHand(self):
        return self.m_matrix[:,:21]

    
    def frames(self):
        return self.m_matrix.shape[0]
        
    
    def numElems(self):
        elems = self.m_matrix.shape
        elems = elems[0] * elems[1]
        return elems

    #No funciona
    def isOneHand(self):
        left = self.leftHand()
        sum_ = np.sum(left)
        elems = left.shape
        elems = elems[0] * elems[1]
        average = sum_/elems
        #print(average)
        return average

    
    def selectHand(self, hand):
        if(hand == 1):
            return self.rightHand()
        elif(hand == 0):
            return self.leftHand()
        else:
            print("Hand must be right (1) or left (0)")
            return self.m_matrix

    
    def selectFrame(self, frame):
        return self.m_matrix[frame,:]


    #finger:
    #0 thumn, 1 index, 2 middle, 3 ring, 4 pinky
    def fingerDirection(self, hand, finger, frame):
        matrix = self.selectHand(hand)

        columnX = 6 + finger * 3
        columnY = columnX + 1
        columnZ = columnY + 1

        dirX = matrix[frame, columnX]
        dirY = matrix[frame, columnY]
        dirZ = matrix[frame, columnZ]

        return np.array([dirX, dirY, dirZ])


    def handDirection(self, hand, frame):
        matrix = self.selectHand(hand)

        dirX = matrix[frame, 0]
        dirY = matrix[frame, 1]
        dirZ = matrix[frame, 2]

        return np.array([dirX, dirY, dirZ])


    def handRotation(self, hand, frame):
        matrix = self.selectHand(hand)

        pitch = matrix[frame, 3]
        roll = matrix[frame, 4]
        yaw = matrix[frame, 5]

        return np.array([pitch, roll, yaw])