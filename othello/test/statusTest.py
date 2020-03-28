'''
    Created on March 28, 2020
    Last Modified March 28, 2020
    @author: Peyton Gasink
'''

from unittest import TestCase
import othello.status as status

class CreateTest(TestCase):
    
    def setUp(self):
        self.inputDictionary = {}
        
    def tearDown(self):
        TestCase.tearDown(self)
        
    def setLight(self, light = None):
        self.inputDictionary["light"] = light
        
    def setDark(self, dark = None):
        self.inputDictionary["dark"] = dark
        
    def setBlank(self, blank = None):
        self.inputDictionary["blank"] = blank
        
    def setBoard(self, board = None):
        self.inputDictionary["board"] = board
        
    def setIntegrity(self, integrity = None):
        self.inputDictionary["integrity"] = integrity
        
#    Desired level of confidence:    boundary value analysis
#    Input-output Analysis
#        inputs:        light -> integer, .GE.0.LE9, optional, unvalidated,
#                                defaults to 1
#                       dark -> integer, .GE.0.LE9, optional, unvalidated
#                                defaults to 2
#                       blank -> integer, .GE.0.LE9, optional, unvalidated
#                                defaults to 0
#                       board -> list of integers with length n x n,
#                                where n is an integer .GE6.LE16, mandatory, unvalidated
#                       integrity -> 64-character sha256 hash hexdigest, mandatory, unvalidated
#        outputs:    dictionary -> key: status,
#                                  values: ok if either token can be placed
#                                          dark if only a dark token can be placed
#                                          light if only a light token can be placed
#                                          end if no tokens can be placed

# Happy Path Acceptance Tests
    def test010_NominalLightDarkBlankBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test020_HighBoundLightNominalDarkBlankBoardIntegrity(self):
        self.setLight(9)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,2,0,0,0,0,2,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('5ab81cb67067273363db989119448a0b878896f7db5c268a50c4ae3062cb3647')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test020_LowBoundLightNominalDarkBlankBoardIntegrity(self):
        self.setLight(0)
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,1,1,1,1,2,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('1b7e612b959852acbaf6b55d3f6b8dab2cdc32248a58a89dcf022ae80e5b36de')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)

        