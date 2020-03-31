import hashlib
import math
from _ctypes import ArgumentError

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
    errorMessage = ("The value for blank spaces must be an integer in the " + 
                    "range [0, 9].")
    try:
        blank = inputDictionary["blank"]
        if isinstance(blank, float):
            raise ValueError
        else:
            # cast the string from the HTTP request into int
            # will raise ValueError upon failure
            blank = int(blank)
            
        if blank > 9 or blank < 0:
            errorList.append(errorMessage)
            
    except KeyError:
        blank = 0
    except (ValueError, TypeError):
        blank = 0
        errorList.append(errorMessage)
    return blank

def _validateUnqiueLightDarkBlankValues(light, dark, blank, errorList):
    if light == dark or light == blank or dark == blank:
        errorList.append("The values of light, dark, " 
            + "and blank must be unique.")

def _validateSize(inputDictionary, errorList):
    errorMessage = ("The value for board size must be an even integer in " + 
                    "the range [6, 16].")
    try:
        size = inputDictionary["size"]
        if isinstance(size, float):
            raise ValueError
        else:
            # cast the string from the HTTP request into int
            # will raise ValueError upon failure
            size = int(size)
            
        if (size % 2 != 0) or (size > 16) or (size < 6):
            errorList.append(errorMessage)
            
    except KeyError:
        size = 8
    except (ValueError, TypeError):
        size = 8
        errorList.append(errorMessage)
    return size

def _validateBoard(inputDictionary, light, dark, blank, errorList):
    # The validation for the other properties in inputDictionary has run by this point,
    # so only proceed if there were no errors.
    if len(errorList) == 0:
        standardErrorMessage = "The board be a square with even length and width, in the range [6, 16]."
        invalidTokensInBoardMessage = "The board must contain only light, dark, and blank tokens."
        try:
            # This will throw a KeyError if there is no board key
            board = inputDictionary["board"]
            
            # This will throw a TypeError if board is None
            size = math.sqrt(len(board))
            
            # This board is not a square
            if size != math.floor(size):
                raise ValueError
            
            # This board is a square, but with odd length and width
            if len(board) % 2 != 0:
                raise ValueError
            
            lightCount = board.count(light)
            darkCount = board.count(dark)
            blankCount = board.count(blank)
            
            # There are values other than light, dark, and blank in this board
            if lightCount + darkCount + blankCount != len(board):
                raise ArgumentError
            
            return board
        
        except (KeyError, TypeError, ValueError):
            errorList.append(standardErrorMessage)
        except ArgumentError:
            errorList.append(invalidTokensInBoardMessage)
        
def _validateIntegrity(inputDictionary, light, dark, blank, board, errorList):
    # The validation for the other properties in inputDictionary has run by this point,
    # so only proceed if there were no errors.
    if len(errorList) == 0:
        standardErrorMessage = "The integrity string must be 64-character sha-256 hash hexdigest."
        nonMatchingHashErrorMessage = "The provided board and integrity hash do not match."
        try:
            # This will raise a KeyError if there is no integrity key
            integrity = inputDictionary["integrity"]
            
            # Convert to a decimal number. This will raise a ValueError if the integrity
            # is not a valid hexdigest. Addtionally, it will raise a TypeError if integrity
            # is None.
            integrityAsDecimal = int(integrity, 16)
            
            generatedIntegrityLight = _generateHash(board, light, dark, blank, light)
            generatedIntegrityDark = _generateHash(board, light, dark, blank, dark)
            generatedIntegrityEnd = _generateHash(board, light, dark, blank)
            
            if len(integrity) != 64:
                raise ValueError
            
            if integrity != generatedIntegrityLight and integrity != generatedIntegrityDark:
                raise ArgumentError
            
            return integrity
            
        except (KeyError, TypeError, ValueError):
            errorList.append(standardErrorMessage)
        except ArgumentError:
            errorList.append(nonMatchingHashErrorMessage)
    
def _generateHash(board, light, dark, blank, nextTurn = None):
    boardString = "".join(str(space) for space in board)
    
#     if nextTurn == None:
#         nextTurn = dark
    if nextTurn != None:
        integrity = str.encode(boardString + f"/{light}/{dark}/{blank}/{nextTurn}")
    else:
        integrity = str.encode(boardString + f"/{light}/{dark}/{blank}/")
    integrityHash = hashlib.sha256(integrity).hexdigest()
    
    return integrityHash       
    
    
    