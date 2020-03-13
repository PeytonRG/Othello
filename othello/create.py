'''
    Created on March 11, 2020
    @author: Peyton Gasink
'''
import hashlib

def _create(inputDictionary):
    errorList = []
    light = 0
    dark = 0
    blank = 0
    lengthWidth = 0
    
    try:
        light = inputDictionary["light"]
        if light > 9 or light < 0:
            errorList.append("The value for light tokens must " 
            + "be an integer in the range [0, 9].")
    except KeyError:
        light = 1
    except TypeError:
        errorList.append("The value for light tokens must " 
            + "be an integer in the range [0, 9].")
    
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
        lengthWidth = inputDictionary["size"]
        if (lengthWidth % 2 != 0) or (lengthWidth > 16) or (lengthWidth < 6):
            errorList.append("The value for board size must " 
            + "be an even integer in the range [6, 16].")
    except KeyError:
        lengthWidth = 8
    except TypeError:
        errorList.append("The value for board size must " 
            + "be an even integer in the range [6, 16].")
           
    if light == dark or light == blank or dark == blank:
        errorList.append("The values of light, dark, " 
            + "and blank must be unique.")
        
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
