'''
    Created on March 28, 2020
    Last Modified March 29, 2020
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
    
    parmValidation._validateUnqiueLightDarkBlankValues(light, dark, blank, errorList)
        
    board = parmValidation._validateBoard(inputDictionary, light, dark, blank, errorList)
     
    integrity = parmValidation._validateIntegrity(inputDictionary, light, dark, blank, board, errorList)
        
    if len(errorList) > 0:
        return {"status": "error: " + errorList[0]}
    
    possibleMoves = _getPossibleMoveCount(board, light, dark, blank)
    
    if possibleMoves["light"] > 0 and possibleMoves["dark"] > 0:
        result = {'status': 'ok'}
    elif possibleMoves["light"] > 0:
        result = {'status': 'light'}
    elif possibleMoves["dark"] > 0:
        result = {'status': 'dark'}
    else:
        result = {'status': 'end'}
    
    return result

def _getPossibleMoveCount(board, light, dark, blank):
    possibleLightMoves = 0
    possibleDarkMoves = 0
    
    for position, token in enumerate(board):
        if token != blank: 
            if token == dark:
                possibleDarkMoves += _calculateMoveCount(token, position, board, light, dark, blank)
            elif token == light:
                possibleLightMoves += _calculateMoveCount(token, position, board, light, dark, blank)
    result = {
        "light": possibleLightMoves,
        "dark": possibleDarkMoves
        }
    return result

def _calculateMoveCount(currentToken, position, board, light, dark, blank):
    length = len(board)
    elementsInRow = int(math.sqrt(length))
    possibleMoves = 0
    oppositeToken = dark if currentToken == light else light
    
    # get the row of this token to compare with the tokens that surround it
    # by dividing the first position in the row by the number of elements in a row
    firstIndexInRow = position - position % elementsInRow
    lastIndexInRow = firstIndexInRow + elementsInRow - 1

    # Direction: Horizontal Left
    try:
        indexOfLeftAdjacent = position - 1
        while (firstIndexInRow <= indexOfLeftAdjacent 
               and indexOfLeftAdjacent > 0):
            tokenLeft = board[indexOfLeftAdjacent]
            if tokenLeft == oppositeToken and board[indexOfLeftAdjacent - 1] == blank:
                possibleMoves += 1
                break
            elif tokenLeft == blank or tokenLeft == currentToken:
                break
            else:
                indexOfLeftAdjacent -= 1
    except IndexError:
        pass
    
    # Direction: Horizontal Right
    try:
        indexOfRightAdjacent = position + 1
        while (lastIndexInRow >= indexOfRightAdjacent 
               and indexOfRightAdjacent < len(board) - 1):
            tokenRight = board[indexOfRightAdjacent]
            if tokenRight == oppositeToken and board[indexOfRightAdjacent + 1] == blank:
                possibleMoves += 1
                break
            elif tokenRight == blank or tokenRight == currentToken:
                break
            else:
                indexOfRightAdjacent += 1
    except IndexError:
        pass
    
    # Direction: Vertical Up
    try:
        indexOfAboveAdjacent = position - elementsInRow
        while indexOfAboveAdjacent > 0:
            tokenAbove = board[indexOfAboveAdjacent]
            if tokenAbove == oppositeToken and board[indexOfAboveAdjacent - elementsInRow] == blank:
                possibleMoves += 1
                break
            elif tokenAbove == blank or tokenAbove == currentToken:
                break
            else:
                indexOfAboveAdjacent -= elementsInRow
    except IndexError:
        pass
    
    # Direction: Vertical Down
    try:
        indexOfBelowAdjacent = position + elementsInRow
        while indexOfBelowAdjacent < len(board) - 1:
            tokenBelow = board[indexOfBelowAdjacent]
            if tokenBelow == oppositeToken and board[indexOfBelowAdjacent + elementsInRow] == blank:
                possibleMoves += 1
                break
            elif tokenBelow == blank or tokenBelow == currentToken:
                break
            else:
                indexOfBelowAdjacent += elementsInRow
    except IndexError:
        pass
    
    # Direction: Diagonal Up, Left
    try:
        indexOfAboveAdjacent = position - elementsInRow
        indexOfAboveLeftAdjacent = indexOfAboveAdjacent - 1
        while indexOfAboveLeftAdjacent > 0:
            tokenAboveLeft = board[indexOfAboveLeftAdjacent]
            if tokenAboveLeft == oppositeToken and board[indexOfAboveLeftAdjacent - (elementsInRow + 1)] == blank:
                firstIndexInPrevRow = indexOfAboveAdjacent - indexOfAboveAdjacent % elementsInRow
                if indexOfAboveLeftAdjacent >= firstIndexInPrevRow:
                    possibleMoves += 1
                break
            elif tokenAboveLeft == blank or tokenAboveLeft == currentToken:
                break
            else:
                indexOfAboveAdjacent -= elementsInRow
                indexOfAboveLeftAdjacent -= (elementsInRow + 1)
    except IndexError:
        pass
    
    # Direction: Diagonal Up, Right
    try:
        indexOfAboveAdjacent = position - elementsInRow
        indexOfAboveRightAdjacent = indexOfAboveAdjacent + 1
        while indexOfAboveRightAdjacent > 0:
            tokenAboveRight = board[indexOfAboveRightAdjacent]
            if tokenAboveRight == oppositeToken and board[indexOfAboveRightAdjacent - (elementsInRow - 1)] == blank:
                firstIndexInPrevRow = indexOfAboveAdjacent - indexOfAboveAdjacent % elementsInRow
                lastIndexInPrevRow = firstIndexInPrevRow + elementsInRow - 1
                if indexOfAboveRightAdjacent <= lastIndexInPrevRow:
                    possibleMoves += 1
                break
            elif tokenAboveRight == blank or tokenAboveRight == currentToken:
                break
            else:
                indexOfAboveAdjacent -= elementsInRow
                indexOfAboveRightAdjacent -= (elementsInRow - 1)
    except IndexError:
        pass
    
    # Direction: Diagonal Down, Left
    try:
        indexOfBelowAdjacent = position + elementsInRow
        indexOfBelowLeftAdjacent = indexOfBelowAdjacent + 1
        while indexOfBelowLeftAdjacent < len(board) - 1:
            tokenBelowLeft = board[indexOfBelowLeftAdjacent]
            if tokenBelowLeft == oppositeToken and board[indexOfBelowLeftAdjacent + elementsInRow - 1] == blank:
                firstIndexInNextRow = indexOfBelowAdjacent - indexOfBelowAdjacent % elementsInRow
                if indexOfBelowLeftAdjacent >= firstIndexInNextRow:
                    possibleMoves += 1
                break
            elif tokenBelowLeft == blank or tokenBelowLeft == currentToken:
                break
            else:
                indexOfBelowAdjacent += elementsInRow
                indexOfBelowLeftAdjacent += (elementsInRow + 1)
    except IndexError:
        pass
    
    # Direction: Diagonal Down, Right
    try:
        indexOfBelowAdjacent = position + elementsInRow
        indexOfBelowRightAdjacent = position + elementsInRow + 1
        while indexOfBelowRightAdjacent < len(board) - 1:
            tokenBelowRight = board[indexOfBelowRightAdjacent]
            if tokenBelowRight == oppositeToken and board[indexOfBelowRightAdjacent + elementsInRow + 1] == blank:
                firstIndexInNextRow = indexOfBelowAdjacent - indexOfBelowAdjacent % elementsInRow
                lastIndexInNextRow = firstIndexInNextRow + elementsInRow - 1
                if indexOfBelowRightAdjacent <= lastIndexInNextRow:
                    possibleMoves += 1
                break
            elif tokenBelowRight == blank or tokenBelowRight == currentToken:
                break
            else:
                indexOfBelowRightAdjacent += (elementsInRow - 1)
    except IndexError:
        pass
    return possibleMoves

# def _getRowFromBoard(rowNum, board):
#     elementsInRow = int(math.sqrt(len(board)))
#     row = board[(elementsInRow * rowNum):(elementsInRow * rowNum + elementsInRow)]
#     return row