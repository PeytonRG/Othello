'''
    Created on March 28, 2020
    Last Modified March 28, 2020
    @author: Peyton Gasink
'''

from unittest import TestCase
import othello.status as status

class statusTest(TestCase):
    
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
        
    def test021_LowBoundLightNominalDarkBlankBoardIntegrity(self):
        self.setLight(0)
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,1,1,1,1,2,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('1b7e612b959852acbaf6b55d3f6b8dab2cdc32248a58a89dcf022ae80e5b36de')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
    
    def test022_MissingLightNominalDarkBlankBoardIntegrity(self):
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('integrity=f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test030_LowBoundDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setDark(0)
        self.setBlank(9)
        self.setBoard([9,9,9,9,9,9,9,9,9,9,9,9,9,9,5,0,9,9,9,9,0,5,9,9,9,9,9,9,9,9,9,9,9,9,9,9])
        self.setIntegrity('85c972c79b667135f99ad9380f4af4a7495c5b5de3768c9cb36c4bc73f0da08a')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test031_HighBoundDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setDark(9)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,5,9,3,3,3,3,9,5,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('34932b7f4bbafed18cf99e367e29407e6aae8b49b2ced711f31e429e7efc2a12')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test032_MissingDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,5,2,3,3,3,3,2,5,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('a348c2dae89e65378fc64d889b1d394819c021b2e4cccb37310bbef9335bb900')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test040_LowBoundBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(5)
        self.setDark(6)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,6,0,0,0,0,6,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('062f219e852404144cd7967bcbac5d5d82c151697d8eacfd8c29779acbc58b19')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
    
    def test041_HighBoundBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(5)
        self.setDark(6)
        self.setBlank(9)
        self.setBoard([9,9,9,9,9,9,9,9,9,9,9,9,9,9,5,6,9,9,9,9,6,5,9,9,9,9,9,9,9,9,9,9,9,9,9,9])
        self.setIntegrity('5b698f38d9d1c1754df196ee688f3900ceba9d074cb74b5e17c19a197b69bf02')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test042_MissingBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(5)
        self.setDark(6)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,6,0,0,0,0,6,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('062f219e852404144cd7967bcbac5d5d82c151697d8eacfd8c29779acbc58b19')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test050_LowBoundSizeBoardWithNominalElementNominalLightDarkBlankIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test051_HighBoundSizeBoardWithNominalElementNominalLightDarkBlankIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,   
                       0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,    
                       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('5df1fd1ccbd0dc74d65ab00d4d62f2e21c2def95dc47e7c73751986cdb5e8710')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
    
    def test060_DarkNextPlayerNominalLightDarkBlankBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test061_LightNextPlayerNominalLightDarkBlankBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('66271cbb9037c515e73be3a74a37259a179f2d2861cf4e82130cd579a2141093')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test070_StatusIsOk(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b')
        expectedResult = {'status': 'ok'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test071_StatusIsDark(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,1,1,1,1,0])
        self.setIntegrity('e2f7b8593ebadc126833074a7d8653d3c12c36ab3b7622a9cc6ac5dc1a0d9698')
        expectedResult = {'status': 'dark'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)

# Unit Tests

# Not sure will need the function these were testing after all. Commenting out for the time being.
#     def test210_ShouldReturnFirstRowFromBoard(self):
#         self.setBoard([0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,1,1,1,1,0])
#         expectedResult = [0,1,1,1,1,0]
#         result = status._getRowFromBoard(0, self.inputDictionary["board"])
#         self.assertEqual(result, expectedResult)
#         
#     def test211_ShouldReturnRowThreeFromBoard(self):
#         self.setBoard([0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,1,1,1,1,0])
#         expectedResult = [1,1,1,2,1,1]
#         result = status._getRowFromBoard(3, self.inputDictionary["board"])
#         self.assertEqual(result, expectedResult)
        
    def test220_ShouldReturnPossibleMoveCounts(self):
        light = 1
        dark = 2
        blank = 0
        board = [0,0,0,0,0,0,
                 0,0,0,0,0,0,
                 0,0,1,2,0,0,
                 0,0,2,1,0,0,
                 0,0,0,0,0,0,
                 0,0,0,0,0,0]
        expectedResult = {
            "light": 4,
            "dark": 4
            }
        result = status._getPossibleMoveCount(board, light, dark, blank)
        self.assertEqual(result, expectedResult)
        
    def test221_OnlyDarkShouldMove(self):
        light = 1
        dark = 2
        blank = 0
        board = [0,1,1,1,1,0,
                 1,1,1,1,1,1,
                 1,1,1,1,1,1,
                 1,1,1,2,1,1,
                 1,1,1,1,1,1,
                 0,1,1,1,1,0]
        expectedResult = {
            "light": 0,
            "dark": 2
            }
        result = status._getPossibleMoveCount(board, light, dark, blank)
        self.assertEqual(result, expectedResult)
        
