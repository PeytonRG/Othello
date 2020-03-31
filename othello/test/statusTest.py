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
        self.setIntegrity('f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a')
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
        
    def test072_StatusIsLight(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3])
        self.setIntegrity('7c53df9ff782bbbff544d876f4d69a1d87d5864295c0e4a6bf29e6a7ee5a96fc')
        expectedResult = {'status': 'light'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test073_StatusIsEnd(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([1,1,1,1,1,1,1,1,
                       1,1,1,1,1,1,1,1,
                       1,1,1,1,1,1,1,1,
                       1,1,1,1,1,1,1,0, 
                       1,1,1,1,1,1,0,0,
                       1,1,1,1,1,1,0,2,
                       1,1,1,1,1,1,1,0,
                       1,1,1,1,1,1,1,1])
        self.setIntegrity('8a1c0659575e8cdd01b2e4ff3f431c845e7e7960279bb7abfaa5465e4a755354')
        expectedResult = {'status': 'end'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)

# Sad Path Tests
    def test900_AboveBoundLightNominalDarkBlankBoardIntegrity(self):
        self.setLight(10)
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,10,2,1,1,1,1,2,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('b71bf3bee30fb8c3caa49752bcf9656870cfbd3bec4e4353e1e491054bf11c2f')
        expectedResult = {'status': 'error: The value for light tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test901_BelowBoundLightNominalDarkBlankBoardIntegrity(self):
        self.setLight(-1)
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,2,1,1,1,1,2,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('f31631fdc7ba5ecd3096a306dbc7e43a9bc13fa781b91d83c36057f5050a51da')
        expectedResult = {'status': 'error: The value for light tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test902_NonIntegerLightNominalDarkBlankBoardIntegrity(self):
        self.setLight('X')
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,'X',2,1,1,1,1,2,'X',1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('8959fc376b23af1520014ef3bef1eb4f924ec692bbbcd9f638245bf85fb0a6da')
        expectedResult = {'status': 'error: The value for light tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test903_NullLightNominalDarkBlankBoardIntegrity(self):
        self.setLight()
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,2,1,1,1,1,2,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('1cc0050055aa122edbb536cc63dfe515e6a55132a42a6c8fa41349ab6e572c6a')
        expectedResult = {'status': 'error: The value for light tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test910_AboveBoundDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setDark(10)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,10,1,1,1,1,10,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('e8a244c301df58429d82070942fe05dff389162c0aeec8383e3c82863ae09c62')
        expectedResult = {'status': 'error: The value for dark tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test911_BelowBoundDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setDark(-1)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,-1,1,1,1,1,-1,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('301e0f00c1b83b65adc1d4fd5e87aaf7f594aa20842ab1df86a6be2e144367db')
        expectedResult = {'status': 'error: The value for dark tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test912_NonIntegerDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setDark(1.2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1.2,1,1,1,1,1.2,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('e62a2ec6eb082391a6a5664b4f4dbd8130e43d6589267b19b831423bfcde4a9d')
        expectedResult = {'status': 'error: The value for dark tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test913_NullDarkNominalLightBlankBoardIntegrity(self):
        self.setLight(5)
        self.setDark()
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('5d5aeb4a45b57eecf69dcc304664fcf7a6f7c74c86ef9ede14da46ab2d9df242')
        expectedResult = {'status': 'error: The value for dark tokens must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test920_AboveBoundBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(10)
        self.setBoard([10,10,10,10,10,10,10,10,10,10,10,10,10,10,1,2,10,10,10,10,2,1,10,10,10,10,10,10,10,10,10,10,10,10,10,10])
        self.setIntegrity('530242aec98aa07d3c025b9101bd5b840527cd9b03302641da18c801d70c37e8')
        expectedResult = {'status': 'error: The value for blank spaces must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test921_BelowBoundBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(-1)
        self.setBoard([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,2,-1,-1,-1,-1,2,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
        self.setIntegrity('2e226315d3fc18cf5771b45ae78bfe7be9510ee98b6e566e382f8a70861c8e7d')
        expectedResult = {'status': 'error: The value for blank spaces must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test922_NonIntegerBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(1E5)
        self.setBoard([1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1,2,1E5,1E5,1E5,1E5,2,1,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5])
        self.setIntegrity('fe62b7f99befb02e21c50cc755a68ef80fb59d56224b02a1f2888e0830454773')
        expectedResult = {'status': 'error: The value for blank spaces must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test923_NullBlankNominalLightDarkBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank()
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b')
        expectedResult = {'status': 'error: The value for blank spaces must '
                          + 'be an integer in the range [0, 9].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test930_NonSquareBoardNominalLightDarkBlankIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('9d43a04297202bccc81a13b6857179269c0fe33e5227c6569286d54d82493ba6')
        expectedResult = {'status': 'error: The board be a square with even length and width, in the range [6, 16].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test933_OddByOddBoardNominalLightDarkBlankIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('1e3f8bb2d56c5b4483c9f3dccf7bc16d339534a98020e9a28383aaa219f3e64d')
        expectedResult = {'status': 'error: The board be a square with even length and width, in the range [6, 16].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test934_MissingBoardNominalLightDarkBlankIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setIntegrity('1e3f8bb2d56c5b4483c9f3dccf7bc16d339534a98020e9a28383aaa219f3e64d')
        expectedResult = {'status': 'error: The board be a square with even length and width, in the range [6, 16].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test935_NullBoardNominalLightDarkBlankIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard()
        self.setIntegrity('1e3f8bb2d56c5b4483c9f3dccf7bc16d339534a98020e9a28383aaa219f3e64d')
        expectedResult = {'status': 'error: The board be a square with even length and width, in the range [6, 16].'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test940_ShortIntegrityNominalLightDarkBlankBoard(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465')
        expectedResult = {'status': 'error: The integrity string must be 64-character sha-256 hash hexdigest.'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test941_LongIntegrityNominalLightDarkBlankBoard(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a00')
        expectedResult = {'status': 'error: The integrity string must be 64-character sha-256 hash hexdigest.'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test942_NonHexIntegrityNominalLightDarkBlankBoard(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity('f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465$')
        expectedResult = {'status': 'error: The integrity string must be 64-character sha-256 hash hexdigest.'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test943_MissingIntegrityNominalLightDarkBlankBoard(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        expectedResult = {'status': 'error: The integrity string must be 64-character sha-256 hash hexdigest.'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test944_NullIntegrityNominalLightDarkBlankBoard(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(3)
        self.setBoard([3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3])
        self.setIntegrity()
        expectedResult = {'status': 'error: The integrity string must be 64-character sha-256 hash hexdigest.'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test950_NominalLightDarkEqualsLightNominalBlankBoardIntegrity(self):
        self.setLight(2)
        self.setDark(2)
        self.setBlank(0)
        self.setBoard([0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.setIntegrity('e50f93033edd2b27fd1c54631a4b574e545df9e8c06e0b4f74ca94841a4ab6c4')
        expectedResult = {'status': 'error: The values of light, dark, '
            + 'and blank must be unique.'}
        result = status._status(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test950_NominalLightDarkBlankEqualsLightNominalBoardIntegrity(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(1)
        self.setBoard([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        self.setIntegrity('c725061d80e342070c231d2b987c476f92b8f3d9e5826c2223cff281562e8e2c')
        expectedResult = {'status': 'error: The values of light, dark, '
            + 'and blank must be unique.'}
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
        
    def test222_OnlyLightShouldMove(self):
        light = 1
        dark = 2
        blank = 3
        board = [2,2,2,2,2,2,
                 2,2,2,2,2,2,
                 2,2,1,2,2,2,
                 2,2,2,2,2,2,
                 2,2,2,2,2,2,
                 2,2,2,2,2,3]
        expectedResult = {
            "light": 1,
            "dark": 0
            }
        result = status._getPossibleMoveCount(board, light, dark, blank)
        self.assertEqual(result, expectedResult)
        
    def test223_NeitherCanMove(self):
        light = 1
        dark = 2
        blank = 0
        board = [1,1,1,1,1,1,1,1, 
                 1,1,1,1,1,1,1,1,
                 1,1,1,1,1,1,1,1,
                 1,1,1,1,1,1,1,0, 
                 1,1,1,1,1,1,0,0,
                 1,1,1,1,1,1,0,2,
                 1,1,1,1,1,1,1,0,
                 1,1,1,1,1,1,1,1]
        expectedResult = {
            "light": 0,
            "dark": 0
            }
        result = status._getPossibleMoveCount(board, light, dark, blank)
        self.assertEqual(result, expectedResult)
        
