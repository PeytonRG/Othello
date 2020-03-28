'''
    Created on March 28, 2020
    Last Modified March 28, 2020
    @author: Peyton Gasink
'''
import hashlib
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
    
    result = {'status': 'ok'}
    return result
