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