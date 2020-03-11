'''
    Created on March 11, 2020
    @author: Peyton Gasink
'''
def _create(inputDictionary):
    light = inputDictionary["light"]
    dark = inputDictionary["dark"]
    blank = inputDictionary["blank"]
    boardSize = inputDictionary["size"]
    
    board = []
    for index in range(boardSize**2):
        board.append(blank)
        
    result = {"board": board}
    return result
