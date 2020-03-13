'''
    Created on March 11, 2020
    Last Modified March 12, 2020
    @author: Peyton Gasink
'''
import hashlib

def _create(inputDictionary):
    errorList = []
    
    light = _validateLight(inputDictionary, errorList)
    
    dark = _validateDark(inputDictionary, errorList)
    
    blank = _validateBlank(inputDictionary, errorList)
        
    lengthWidth = _validateSize(inputDictionary, errorList)
           
    if light == dark or light == blank or dark == blank:
        errorList.append("The values of light, dark, " 
            + "and blank must be unique.")
        
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

def _validateLight(inputDictionary, errorList):
    errorMessage = ("The value for light tokens must be an integer in the " + 
                    "range [0, 9].")
    try:
        light = inputDictionary["light"]
        if isinstance(light, float):
            raise ValueError
        else:
            # cast the string from the HTTP request into int
            # will raise ValueError upon failure
            light = int(light)
            
        if light > 9 or light < 0:
            errorList.append(errorMessage)
    except KeyError:
        light = 1
    except (ValueError, TypeError):
        light = 1
        errorList.append(errorMessage)
    return light

def _validateDark(inputDictionary, errorList):
    errorMessage = ("The value for dark tokens must be an integer in the " + 
                    "range [0, 9].")
    try:
        dark = inputDictionary["dark"]
        if isinstance(dark, float):
            raise ValueError
        else:
            # cast the string from the HTTP request into int
            # will raise ValueError upon failure
            dark = int(dark)
            
        if dark > 9 or dark < 0:
            errorList.append(errorMessage)
    except KeyError:
        dark = 2
    except (ValueError, TypeError):
        dark = 2
        errorList.append(errorMessage)
    return dark

def _validateBlank(inputDictionary, errorList):
    try:
        blank = inputDictionary["blank"]
        if isinstance(blank, float):
            raise ValueError
        else:
            # cast the string from the HTTP request into int
            # will raise ValueError upon failure
            blank = int(blank)
            
        if blank > 9 or blank < 0:
            errorList.append("The value for blank spaces must " + 
                             "be an integer in the range [0, 9].")
    except KeyError:
        blank = 0
    except (ValueError, TypeError):
        blank = 0
        errorList.append(
            "The value for blank spaces must " + 
            "be an integer in the range [0, 9].")
    return blank

def _validateSize(inputDictionary, errorList):
    try:
        lengthWidth = inputDictionary["size"]
        if isinstance(lengthWidth, float):
            raise ValueError
        else:
            # cast the string from the HTTP request into int
            # will raise ValueError upon failure
            lengthWidth = int(lengthWidth)
            
        if (lengthWidth % 2 != 0) or (lengthWidth > 16) or (lengthWidth < 6):
            errorList.append("The value for board size must " + 
                             "be an even integer in the range [6, 16].")
    except KeyError:
        lengthWidth = 8
    except (ValueError, TypeError):
        lengthWidth = 8
        errorList.append(
            "The value for board size must " + 
            "be an even integer in the range [6, 16].")
    return lengthWidth

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






