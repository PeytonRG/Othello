'''
    Created on March 11, 2020
    Last Modified March 12, 2020
    @author: Peyton Gasink
'''
import hashlib
from othello import parmValidation

def _create(inputDictionary):
    errorList = []
    
    light = parmValidation._validateLight(inputDictionary, errorList)
    
    dark = parmValidation._validateDark(inputDictionary, errorList)
    
    blank = parmValidation._validateBlank(inputDictionary, errorList)
        
    lengthWidth = parmValidation._validateSize(inputDictionary, errorList)
           
    parmValidation._validateUnqiueLightDarkBlankValues(light, dark, blank, errorList)
        
    if len(errorList) > 0:
        return {"status": "error: " + errorList[0]}
    
    board = _generateBoard(light, dark, blank, lengthWidth)
            
    integrity = _generateHash(board, light, dark, blank)
    
    result = {
        "board": board,
        "tokens": {
            "light": light, 
            "dark": dark, 
            "blank": blank
            },
        "integrity": hashlib.sha256(integrity).hexdigest(),
        "status": "ok"
        }
    return result



def _generateBoard(light, dark, blank, lengthWidth):
    boardSize = lengthWidth ** 2
    boardMidpoint = boardSize / 2 - 1
    distanceFromMidpoint = lengthWidth / 2
    board = []
    
    for index in range(boardSize):
        # the token indexed either n below or n + 1 above the midpoint
        # should be a light token, where n is distanceFromMidpoint, or half
        # the length/width of the board
        if ((boardMidpoint - distanceFromMidpoint) == index or 
            (boardMidpoint + distanceFromMidpoint + 1) == index):
            board.append(light)
        # likewise, the token indexed at n + 1 below the midpoint
        # or n above the midpoint should be a dark token
        elif ((boardMidpoint - distanceFromMidpoint + 1) == index or 
              (boardMidpoint + distanceFromMidpoint) == index):
            board.append(dark)
        else:
            board.append(blank)
    return board

def _generateHash(board, light, dark, blank):
    boardString = "".join(str(space) for space in board)
    integrity = str.encode(boardString + f"/{light}/{dark}/{blank}/{dark}")
    return integrity






