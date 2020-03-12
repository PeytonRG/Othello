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
    
    def setLight(self, light):
        self.inputDictionary["light"] = light
        
    def setDark(self, dark):
        self.inputDictionary["dark"] = dark
        
    def setBlank(self, blank):
        self.inputDictionary["blank"] = blank
        
    def setSize(self, size):
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
        expectedResult = {'board': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'tokens': {'light': 6, 'dark': 5, 'blank': 1}, 'status': 'ok', 'integrity': 'd0f18c5b412ab1dbf89da19baa33cc35f4a7dd0619ce7b7dcb2381d2cb14a412'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
        
    def test020_HighBoundLightNominalDarkBlankSize(self):
        self.setLight(9)
        self.setDark(5)
        self.setBlank(1)
        self.setSize(10)
        expectedResult = {'board': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'tokens': {'light': 9, 'dark': 5, 'blank': 1}, 'status': 'ok', 'integrity': '723c769319c6529cf8520336232a9e5d281be77df1455c6ceb10a5d1d4733236'}
        result = create._create(self.inputDictionary)
        self.assertEqual(result, expectedResult)
