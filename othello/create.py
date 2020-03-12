'''
    Created on March 11, 2020
    @author: Peyton Gasink
'''
import hashlib

def _create(inputDictionary):
    status = []
    
    try:
        if inputDictionary["light"] > 9:
            status.append("The value for light tokens is " 
            + "above the accepted range.")
        light = inputDictionary["light"]
    except KeyError:
        light = 1
    try:
        dark = inputDictionary["dark"]
    except KeyError:
        dark = 2
    try:
        blank = inputDictionary["blank"]
    except KeyError:
        blank = 0
    try:
        lengthWidth = inputDictionary["size"]
    except KeyError:
        lengthWidth = 8
    
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
    
    if len(status) > 0:
        return {"status": "error: " + status[0]}
    else:
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
