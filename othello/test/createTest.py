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
        #self.solutionKey = "create"
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
        
#     def test220_ShouldReturnCorrectBoardKeyValuePair(self):
#         self.setLight(1)
#         self.setDark(2)
#         self.setBlank(0)
#         self.setSize(8)
#         result = create._create(self.inputDictionary)
#         self.assertIsInstance(result, dict)
    
# Happy Path Acceptance Tests
#     def test010_AllParamsNominal(self):
#         self.setLight(6)
#         self.setDark(5)
#         self.setBlank(1)
#         self.setSize(10)
#         expectedResult = {'board': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 5, 1, 1, 1, 1, 1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'tokens': {'light': 6, 'dark': 5, 'blank': 1}, 'status': 'ok', 'integrity': 'd0f18c5b412ab1dbf89da19baa33cc35f4a7dd0619ce7b7dcb2381d2cb14a412'}
#         result = create._create(self.inputDictionary)
#         self.assertEqual(result, expectedResult)
