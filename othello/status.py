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
    length = len(board)
    nextStartTokenIndex = 0
    elementsInRow = int(math.sqrt(length))
    for token in board:
        if token != blank:
            tokenIndex = board.index(token, nextStartTokenIndex, length - 1)
            nextStartTokenIndex = tokenIndex + 1
            # track the row of this token to compare with the tokens that surround it
            # by dividing the first element in the row by the number of elements in a row
            rowNum = int((tokenIndex - tokenIndex % elementsInRow) / elementsInRow)
            
            tokenLeftOfCurrentToken = board[tokenIndex - 1]
            tokenRightOfCurrentToken = board[tokenIndex + 1]           
                
            # index of the current token relative to its row
            relativeIndex = tokenIndex - rowNum * elementsInRow
            
            # get the two rows above and below the current row
            rowAbove = _getRowFromBoard(rowNum - 1, board)
            twoRowsAbove = _getRowFromBoard(rowNum - 2, board)
            rowBelow = _getRowFromBoard(rowNum + 1, board)
            twoRowsBelow = _getRowFromBoard(rowNum + 2, board)
            
            # get the tokens above and below the current token
            tokenAbove = rowAbove[relativeIndex]
            twoTokensAbove = twoRowsAbove[relativeIndex]
            tokenBelow = rowBelow[relativeIndex]
            twoTokensBelow = twoRowsBelow[relativeIndex]
            
            if token == light:
                # immediate left token must be light and the left of that must be blank
                if tokenLeftOfCurrentToken == dark and board[tokenIndex - 2] == blank:
                    possibleLightMoves += 1
                    
                # same idea but to the right
                if tokenRightOfCurrentToken == dark and board[tokenIndex + 2] == blank:
                    possibleLightMoves += 1
                    
                if tokenAbove == dark and twoTokensAbove == blank:
                    possibleLightMoves += 1
            
                if tokenBelow == dark and twoTokensBelow == blank:
                    possibleLightMoves += 1
                    
            if token == dark:
                # immediate left token must be light and the left of that must be blank
                if tokenLeftOfCurrentToken == light and board[tokenIndex - 2] == blank:
                    possibleDarkMoves += 1
                    
                # same idea but to the right
                if tokenRightOfCurrentToken == light and board[tokenIndex + 2] == blank:
                    possibleDarkMoves += 1
                    
                if tokenAbove == light and twoTokensAbove == blank:
                    possibleDarkMoves += 1
            
                if tokenBelow == light and twoTokensBelow == blank:
                    possibleDarkMoves += 1
    
    result = {
        "light": possibleLightMoves,
        "dark": possibleDarkMoves
        }
    return result

def _getRowFromBoard(rowNum, board):
    elementsInRow = int(math.sqrt(len(board)))
    row = board[(elementsInRow * rowNum):(elementsInRow * rowNum + elementsInRow)]
    return row