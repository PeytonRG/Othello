'''
    Created on March 11, 2020
    @author: Peyton Gasink
'''
import hashlib

def _create(inputDictionary):
    errorList = []
    
    try:
        if inputDictionary["light"] > 9:
            errorList.append("The value for light tokens is " 
            + "above the accepted range.")
        elif inputDictionary["light"] < 0:
            errorList.append("The value for light tokens is " 
            + "below the accepted range.")
        light = inputDictionary["light"]
    except KeyError:
        light = 1
    except TypeError:
        errorList.append("The value for light tokens must " 
            + "be an integer.")
    
    try:
        if inputDictionary["dark"] > 9:
            errorList.append("The value for dark tokens is " 
            + "above the accepted range.")
        elif inputDictionary["dark"] < 0:
            errorList.append("The value for dark tokens is " 
            + "below the accepted range.")
        dark = inputDictionary["dark"]
    except KeyError:
        dark = 2
    except TypeError:
        errorList.append("The value for dark tokens must " 
            + "be an integer.")
    
    try:
        if inputDictionary["blank"] > 9:
            errorList.append("The value for blank spaces is " 
            + "above the accepted range.")
        elif inputDictionary["blank"] < 0:
            errorList.append("The value for blank spaces is " 
            + "below the accepted range.")
        blank = inputDictionary["blank"]
    except KeyError:
        blank = 0
    except TypeError:
        errorList.append("The value for blank spaces must " 
            + "be an integer.")
        
    try:
        if inputDictionary["size"] > 16:
            errorList.append("The value for board size is " 
            + "above the accepted range.")
        elif inputDictionary["size"] < 6:
            errorList.append("The value for board size is " 
            + "below the accepted range.")
        lengthWidth = inputDictionary["size"]
    except KeyError:
        lengthWidth = 8
        
    if len(errorList) > 0:
        return {"status": "error: " + errorList[0]}
    
    boardSize = lengthWidth**2
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
            
    boardString = "".join(str(element) for element in board)
    integrity = str.encode(boardString + f"/{light}/{dark}/{blank}/{dark}")
    
    
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
