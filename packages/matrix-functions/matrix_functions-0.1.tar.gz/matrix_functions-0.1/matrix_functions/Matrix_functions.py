# -*- coding: utf-8 -*-
"""
Created on Mon May 24 22:27:16 2021

Matrix class
Init() creates a matrix object with empty list

str() prints out matrix

add() adds two matrix objects i.e., A + B

sub () subtracts two matrix objects i.e., A - B

To Do: add multiplication, matrix fill at object creation, error function


@author: Christopher Phillips
"""

class Matrix:

    def __init__(self, list):
        # initiate empty matrix list
        # accept 
        self.list = list


    def __str__(self):
        # print method for matrix output.
        # creates square matrix like output
        new_matrix ='\n'.join([' '.join([str(item) for item in row]) \
                               for row in self.list])
        return new_matrix + '\n'
    
    
    def __add__(self, other):
        # define matrix addition
        # does not currentlycheck if both matrix objects are the same dimentions.
        
        # checks if object is a matrix object with numbers and not strings
        if isinstance(other, (int, float)):
            return Matrix([[other + ent for ent in row] for row in self.list])    
        # create empty temporary list
        endlist = []

        # matrix addition
        for row, otherrow in zip(self.list, other.list):
            newrow = []

            for value, othervalue in zip(row, otherrow):
                newrow.append(value + othervalue)

            endlist.append(newrow)

        sum = Matrix(endlist)

        return sum

    def __sub__(self, other):  # define matrix subtraction
        # define matrix subtraction
        # does not currentlycheck if both matrix objects are the same dimentions.
        
        # checks if object is a matrix object with numbers and not strings
        if isinstance(other, (int, float)):
            return Matrix([[other + ent for ent in row] for row in self.list]) 

        # create empty temporary list
        endlist = []

        # matrix subtraction
        for row, otherrow in zip(self.list, other.list):
            newrow = []

            for value, othervalue in zip(row, otherrow):
                newrow.append(value - othervalue)

            endlist.append(newrow)

        sub = Matrix(endlist)

        return sub