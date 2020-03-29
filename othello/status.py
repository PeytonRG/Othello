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
    
    row = _getRowFromBoard(0, board)
    row = _getRowFromBoard(3, board)
    
    result = {'status': 'ok'}
    return result

def _getRowFromBoard(rowNum, board):
    elementsInRow = int(math.sqrt(len(board)))
    row = board[(elementsInRow * rowNum):(elementsInRow * rowNum + elementsInRow)]
    return row