from unittest import TestCase
import othello.create as create
import json

class CreateTest(TestCase):
    
    def setUp(self):
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