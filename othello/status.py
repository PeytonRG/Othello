'''
    Created on March 28, 2020
    Last Modified March 31, 2020
    @author: Peyton Gasink
'''

import math
from othello import parmValidation

def _status(inputDictionary):
    errorList = []
    
    light = parmValidation._validateLight(inputDictionary, errorList)
    
    dark = parmValidation._validateDark(inputDictionary, errorList)
    
    blank = parmValidation._validateBlank(inputDictionary, errorList)
    
    parmValidation._validateUnqiueLightDarkBlankValues(light, dark, blank, errorList)
        
    board = parmValidation._validateBoard(inputDictionary, light, dark, blank, errorList)
    
    # Integrity is not saved to a variable because it is only used for validation 
    parmValidation._validateIntegrity(inputDictionary, light, dark, blank, board, errorList)
        
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

    # Direction: Horizontal Left
    directionFunctions = {
        "offset": _getOffsetLeft,
        "loopCondition": _loopConditionLeft,
        "rowBounding": _enforceRowBoundingLeft
    }
    
    possibleMoves += _scanInOneDimension(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
    
    # Direction: Horizontal Right
    directionFunctions = {
        "offset": _getOffsetRight,
        "loopCondition": _loopConditionRight,
        "rowBounding": _enforceRowBoundingRight
    }
    
    possibleMoves += _scanInOneDimension(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
    
    # Direction: Vertical Up
    directionFunctions = {
        "offset": _getOffsetAbove,
        "loopCondition": _loopConditionAbove,
        "rowBounding": _enforceRowBoundingAbove
    }
    
    possibleMoves += _scanInOneDimension(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
        
    # Direction: Vertical Down
    directionFunctions = {
        "offset": _getOffsetBelow,
        "loopCondition": _loopConditionBelow,
        "rowBounding": _enforceRowBoundingBelow
    }
    
    possibleMoves += _scanInOneDimension(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
    
    # Direction: Diagonal Up, Left
    directionFunctions = {
        "offset": _getOffsetAboveLeft,
        "loopCondition": _loopConditionAbove,
        "rowBounding": _enforceRowBoundingAboveDiagonals,
        "wrapAround": _enforceRowBoundingLeft,
        "verticalNeighbor": _getOffsetRight
    }
    
    possibleMoves += _scanInTwoDimensions(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
    
    # Direction: Diagonal Up, Right
    directionFunctions = {
        "offset": _getOffsetAboveRight,
        "loopCondition": _loopConditionAbove,
        "rowBounding": _enforceRowBoundingAboveDiagonals,
        "wrapAround": _enforceRowBoundingRight,
        "verticalNeighbor": _getOffsetLeft
    }    
    
    possibleMoves += _scanInTwoDimensions(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
    
    # Direction: Diagonal Down, Left
    directionFunctions = {
        "offset": _getOffsetBelowLeft,
        "loopCondition": _loopConditionBelow,
        "rowBounding": _enforceRowBoundingBelowDiagonals,
        "wrapAround": _enforceRowBoundingLeft,
        "verticalNeighbor": _getOffsetRight
    }    
    
    possibleMoves += _scanInTwoDimensions(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)
    
    # Direction: Diagonal Down, Right
    directionFunctions = {
        "offset": _getOffsetBelowRight,
        "loopCondition": _loopConditionBelow,
        "rowBounding": _enforceRowBoundingBelowDiagonals,
        "wrapAround": _enforceRowBoundingRight,
        "verticalNeighbor": _getOffsetLeft
    }    
    
    possibleMoves += _scanInTwoDimensions(position, elementsInRow, currentToken, oppositeToken,
                                     blank, board, directionFunctions)

    return possibleMoves

def _scanInOneDimension(position, elementsInRow, currentToken, oppositeToken, blank, board, directionFunctions):
    possibleMoves = 0
    
    # get the row of this token to compare with the tokens that surround it
    # by dividing the first position in the row by the number of elements in a row
    firstIndexInRow = position - position % elementsInRow
    
    indexOfNeighbor = directionFunctions["offset"](elementsInRow, position)
    # Only enter the loop if it remains on the current row and on the board
    while (directionFunctions["loopCondition"](board, elementsInRow, firstIndexInRow, indexOfNeighbor)):
        neighborValue = board[indexOfNeighbor]
        lookahead = directionFunctions["offset"](elementsInRow, indexOfNeighbor)
        if directionFunctions["rowBounding"](board, elementsInRow, firstIndexInRow, lookahead):
            if neighborValue == oppositeToken and board[directionFunctions["offset"](elementsInRow, indexOfNeighbor)] == blank:
                possibleMoves += 1
                break
            elif neighborValue == blank or neighborValue == currentToken:
                break
            else:
                indexOfNeighbor = directionFunctions["offset"](elementsInRow, indexOfNeighbor)
        else:
            break
        
    return possibleMoves

def _scanInTwoDimensions(position, elementsInRow, currentToken, oppositeToken, blank, board, directionFunctions):
    possibleMoves = 0
    
    # get the row of this token to compare with the tokens that surround it
    # by dividing the first position in the row by the number of elements in a row
    firstIndexInRow = position - position % elementsInRow
    
    indexOfNeighbor = directionFunctions["offset"](elementsInRow, position)
    # Only enter the loop if there is a row above the current row
    while directionFunctions["loopCondition"](board, elementsInRow, firstIndexInRow, indexOfNeighbor):
        neighborValue = board[indexOfNeighbor]
        indexOfVerticalNeighbor = directionFunctions["verticalNeighbor"](elementsInRow, indexOfNeighbor)
        lookahead = directionFunctions["offset"](elementsInRow, indexOfNeighbor)
        # Ensure the next space to check is also on the board
        if directionFunctions["rowBounding"](board, elementsInRow, indexOfVerticalNeighbor, lookahead):
            
            firstIndexInNeighboringRow = indexOfVerticalNeighbor - indexOfVerticalNeighbor % elementsInRow
            
            # In addition to the usual checks for token colors, ensure no wrapping around
            # to the other side of the board
            if (directionFunctions["wrapAround"](board, elementsInRow, firstIndexInNeighboringRow, indexOfNeighbor) 
                and neighborValue == oppositeToken and board[lookahead] == blank):
                
                possibleMoves += 1
                break
            elif neighborValue == blank or neighborValue == currentToken:
                break
            else:
                indexOfNeighbor = directionFunctions["offset"](elementsInRow, indexOfNeighbor)
        else: 
            break
    
    return possibleMoves


# Loop Condition Helper Functions
def _loopConditionAbove(board, elementsInRow, firstIndexInRow, indexOfNeighbor):
    return indexOfNeighbor > 0

def _loopConditionBelow(board, elementsInRow, firstIndexInRow, indexOfNeighbor):
    return indexOfNeighbor < len(board) - 1

def _loopConditionLeft(board, elementsInRow, firstIndexInRow, indexOfHorizontalNeighbor):
    return (firstIndexInRow <= indexOfHorizontalNeighbor 
           and indexOfHorizontalNeighbor > 0)
    
def _loopConditionRight(board, elementsInRow, firstIndexInRow, indexOfHorizontalNeighbor):
    lastIndexInRow = firstIndexInRow + elementsInRow - 1
    return (lastIndexInRow >= indexOfHorizontalNeighbor 
           and indexOfHorizontalNeighbor < len(board) - 1)


# Row Bounding Helper Functions
def _enforceRowBoundingAbove(board, elementsInRow, firstIndexInRow, lookahead):
    return lookahead >= 0

def _enforceRowBoundingAboveDiagonals(board, elementsInRow, indexOfVerticalNeighbor, lookahead):
    return indexOfVerticalNeighbor >= 0 and lookahead >= 0

def _enforceRowBoundingBelow(board, elementsInRow, firstIndexInRow, lookahead):
    return lookahead <= len(board) - 1

def _enforceRowBoundingBelowDiagonals(board, elementsInRow, indexOfVerticalNeighbor, lookahead):
    return indexOfVerticalNeighbor <= len(board) - 1 and lookahead <= len(board) - 1
           
def _enforceRowBoundingLeft(board, elementsInRow, firstIndexInRow, lookahead):
    return lookahead >= firstIndexInRow

def _enforceRowBoundingRight(board, elementsInRow, firstIndexInRow, lookahead):
    lastIndexInRow = firstIndexInRow + elementsInRow - 1
    return lookahead <= lastIndexInRow


# Offset Locating Helper Functions
def _getOffsetAbove(elementsInRow, position):
    return position - elementsInRow

def _getOffsetAboveLeft(elementsInRow, position):
    return position - elementsInRow - 1

def _getOffsetAboveRight(elementsInRow, position):
    return position - elementsInRow + 1

def _getOffsetBelow(elementsInRow, position):
    return position + elementsInRow

def _getOffsetBelowLeft(elementsInRow, position):
    return position + elementsInRow - 1

def _getOffsetBelowRight(elementsInRow, position):
    return position + elementsInRow + 1

def _getOffsetLeft(elementsInRow, position):
    return position - 1

def _getOffsetRight(elementsInRow, position):
    return position + 1
