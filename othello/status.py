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
    indexOfLeftAdjacent = position - 1
    # Only enter the loop if it remains on the current row and on the board
    while (firstIndexInRow <= indexOfLeftAdjacent 
           and indexOfLeftAdjacent > 0):
        tokenLeft = board[indexOfLeftAdjacent]
        lookahead = indexOfLeftAdjacent - 1
        if lookahead >= firstIndexInRow:
            if tokenLeft == oppositeToken and board[indexOfLeftAdjacent - 1] == blank:
                possibleMoves += 1
                break
            elif tokenLeft == blank or tokenLeft == currentToken:
                break
            else:
                indexOfLeftAdjacent -= 1
        else:
            break
    
    # Direction: Horizontal Right
    indexOfRightAdjacent = position + 1
    # Only enter the loop if it remains on the current row and on the board
    while (lastIndexInRow >= indexOfRightAdjacent 
           and indexOfRightAdjacent < len(board) - 1):
        tokenRight = board[indexOfRightAdjacent]
        lookahead = indexOfRightAdjacent + 1
        if lookahead <= lastIndexInRow:
            if tokenRight == oppositeToken and board[lookahead] == blank:
                possibleMoves += 1
                break
            elif tokenRight == blank or tokenRight == currentToken:
                break
            else:
                indexOfRightAdjacent += 1
        else:
            break
    
    # Direction: Vertical Up
    indexOfAboveAdjacent = position - elementsInRow
    # Only enter the loop if there is a row above the current row
    while indexOfAboveAdjacent > 0:
        tokenAbove = board[indexOfAboveAdjacent]
        lookahead = indexOfAboveAdjacent - elementsInRow
        # Ensure the next space to check is also on the board
        if lookahead >= 0:
            if tokenAbove == oppositeToken and board[lookahead] == blank:
                possibleMoves += 1
                break
            elif tokenAbove == blank or tokenAbove == currentToken:
                break
            else:
                indexOfAboveAdjacent -= elementsInRow
        else:
            break
        
    # Direction: Vertical Down
    indexOfBelowAdjacent = position + elementsInRow
    # Only enter the loop if there is a row below the current row
    while indexOfBelowAdjacent < len(board) - 1:
        tokenBelow = board[indexOfBelowAdjacent]
        lookahead = indexOfBelowAdjacent + elementsInRow
        # Ensure the next space to check is also on the board
        if lookahead <= len(board) - 1:
            if tokenBelow == oppositeToken and board[lookahead] == blank:
                possibleMoves += 1
                break
            elif tokenBelow == blank or tokenBelow == currentToken:
                break
            else:
                indexOfBelowAdjacent += elementsInRow
        else:
            break
    
    # Direction: Diagonal Up, Left
    indexOfAboveLeftAdjacent = position - elementsInRow - 1
    # Only enter the loop if there is a row above the current row
    while indexOfAboveLeftAdjacent > 0:
        tokenAboveLeft = board[indexOfAboveLeftAdjacent]
        indexOfAboveAdjacent = indexOfAboveLeftAdjacent + 1
        lookahead = indexOfAboveLeftAdjacent - elementsInRow - 1
        # Ensure the next space to check is also on the board
        if indexOfAboveAdjacent >= 0 and lookahead >= 0:
            firstIndexInPrevRow = indexOfAboveAdjacent - indexOfAboveAdjacent % elementsInRow
            # In addition to the usual checks for token colors, ensure no wrapping around
            # to the other side of the board
            if (indexOfAboveLeftAdjacent >= firstIndexInPrevRow 
                and tokenAboveLeft == oppositeToken and board[lookahead] == blank):
                
                possibleMoves += 1
                break
            elif tokenAboveLeft == blank or tokenAboveLeft == currentToken:
                break
            else:
                indexOfAboveLeftAdjacent -= (elementsInRow + 1)
        else: 
            break
    
    # Direction: Diagonal Up, Right
    indexOfAboveRightAdjacent = position - elementsInRow + 1
    # Only enter the loop if there is a row above the current row
    while indexOfAboveRightAdjacent > 0:
        tokenAboveRight = board[indexOfAboveRightAdjacent]
        indexOfAboveAdjacent = indexOfAboveRightAdjacent + 1
        lookahead = indexOfAboveRightAdjacent - elementsInRow + 1
        # Ensure the next space to check is also on the board
        if indexOfAboveRightAdjacent <= len(board) - 1 and lookahead <= len(board) - 1:
            firstIndexInPrevRow = indexOfAboveAdjacent - indexOfAboveAdjacent % elementsInRow
            lastIndexInPrevRow = firstIndexInPrevRow + elementsInRow - 1
            if (indexOfAboveRightAdjacent <= lastIndexInPrevRow 
                and tokenAboveRight == oppositeToken 
                and board[indexOfAboveRightAdjacent - (elementsInRow - 1)] == blank):
                
                possibleMoves += 1
                break
            elif tokenAboveRight == blank or tokenAboveRight == currentToken:
                break
            else:
                indexOfAboveRightAdjacent -= (elementsInRow - 1)
    
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

