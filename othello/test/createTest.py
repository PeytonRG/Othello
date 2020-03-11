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
    def test510_ShouldReturnOutputDictionary(self):
        self.setLight(1)
        self.setDark(2)
        self.setBlank(0)
        self.setSize(8)
        result = create._create(self.inputDictionary)
        self.assertIsInstance(result, dict)
        
    

