'''
    Created on March 11, 2020
    @author: Peyton Gasink
'''

from unittest import TestCase
import othello.create as create
import json

class CreateTest(TestCase):
    
    def setUp(self):
        self.nominalLight = 1
        self.nominalDark = 2
        self.nominalBlank = 0
        self.nominalSize = 8
        self.errorValue = "error:"
        self.errorKey = "error"
        self.inputDictionary = {}
        
    def tearDown(self):
        self.inputDictionary = {}
    
    def setLight(self, light = None):
        self.inputDictionary["light"] = light
        
    def setDark(self, dark = None):
        self.inputDictionary["dark"] = dark
        
    def setBlank(self, blank = None):
        self.inputDictionary["blank"] = blank
        
    def setSize(self, size = None):
        self.inputDictionary["size"] = size
        
    # Unit Tests
    def test210_ShouldReturnOutputDictionary(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        result = create._create(self.inputDictionary)
        self.assertIsInstance(result, dict)
        
    def test220_ShouldReturnBoardWithLengthEqualsSizeSquared(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        expectedResult = self.inputDictionary["size"]**2
        result = create._create(self.inputDictionary)
        self.assertEqual(len(result["board"]), expectedResult)
        
    def test230_ShouldReturnCorrectBoardKeyValuePair(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        expectedResult = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0, 0,0,0,1,2,0,0,0, 
                          0,0,0,2,1,0,0,0, 0,0,0,0,0,0,0,0, 
                          0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0]
        result = create._create(self.inputDictionary)
        self.assertEqual(result["board"], expectedResult)
        
    def test240_ShouldReturnCorrectTokenKeyValuePair(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        expectedResult = {'light': 1,'dark': 2, 'blank': 0}
        result = create._create(self.inputDictionary)
        self.assertEqual(result["tokens"], expectedResult)
        
    def test250_ShouldReturnCorrectIntegrityKeyValuePair(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        expectedResult = 'b11fcf5f9ac9d3b8cea8085208e210182a8d6b73a84028562ab2c87d190b9ada'
        result = create._create(self.inputDictionary)
        self.assertEqual(result["integrity"], expectedResult)
    
    def test260_ShouldReturnStatusKeyValuePairWithStringValue(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        result = create._create(self.inputDictionary)
        self.assertIsInstance(result["status"], str)
    
# Happy Path Acceptance Tests
    def test010_AllParamsNominal(self):
        self.setLight(6)
        self.setDark(5)
        self.setBlank(1)
        self.setSize(10)
        expectedResult = {'board': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 6, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1], 
                                    'tokens': {'light': 6, 'dark': 5, 
                                               'blank': 1}, 'status': 'ok', 
                                    'integrity': 'd0f18c5b412ab1dbf89da19ba' +
                                    'a33cc35f4a7dd0619ce7b7dcb2381d2cb14a412'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test020_HighBoundLightNominalDarkBlankSize(self):
        self.setLight(9)
        self.setDark(5)
        self.setBlank(1)
        self.setSize(10)
        expectedResult = {'board': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 9, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 9, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1], 
                                    'tokens': {'light': 9, 'dark': 5, 
                                               'blank': 1}, 'status': 'ok', 
                                    'integrity': '723c769319c6529cf85203362' +
                                    '32a9e5d281be77df1455c6ceb10a5d1d4733236'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
    
    def test021_LowBoundLightNominalDarkBlankSize(self):
        self.setLight(0)
        self.setDark(5)
        self.setBlank(1)
        self.setSize(10)
        expectedResult = {'board': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 0, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 0, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                    1, 1], 
                                    'tokens': {'light': 0, 'dark': 5, 
                                               'blank': 1}, 'status': 'ok', 
                                    'integrity': '4bd2efa7e0d5f13551f727795' +
                                    '0e45b6fcfe7d5159b80823a5dcbdf57abb4d83a'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test022_MissingLightNominalDarkBlankSize(self):
        self.setDark(5)
        self.setBlank(3)
        self.setSize(10)
        expectedResult = {'board': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                                    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                                    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                                    3, 3, 1, 5, 3, 3, 3, 3, 3, 3, 3, 3, 5, 1, 
                                    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                                    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                                    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                                    3, 3], 
                                    'tokens': {'light': 1, 'dark': 5, 
                                               'blank': 3}, 'status': 'ok', 
                                    'integrity': 'f211a92f576794a821bb24f35' +
                                    '9739b8b42a6a16634005a1e4b32313a6575e2be'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test030_HighBoundDarkNominalLightBlankSize(self):
        self.setLight(3)
        self.setDark(9)
        self.setBlank(4)
        self.setSize(10)
        expectedResult = {'board': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 3, 9, 4, 4, 4, 4, 4, 4, 4, 4, 9, 3, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4], 
                                    'tokens': {'light': 3, 'dark': 9, 
                                               'blank': 4}, 'status': 'ok', 
                                    'integrity': 'a3718ffbc2f822320ee4db10c' +
                                    '269a9749859b9952db13ff6b289a6ebd6ce42c6'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test031_LowBoundDarkNominalLightBlankSize(self):
        self.setLight(3)
        self.setDark(0)
        self.setBlank(4)
        self.setSize(10)
        expectedResult = {'board': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 3, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 3, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4], 
                                    'tokens': {'light': 3, 'dark': 0, 
                                               'blank': 4}, 'status': 'ok', 
                                    'integrity': '7bf98e8385a158097f52361da' +
                                    'c139bb5882f3eaa48e8146d72d65de5981d2e5e'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test032_MissingDarkNominalLightBlankSize(self):
        self.setLight(3)
        self.setBlank(4)
        self.setSize(10)
        expectedResult = {'board': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 3, 2, 4, 4, 4, 4, 4, 4, 4, 4, 2, 3, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                                    4, 4], 
                                    'tokens': {'light': 3, 'dark': 2, 
                                               'blank': 4}, 'status': 'ok', 
                                    'integrity': '71f91a7d487c9e9ad69a43269' +
                                    'c6a90c449f97fd93848b8493e47a2f6054e7c82'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test040_HighBoundBlankNominalLightDarkSize(self):
        self.setLight(3)
        self.setDark(4)
        self.setBlank(9)
        self.setSize(10)
        expectedResult = {'board': [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                                    9, 9, 3, 4, 9, 9, 9, 9, 9, 9, 9, 9, 4, 3, 
                                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                                    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                                    9, 9], 
                                    'tokens': {'light': 3, 'dark': 4, 
                                               'blank': 9}, 'status': 'ok', 
                                    'integrity': '5b4c82af0cf6a72ab1938b8e5' +
                                    'a3c1ce413b9db583d0f974703954427413021d0'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test041_LowBoundBlankNominalLightDarkSize(self):
        self.setLight(3)
        self.setDark(4)
        self.setBlank(0)
        self.setSize(10)
        expectedResult = {'board': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0], 
                                    'tokens': {'light': 3, 'dark': 4, 
                                               'blank': 0}, 'status': 'ok', 
                                    'integrity': 'eeaa1d4229234a1453901319e' +
                                    '7f584a337595d6d332a22a76c4aae8888cde9d6'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test042_MissingBlankNominalLightDarkSize(self):
        self.setLight(3)
        self.setDark(4)
        self.setSize(10)
        expectedResult = {'board': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0], 
                                    'tokens': {'light': 3, 'dark': 4, 
                                               'blank': 0}, 'status': 'ok', 
                                    'integrity': 'eeaa1d4229234a1453901319e' +
                                    '7f584a337595d6d332a22a76c4aae8888cde9d6'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test050_HighBoundSizeNominalLightDarkBlank(self):
        self.setLight(3)
        self.setDark(4)
        self.setBlank(5)
        self.setSize(16)
        expectedResult = {'board': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 3, 4, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5], 
                                    'tokens': {'light': 3, 'dark': 4, 
                                               'blank': 5}, 'status': 'ok', 
                                    'integrity': '682b1bac788017f23b846862c' +
                                    'e44f2c3efe03a22f49de36085e0e57fc6957416'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test051_LowBoundSizeNominalLightDarkBlank(self):
        self.setLight(3)
        self.setDark(4)
        self.setBlank(5)
        self.setSize(6)
        expectedResult = {'board': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    3, 4, 5, 5, 5, 5, 4, 3, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5], 
                                    'tokens': {'light': 3, 'dark': 4, 
                                               'blank': 5}, 'status': 'ok', 
                                    'integrity': 'b87b212e557d1dc1080f1c6e3' +
                                    '80bab404ae8cffa048b86e649e54c620f0d9c6a'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test052_MissingSizeNominalLightDarkBlank(self):
        self.setLight(3)
        self.setDark(4)
        self.setBlank(5)
        expectedResult = {'board': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 
                                    4, 5, 5, 5, 5, 5, 5, 4, 3, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                                    5, 5, 5, 5, 5, 5, 5, 5], 
                                    'tokens': {'light': 3, 'dark': 4, 
                                               'blank': 5}, 'status': 'ok', 
                                    'integrity': '306a2474c8f8b41c9e31af0fe' +
                                    '360f9fcaf3531b3b4a1c3624acd8fbc2530b02e'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test060_AllParametersDefaulted(self):
        expectedResult = {'board': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
                                    2, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0], 
                                    'tokens': {'light': 1, 'dark': 2, 
                                               'blank': 0}, 'status': 'ok', 
                                    'integrity': 'b11fcf5f9ac9d3b8cea808520' +
                                    '8e210182a8d6b73a84028562ab2c87d190b9ada'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test070_ShouldIgnoreExtraneousParameters(self):
        self.inputDictionary["extra"] = 1234
        expectedResult = {'board': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
                                    2, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0, 0, 0, 0], 
                                    'tokens': {'light': 1, 'dark': 2, 
                                               'blank': 0}, 'status': 'ok', 
                                    'integrity': 'b11fcf5f9ac9d3b8cea808520' +
                                    '8e210182a8d6b73a84028562ab2c87d190b9ada'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
# Sad Path Acceptance Tests
    def test900_AboveBoundLightNominalDarkBlankSize(self):
        self.setLight(10)
        expectedResult = {'status': 'error: The value for light tokens is '
                          + 'above the accepted range.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test901_BelowBoundLightNominalDarkBlankSize(self):
        self.setLight(-1)
        expectedResult = {'status': 'error: The value for light tokens is '
                          + 'below the accepted range.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test902_NonIntegerLightNominalDarkBlankSize(self):
        self.setLight("w")
        expectedResult = {'status': 'error: The value for light tokens must '
                          + 'be an integer.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test903_NullLightNominalDarkBlankSize(self):
        self.setLight()
        expectedResult = {'status': 'error: The value for light tokens must '
                          + 'be an integer.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test910_AboveBoundDarkNominalLightBlankSize(self):
        self.setDark(10)
        expectedResult = {'status': 'error: The value for dark tokens is '
                          + 'above the accepted range.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test911_BelowBoundDarkNominalLightBlankSize(self):
        self.setDark(-1)
        expectedResult = {'status': 'error: The value for dark tokens is '
                          + 'below the accepted range.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test912_NonIntegerDarkNominalLightBlankSize(self):
        self.setDark("d")
        expectedResult = {'status': 'error: The value for dark tokens must '
                          + 'be an integer.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test913_NullDarkNominalLightBlankSize(self):
        self.setDark()
        expectedResult = {'status': 'error: The value for dark tokens must '
                          + 'be an integer.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test920_AboveBoundBlankNominalLightDarkSize(self):
        self.setBlank(10)
        expectedResult = {'status': 'error: The value for blank spaces is '
                          + 'above the accepted range.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test921_BelowBoundBlankNominalLightDarkSize(self):
        self.setBlank(-1)
        expectedResult = {'status': 'error: The value for blank spaces is '
                          + 'below the accepted range.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test922_NonIntegerBlankNominalLightDarkSize(self):
        self.setBlank("b")
        expectedResult = {'status': 'error: The value for blank spaces must '
                          + 'be an integer.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
    
    def test923_NullBlankNominalLightDarkSize(self):
        self.setBlank()
        expectedResult = {'status': 'error: The value for blank spaces must '
                          + 'be an integer.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test930_AboveBoundSizeNominalLightDarkBlank(self):
        self.setSize(17)
        expectedResult = {'status': 'error: The value for board size must '
                          + 'be an even integer in the range [6, 16].'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test931_BelowBoundSizeNominalLightDarkBlank(self):
        self.setSize(5)
        expectedResult = {'status': 'error: The value for board size must '
                          + 'be an even integer in the range [6, 16].'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test932_OddSizeNominalLightDarkBlank(self):
        self.setSize(9)
        expectedResult = {'status': 'error: The value for board size must '
                          + 'be an even integer in the range [6, 16].'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test933_NonIntegerSizeNominalLightDarkBlank(self):
        self.setSize(1.2)
        expectedResult = {'status': 'error: The value for board size must '
                          + 'be an even integer in the range [6, 16].'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test934_NullSizeNominalLightDarkBlank(self):
        self.setSize()
        expectedResult = {'status': 'error: The value for board size must '
                          + 'be an even integer in the range [6, 16].'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
    
    def test940_NominalLightDarkEqualsLightNominalBlankSize(self):
        self.setLight(5)
        self.setDark(5)
        self.setBlank(0)
        expectedResult = {'status': 'error: The values of light, dark, '
                          + 'and blank must be unique.'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
