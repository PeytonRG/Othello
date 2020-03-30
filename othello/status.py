'''
    Created on March 28, 2020
    Last Modified March 28, 2020
    @author: Peyton Gasink
'''
import hashlib
import math
from othello import parmValidation

def _status(inputDictionary):
    errorList = []
    
    light = parmValidation._validateLight(inputDictionary, errorList)
    
    dark = parmValidation._validateDark(inputDictionary, errorList)
    
    blank = parmValidation._validateBlank(inputDictionary, errorList)
        
    board = inputDictionary["board"] #parmValidation._validateBoard(inputDictionary, errorList)
     
    integrity = inputDictionary["integrity"] #parmValidation._validateIntegrity(inputDictionary, errorList)
           
    parmValidation._validateUnqiueLightDarkBlankValues(light, dark, blank, errorList)
        
    if len(errorList) > 0:
        return {"status": "error: " + errorList[0]}
    
    result = {'status': 'ok'}
    return result

def _getPossibleMoveCount(board, light, dark, blank):
    possibleLightMoves = 0
    possibleDarkMoves = 0
    
    for position, token in enumerate(board):
        if token != blank: 
            if token == dark:
                possibleDarkMoves += _calculateMoveCount(dark, position, board, light, dark, blank)
            elif token == light:
                possibleLightMoves += _calculateMoveCount(light, position, board, light, dark, blank)
    result = {
        "light": possibleLightMoves,
        "dark": possibleDarkMoves
        }
    return result

def _calculateMoveCount(lightOrDark, position, board, light, dark, blank):
    length = len(board)
    elementsInRow = int(math.sqrt(length))
    possibleMoves = 0
    oppositeToken = dark if lightOrDark == light else light
    
    # get the row of this token to compare with the tokens that surround it
    # by dividing the first position in the row by the number of elements in a row
    firstIndexInRow = position - position % elementsInRow
    lastIndexInRow = firstIndexInRow + elementsInRow - 1
    rowNum = int(firstIndexInRow / elementsInRow)
    try:
        indexOfLeftAdjacent = position - 1
        while (firstIndexInRow <= indexOfLeftAdjacent 
               and indexOfLeftAdjacent > 0):
            tokenLeft = board[indexOfLeftAdjacent]
            if tokenLeft == oppositeToken and board[indexOfLeftAdjacent - 1] == blank:
                possibleMoves += 1
                break
            else:
                indexOfLeftAdjacent -= 1
    except IndexError:
        pass
    
    try:
        indexOfRightAdjacent = position + 1
        while (lastIndexInRow >= indexOfRightAdjacent 
               and indexOfRightAdjacent < len(board) - 1):
            tokenRight = board[indexOfRightAdjacent]
            if tokenRight == oppositeToken and board[indexOfRightAdjacent + 1] == blank:
                possibleMoves += 1
                break
            else:
                indexOfRightAdjacent += 1
    except IndexError:
        pass
    
    try:
        indexOfAboveAdjacent = position - elementsInRow
        while indexOfAboveAdjacent > 0:
            tokenAbove = board[indexOfAboveAdjacent]
            if tokenAbove == oppositeToken and board[indexOfAboveAdjacent - elementsInRow] == blank:
                possibleMoves += 1
                break
            else:
                indexOfAboveAdjacent -= elementsInRow
    except IndexError:
        pass
    
    try:
        indexOfBelowAdjacent = position + elementsInRow
        while indexOfBelowAdjacent < len(board) - 1:
            tokenBelow = board[indexOfBelowAdjacent]
            if tokenBelow == oppositeToken and board[indexOfBelowAdjacent + elementsInRow] == blank:
                possibleMoves += 1
                break
            else:
                indexOfBelowAdjacent += elementsInRow
    except IndexError:
        pass
    
    try:
        indexOfAboveLeftAdjacent = position - elementsInRow - 1
        while indexOfAboveLeftAdjacent > 0:
            tokenAboveLeft = board[indexOfAboveLeftAdjacent]
            if tokenAboveLeft == oppositeToken and board[indexOfAboveLeftAdjacent - elementsInRow - 1] == blank:
                possibleMoves += 1
                break
            else:
                indexOfAboveLeftAdjacent -= (elementsInRow + 1)
    except IndexError:
        pass
    
    try:
        indexOfAboveRightAdjacent = position - elementsInRow + 1
        while indexOfAboveRightAdjacent > 0:
            tokenAboveRight = board[indexOfAboveRightAdjacent]
            if tokenAboveRight == oppositeToken and board[indexOfAboveRightAdjacent - elementsInRow + 1] == blank:
                possibleMoves += 1
                break
            else:
                indexOfAboveRightAdjacent -= (elementsInRow - 1)
    except IndexError:
        pass
    
    try:
        indexOfBelowLeftAdjacent = position + elementsInRow - 1
        while indexOfBelowLeftAdjacent < len(board) - 1:
            tokenBelowLeft = board[indexOfBelowLeftAdjacent]
            if tokenBelowLeft == oppositeToken and board[indexOfBelowLeftAdjacent + elementsInRow - 1] == blank:
                possibleMoves += 1
                break
            else:
                indexOfBelowLeftAdjacent += (elementsInRow + 1)
    except IndexError:
        pass
    
    try:
        indexOfBelowRightAdjacent = position + elementsInRow + 1
        while indexOfBelowRightAdjacent < len(board) - 1:
            tokenBelowRight = board[indexOfBelowRightAdjacent]
            if tokenBelowRight == oppositeToken and board[indexOfBelowRightAdjacent + elementsInRow + 1] == blank:
                possibleMoves += 1
                break
            else:
                indexOfBelowRightAdjacent += (elementsInRow - 1)
    except IndexError:
        pass
    return possibleMoves

def _getRowFromBoard(rowNum, board):
    elementsInRow = int(math.sqrt(len(board)))
    row = board[(elementsInRow * rowNum):(elementsInRow * rowNum + elementsInRow)]
    return row