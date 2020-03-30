import math

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

def _validateBoard(inputDictionary, errorList):
    errorMessage = "The board be a square with even length and width, in the range [6, 16]."
    try:
        board = inputDictionary["board"]
        
        if not(isinstance(math.sqrt(len(board)), int)):
            raise ValueError
        
#         if len(board) % 2 != 0:
#             raise ValueError
        
    except ValueError:
        errorList.append(errorMessage)
    
    