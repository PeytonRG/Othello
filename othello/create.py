'''
    Created on March 11, 2020
    @author: Peyton Gasink
'''
def _create(inputDictionary):
    light = inputDictionary["light"]
    dark = inputDictionary["dark"]
    blank = inputDictionary["blank"]
    lengthWidth = inputDictionary["size"]
    boardSize = lengthWidth**2
    boardMidpoint = boardSize / 2 - 1
    distanceFromMidpoint = lengthWidth / 2
    
    board = []
    for index in range(boardSize):
        if ((boardMidpoint - distanceFromMidpoint) == index or 
            (boardMidpoint + distanceFromMidpoint + 1) == index):
            board.append(light)
        elif ((boardMidpoint - distanceFromMidpoint + 1) == index or 
            (boardMidpoint + distanceFromMidpoint) == index):
            board.append(dark)
        else:
            board.append(blank)
        
    result = {"board": board}
    return result
