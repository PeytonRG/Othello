from unittest import TestCase
import http.client
from urllib.parse import urlencode
import json
import othello.dispatch as othello 




class MicroserviceTest(TestCase):
    def setUp(self):
        self.PATH = '/othello?'
        self.PORT = 5000
        self.URL = 'localhost'
        self.status = "ok"

        
    def microservice(self, parm = ""):
        '''Issue HTTP Get and return result, which will be JSON string'''
        try:
            theParm = urlencode(parm)
            theConnection = http.client.HTTPConnection(self.URL, self.PORT)
            theConnection.request("GET", self.PATH + theParm)
            theStringResponse = str(theConnection.getresponse().read(), "utf-8")
        except Exception as e:
            theStringResponse = "{'diagnostic': '" + str(e) + "'}"
            
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = theStringResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element], str)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result
        
# Happy path
#    Test that each dispatched operation returns a status element
 
    def test100_010ShouldVerifyInstallOfCreate(self):
        parms = {}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertIn('status', result)
        #self.assertIn('create', result['status'])
 
    def test100_020ShouldVerifyInstallOfNext(self):
        parms = {}
        parms['op'] = 'next'
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertIn('next', result['status'])
        
    def test100_030ShouldVerifyInstallOfPlace(self):
        parms = {}
        parms['op'] = 'place'
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertIn('place', result['status'])
        
    def test100_040ShouldVerifyInstallOfStatus(self):
        parms = {}
        parms['op'] = 'status'
        result = self.microservice(parms)
        self.assertIn('status', result)
        #self.assertIn('status', result['status'])
        
# Sad path
#    Verify status of 
#        1) missing parm
#        2) non-dict parm
#        3) missing "op" keyword
#        4) empty "op" keyword
#        5) invalid op name

    def test100_910ShouldErrOnMissingParm(self):
        result = self.microservice()
        self.assertIn('status', result)
        self.assertEquals(result['status'], othello.ERROR01)
        
    def test100_920ShouldErrOnNoOp(self):
        parms = {}
        parms['board'] = 1
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], othello.ERROR01)
                
    def test100_930ShouldErrOnEmptyOp(self):
        parms = {}
        parms['op'] = 'othello'
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], othello.ERROR03)
        
    def test100_940ShouldErrOnUnknownOp(self):
        parms = {}
        parms['op'] = ''
        result = self.microservice(parms)
        self.assertIn('status', result)
        self.assertEquals(result['status'], othello.ERROR03)
        
# Analysis
# test200 - op=create
# Sad Path Test
    def test200_900ShouldErrOnAboveBoundLight(self):
        parms = {'light':'10'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        
    def test200_905ShouldErrOnBelowBoundLight(self):
        parms = {'light':'-1'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_910ShouldErrOnNonIntegerLight(self):
        parms = {'light':'w'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
    
    def test200_915ShouldErrOnNullLight(self):
        parms = {'light':''}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')

    def test200_920ShouldErrOnAboveBoundDark(self):
        parms = {'dark':'10'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')    
    
    def test200_925ShouldErrOnBelowBoundDark(self):
        parms = {'dark':'-1'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')    
        
    def test200_930ShouldErrOnNonIntegerDark(self):
        parms = {'dark':'d'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')    
    
    def test200_935ShouldErrOnNullDark(self):
        parms = {'dark':''}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_940ShouldErrOnAboveBoundBlank(self):
        parms = {'blank':'10'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
        
    def test200_945ShouldErrOnBelowBoundBlank(self):
        parms = {'blank':'-1'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_950ShouldErrOnNonIntegerBlank(self):
        parms = {'blank':'b'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
        
    def test200_955ShouldErrOnNulBlank(self):
        parms = {'blank':''}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
        
    def test200_960ShouldErrOnAboveBoundSize(self):
        parms = {'size':'17'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_965ShouldErrOnAboveBoundSize(self):
        parms = {'size':'18'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_970ShouldErrOnBelowBoundSize(self):
        parms = {'size':'5'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_975ShouldErrOnBelowBoundSize(self):
        parms = {'size':'4'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_980ShouldErrOnOddSize(self):
        parms = {'size':'9'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_985ShouldErrOnNonIntegerSize(self):
        parms = {'size':'1.2'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_990ShouldErrOnNonNullSize(self):
        parms = {'size':''}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_995ShouldErrOnNonNullSize(self):
        parms = {'size':''}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
        
    def test200_995ShouldErrOnNotUniqueValuesWithNominalLightNominalDarkNominalBlankNominalSize(self):
        parms = {'light':'5', 'dark':'5', 'blank':'0'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_996ShouldErrOnNotUniqueValuesWithNominalLightNominalDarkNominalBlankNominalSize(self):
        parms = {'light':'5', 'dark':'2', 'blank':'5'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
    
    def test200_997ShouldErrOnNotUniqueValuesWithNominalLightNominalDarkNominalBlankNominalSize(self):
        parms = {'light':'1', 'dark':'2', 'blank':'2'}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:') 
        
 
# Happy Path Test   
    def test200_100ShouldReturnValidBoardWithZeroBlankOnSize8by8Matrix(self):  
        parms = {'light':"1", "dark":"2", "blank":"0", "size":"8"}
        tokens = {'light':1, "dark":2, "blank":0}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue(  [0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,1,2,0,0,0,\
                           0,0,0,2,1,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "b11fcf5f9ac9d3b8cea8085208e210182a8d6b73a84028562ab2c87d190b9ada")
    
    def test200_110ShouldReturnValidBoardWithZeroBlankOnSize6by6Matrix(self):  
        parms = {'light':"1", "dark":"2", "blank":"0", "size":"6"}
        tokens = {'light':1, "dark":2, "blank":0}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([0,0,0,0,0,0,
                         0,0,0,0,0,0, 
                         0,0,1,2,0,0, 
                         0,0,2,1,0,0, 
                         0,0,0,0,0,0, 
                         0,0,0,0,0,0],board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b")
           
    def test200_120ShouldReturnValidBoardWithNominalLightDarkBlankAndSize(self):
        parms = {'light':"6", "dark":"5", "blank":"1", "size":"10"}
        tokens = {'light':6, "dark":5, "blank":1}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 6, 5, 1, 1, 1, 1, 
                         1, 1, 1, 1, 5, 6, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "d0f18c5b412ab1dbf89da19baa33cc35f4a7dd0619ce7b7dcb2381d2cb14a412")
        
    def test200_130ShouldReturnValidBoardWithHighBoundLightNominalDarkBlankAndSize(self):
        parms = {'light':"9", "dark":"5", "blank":"1", "size":"10"}
        tokens = {'light':9, "dark":5, "blank":1}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 9, 5, 1, 1, 1, 1, 
                         1, 1, 1, 1, 5, 9, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "723c769319c6529cf8520336232a9e5d281be77df1455c6ceb10a5d1d4733236")
    
    def test200_140ShouldReturnValidBoardWithLowBoundLightNominalDarkBlankAndSize(self):
        parms = {'light':"0", "dark":"5", "blank":"1", "size":"10"}
        tokens = {'light':0, "dark":5, "blank":1}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 0, 5, 1, 1, 1, 1, 
                         1, 1, 1, 1, 5, 0, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "4bd2efa7e0d5f13551f7277950e45b6fcfe7d5159b80823a5dcbdf57abb4d83a")
        
    def test200_150ShouldReturnValidBoardWithMissingLightNominalDarkBlankAndSize(self):
        parms = { "dark":"5", "blank":"3", "size":"10"}
        tokens = {'light':1, "dark":5, "blank":3}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 1, 5, 3, 3, 3, 3, 
                         3, 3, 3, 3, 5, 1, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
                         3, 3, 3, 3, 3, 3, 3, 3, 3, 3], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "f211a92f576794a821bb24f359739b8b42a6a16634005a1e4b32313a6575e2be")
    
    def test200_160ShouldReturnValidBoardWithNominalLightHighBoundDarkNominalBlankAndNominalSize(self):
        parms = { "light":"3","dark":"9", "blank":"4", "size":"10"}
        tokens = {'light':3, "dark":9, "blank":4}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 3, 9, 4, 4, 4, 4, 
                         4, 4, 4, 4, 9, 3, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "a3718ffbc2f822320ee4db10c269a9749859b9952db13ff6b289a6ebd6ce42c6")
    
    def test200_170ShouldReturnValidBoardWithNominalLightLowBoundDarkNominalBlankAndNominalSize(self):
        parms = { "light":"3","dark":"0", "blank":"4", "size":"10"}
        tokens = {'light':3, "dark":0, "blank":4}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue([4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 3, 0, 4, 4, 4, 4, 
                         4, 4, 4, 4, 0, 3, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                         4, 4, 4, 4, 4, 4, 4, 4, 4, 4], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "7bf98e8385a158097f52361dac139bb5882f3eaa48e8146d72d65de5981d2e5e")
        
    def test200_180ShouldReturnValidBoardWithNominalLightMissingDarkNominalBlankAndNominalSize(self):
        parms = { "light":"3", "blank":"4", "size":"10"}
        tokens = {'light':3, "dark":2, "blank":4}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                          4, 4, 4, 4, 3, 2, 4, 4, 4, 4, 
                          4, 4, 4, 4, 2, 3, 4, 4, 4, 4, 
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
                          4, 4, 4, 4, 4, 4, 4, 4, 4, 4], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "71f91a7d487c9e9ad69a43269c6a90c449f97fd93848b8493e47a2f6054e7c82")
        
    def test200_190ShouldReturnValidBoardWithNominalLightAndDarkHighBoundBlankAndNominalSize(self):
        parms = { "light":"3","dark":"4" ,"blank":"9", "size":"10"}
        tokens = {'light':3, "dark":4, "blank":9}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 3, 4, 9, 9, 9, 9, 
                          9, 9, 9, 9, 4, 3, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
                          9, 9, 9, 9, 9, 9, 9, 9, 9, 9], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "5b4c82af0cf6a72ab1938b8e5a3c1ce413b9db583d0f974703954427413021d0")
    
    def test200_200ShouldReturnValidBoardWithNominalLightAndDarkLowBoundBlankAndNominalSize(self):
        parms = { "light":"3","dark":"4" ,"blank":"0", "size":"10"}
        tokens = {'light':3, "dark":4, "blank":0}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue(  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 
                           0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "eeaa1d4229234a1453901319e7f584a337595d6d332a22a76c4aae8888cde9d6")
        
    def test200_210ShouldReturnValidBoardWithNominalLightAndDarkMissingBlankAndNominalSize(self):
        parms = { "light":"3","dark":"4" , "size":"10"}
        tokens = {'light':3, "dark":4, "blank":0}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue(  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 3, 4, 0, 0, 0, 0,
                           0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "eeaa1d4229234a1453901319e7f584a337595d6d332a22a76c4aae8888cde9d6")
    
    def test200_220ShouldReturnValidBoardWithNominalLightAndDarkHighBoundBlankAndNominalSize(self):
        parms = { "light":"3","dark":"4" ,"blank":"5" ,"size":"16"}
        tokens = {'light':3, "dark":4, "blank":5}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5, 5, 3, 4, 5, 5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5, 5, 4, 3, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "682b1bac788017f23b846862ce44f2c3efe03a22f49de36085e0e57fc6957416")
    
    def test200_230ShouldReturnValidBoardWithNominalLightDarkBlankAndLowBoundSize(self):
        parms = { "light":"3","dark":"4" ,"blank":"5" ,"size":"6"}
        tokens = {'light':3, "dark":4, "blank":5}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 
                          5, 5, 3, 4, 5, 5, 
                          5, 5, 4, 3, 5, 5,
                          5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "b87b212e557d1dc1080f1c6e380bab404ae8cffa048b86e649e54c620f0d9c6a")
     
    def test200_240ShouldReturnValidBoardWithNominalLightDarkBlankAndMissingSize(self):
        parms = { "light":"3","dark":"4" ,"blank":"5"}
        tokens = { "light":3,"dark":4 ,"blank":5}
        parms['op'] = 'create'
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [5, 5, 5, 5, 5, 5, 5, 5,
                          5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 3, 4, 5, 5, 5, 
                          5, 5, 5, 4, 3, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5, 
                          5, 5, 5, 5, 5, 5, 5, 5], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "306a2474c8f8b41c9e31af0fe360f9fcaf3531b3b4a1c3624acd8fbc2530b02e")
        
    def test200_250ShouldReturnValidBoardWithDefaultedParameters(self):
        tokens = { "light":1,"dark":2 ,"blank":0}
        parms ={'op': 'create'}
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,1,2,0,0,0,
                          0,0,0,2,1,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "b11fcf5f9ac9d3b8cea8085208e210182a8d6b73a84028562ab2c87d190b9ada")
        
    def test200_250ShouldReturnValidBoardWithDefaultedParametersAndExtraParameterOnInputQuery(self):
        tokens = { "light":1,"dark":2 ,"blank":0}
        parms ={'op': 'create', "extra":"1234"}
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 1, 2, 0, 0, 0,
                          0, 0, 0, 2, 1, 0, 0, 0, 
                          0, 0, 0, 0, 0, 0, 0, 0, 
                          0, 0, 0, 0, 0, 0, 0, 0, 
                          0, 0, 0, 0, 0, 0, 0, 0], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "b11fcf5f9ac9d3b8cea8085208e210182a8d6b73a84028562ab2c87d190b9ada")
        
    def test200_260ShouldReturnValidBoardWithNominalValues(self):
        parms = { "light":"4","dark":"7" ,"blank":"8", "size":"12"}
        parms['op']= 'create'
        tokens = {"light":4,"dark":7 ,"blank":8}
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 4, 7, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 7, 4, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "5ac2ac4b627242b2f6d116fb6c27e240c5d5ced735a886bab9f0569a02d58d01")
        
    def test200_270ShouldReturnValidBoardWithNominalValues(self):
        parms = { "light":"2","dark":"4" ,"blank":"6", "size":"10"}
        parms['op']= 'create'
        tokens = {"light":2,"dark":4 ,"blank":6}
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 2, 4, 6, 6, 6, 6, 
                          6, 6, 6, 6, 4, 2, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
                          6, 6, 6, 6, 6, 6, 6, 6, 6, 6], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "1a2e64dfe37d40dd0050575a14b8f4ac59d991303c898e52b0b0b0ce4b19d9a9")
    
    def test200_280ShouldReturnValidBoardWithNominalValues(self):
        parms = { "light":"1","dark":"3" ,"blank":"7", "size":"14"}
        parms['op']= 'create'
        tokens = {"light":1,"dark":3 ,"blank":7}
        result = self.microservice(parms)
        self.assertEqual(len(result), 4)
        self.assertEquals(result['status'], self.status)
        self.assertIn('board', result)
        board = result['board']
        self.assertTrue( [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 1, 3, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 3, 1, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], board)
        self.assertIn('tokens', result)
        self.assertDictEqual(result['tokens'], tokens)
        self.assertIn('integrity', result)
        self.assertEquals(result['integrity'], "5e9de009d857edb7d772043e9d9e5699b1a9768a78e00133198bdace104c82b2")

# Analysis
# test300 - op=status
# Sad Path Test
    def test300_900ShouldReturnErrorOnAboveBoundLightWithNominalDarkBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='10'
        parms['dark']='2'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,10,2,1,1,1,1,2,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='b71bf3bee30fb8c3caa49752bcf9656870cfbd3bec4e4353e1e491054bf11c2f'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_901ShouldReturnErrorOnBelowBoundLightWithNominalDarkBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='-1'
        parms['dark']='2'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,2,1,1,1,1,2,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='f31631fdc7ba5ecd3096a306dbc7e43a9bc13fa781b91d83c36057f5050a51da'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
        
        
    def test300_902ShouldReturnErrorOnNonIntegerLightWithNominalDarkBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='X'
        parms['dark']='2'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,X,2,1,1,1,1,2,X,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='8959fc376b23af1520014ef3bef1eb4f924ec692bbbcd9f638245bf85fb0a6da'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
        
    def test300_903ShouldReturnErrorOnNullLightWithNominalDarkBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']=''
        parms['dark']='2'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,2,1,1,1,1,2,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='1cc0050055aa122edbb536cc63dfe515e6a55132a42a6c8fa41349ab6e572c6a'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_910ShouldReturnErrorOnAboveBoundDarkWithNominalLightBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='5'
        parms['dark']='10'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,10,1,1,1,1,10,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='e8a244c301df58429d82070942fe05dff389162c0aeec8383e3c82863ae09c62'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
        
    def test300_911ShouldReturnErrorOnBelowBoundDarkWithNominalLightBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='5'
        parms['dark']='-1'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,-1,1,1,1,1,-1,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='301e0f00c1b83b65adc1d4fd5e87aaf7f594aa20842ab1df86a6be2e144367db'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_912ShouldReturnErrorOnNonIntegerDarkWithNominalLightBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='5'
        parms['dark']='1.2'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1.2,1,1,1,1,1.2,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='e62a2ec6eb082391a6a5664b4f4dbd8130e43d6589267b19b831423bfcde4a9d'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_913ShouldReturnErrorOnNullDarkWithNominalLightBlankBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='5'
        parms['dark']=''
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='5d5aeb4a45b57eecf69dcc304664fcf7a6f7c74c86ef9ede14da46ab2d9df242'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_920ShouldReturnErrorOnAboveBoundBlankWithNominalLightDarkBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='10'
        parms['board']='[10,10,10,10,10,10,10,10,10,10,10,10,10,10,1,2,10,10,10,10,2,1,10,10,10,10,10,10,10,10,10,10,10,10,10,10]'
        parms['integrity']='530242aec98aa07d3c025b9101bd5b840527cd9b03302641da18c801d70c37e8'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_921ShouldReturnErrorOnBelowBoundBlankWithNominalLightDarkBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='-1'
        parms['board']='[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,2,-1,-1,-1,-1,2,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]'
        parms['integrity']='2e226315d3fc18cf5771b45ae78bfe7be9510ee98b6e566e382f8a70861c8e7d'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
        
    def test300_922ShouldReturnErrorOnNonIntegerBlankWithNominalLightDarkBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='1E5'
        parms['board']='[1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1,2,1E5,1E5,1E5,1E5,2,1,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5,1E5]'
        parms['integrity']='fe62b7f99befb02e21c50cc755a68ef80fb59d56224b02a1f2888e0830454773'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_923ShouldReturnErrorOnNullBlankWithNominalLightDarkBoardAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']=''
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_930ShouldReturnErrorOnNonSquareBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='9d43a04297202bccc81a13b6857179269c0fe33e5227c6569286d54d82493ba6'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_931ShouldReturnErrorOnNonSquareBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='5'
        parms['blank']='3'
        parms['board']='[3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                        3, 3, 3, 3, 1, 5, 3, 3, 3, 3,\
                        3, 3, 3, 3, 5, 1, 3, 3, 3, 3,\
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,\
                         3, 3, 3, 3, 3, 3, 3, 3, 3 ]'
        parms['integrity']='a35cc9a0976a0932b96bb69be91933399c6441dac47b65d418f1cafc3f99cd12'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
        
    def test300_932ShouldReturnErrorOnNonSquareBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='4'
        parms['dark']='7'
        parms['blank']='8'
        parms['board']='[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 4, 7, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 7, 4, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]'
        parms['integrity']='6c727bb4fe96b7d1deaa0313521a24882cd34449722a6b3f0d5822ccbcf38e7d'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_933ShouldReturnErrorOnOddxOddBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='1e3f8bb2d56c5b4483c9f3dccf7bc16d339534a98020e9a28383aaa219f3e64d'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_934ShouldReturnErrorOnMissingBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['integrity']='1e3f8bb2d56c5b4483c9f3dccf7bc16d339534a98020e9a28383aaa219f3e64d'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_935ShouldReturnErrorOnNullBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']=''
        parms['integrity']='1e3f8bb2d56c5b4483c9f3dccf7bc16d339534a98020e9a28383aaa219f3e64d'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_936ShouldReturnErrorOninvalidBoardWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='0'
        parms['board']='[]'
        parms['integrity']='93dace00194327f65057f7c4c5af301653010d4040c221cf1aa84e9fef15af1a'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
        
    def test300_939ShouldReturnErrorOninvalidBoardSizeWithNominalLightDarkBlankAndIntegrity(self):
        parms={'op':'status'}
        parms['light']='2'
        parms['dark']='3'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,2,3,1,1,3,2,1,1,1,1,1]'
        parms['integrity']='93227ae92ea105c3ceff1f6cd6dee21dc952d8bee43cf41a171026951c6e252a'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)
    
    def test300_940ShouldReturnErrorOnShortIntegrityWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2)    
    
    def test300_941ShouldReturnErrorOnLongIntegrityWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a00'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
    
    def test300_942ShouldReturnErrorOnNonHexIntegrityWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465$'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
    
    def test300_944ShouldReturnErrorOnNonNullIntegrityWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']=''
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
    
    def test300_945ShouldReturnErrorOnNonInvalidIntegrityWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']= "0000000000000000000000000001200000021000000000000000000000000000/1/2/0/2"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
    
    def test300_950ShouldErrOnNotUniqueValuesWhereDarkEqualtoLightWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='2'
        parms['dark']='2'
        parms['blank']='0'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']= "e50f93033edd2b27fd1c54631a4b574e545df9e8c06e0b4f74ca94841a4ab6c4"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
    
    def test300_951ShouldErrOnNotUniqueValuesWhereLightEqualtoBlankWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='1'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']= "c725061d80e342070c231d2b987c476f92b8f3d9e5826c2223cff281562e8e2c"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 

    def test300_952ShouldErrOnNotUniqueValuesWhereDarkEqualtoBlankWithNominalLightDarkBlankAndBoard(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='2'
        parms['board']='[2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2]'
        parms['integrity']= "4edfe0aad5d491d98b8103e4f8f899cd3cef690f6ec3602a16e5a0e0301e8bd6"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
    
#     def test300_953ShouldErrOnNominalLightDarkBlankBoardWithNonLightDarkBlankValues(self):
#         parms={'op':'status'}
#         parms['light']='1'
#         parms['dark']='2'
#         parms['blank']='3'
#         parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
#         parms['integrity']= "b42a70b9f5b1064d1a1c594f466ec6cb1c2383694a8fe9f660d7fb07bcdce637"
#         result = self.microservice(parms)
#         self.assertEqual(len(result), 1)
#         self.assertIn('status', result)
#         self.assertIn(result['status'][0:5], 'error:')
#         self.assertGreater(len(result['status'][5:]), 2) 
        
    def test300_954ShouldErrOnNominalLightDarkBlankBoardWithInvalidIntegrity(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']= "4d5aeb4a45b57eecf69dcc304664fcf7a6f7c74c86ef9ede14da46ab2d9df242"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
        
    def test300_955ShouldErrOnNominalLightDarkBlankBoardWithNonLightDarkBlankTokens(self):
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='3'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']= "c9fd7c0049f79f33e45998064cd1fca01600dd5cdc55cb3bf33169cd07c1905a"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertIn('status', result)
        self.assertIn(result['status'][0:5], 'error:')
        self.assertGreater(len(result['status'][5:]), 2) 
        
        
#Happy Path Test
    def test300_010ShouldReturnStatusOkWithNominalLightDarkBlankBoardAndIntegrity(self):  
        parms = {'light':"1", "dark":"2", "blank":"0"}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)

    # Board Size=8
    def test300_011ShouldReturnStatusOkWithNominalLightDarkBlankBoardAndIntegrity(self): 
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='2'
        parms['blank']='0'
        parms['board']='[0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,1,2,0,0,0,\
                           0,0,0,2,1,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0,\
                           0,0,0,0,0,0,0,0]'
        parms['integrity']= "b11fcf5f9ac9d3b8cea8085208e210182a8d6b73a84028562ab2c87d190b9ada"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    # Board size=10
    def test300_012ShouldReturnStatusOkWithNominalLightDarkBlankBoardAndIntegrity(self): 
        parms={'op':'status'}
        parms['light']='6'
        parms['dark']='5'
        parms['blank']='1'
        parms['board']='[1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 6, 5, 1, 1, 1, 1,\
                         1, 1, 1, 1, 5, 6, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,\
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1]'
        parms['integrity']="d0f18c5b412ab1dbf89da19baa33cc35f4a7dd0619ce7b7dcb2381d2cb14a412"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    #Board Size=12
    def test300_013ShouldReturnStatusOkWithNominalLightDarkBlankBoardAndIntegrity(self): 
        parms={'op':'status'}
        parms['light']='4'
        parms['dark']='7'
        parms['blank']='8'
        parms['board']='[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 4, 7, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 7, 4, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,\
                          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]'
        parms['integrity']='5ac2ac4b627242b2f6d116fb6c27e240c5d5ced735a886bab9f0569a02d58d01'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    
    # Board size=14
    def test300_014ShouldReturnStatusOkWithNominalLightDarkBlankBoardAndIntegrity(self): 
        parms={'op':'status'}
        parms['light']='1'
        parms['dark']='3'
        parms['blank']='7'
        parms['board']='[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 1, 3, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 3, 1, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,\
                          7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]'
        parms['integrity']='5e9de009d857edb7d772043e9d9e5699b1a9768a78e00133198bdace104c82b2'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    
    def test300_015ShouldReturnStatusOkWithNominalLightDarkBlankBoardAndIntegrity(self): 
        parms={'op':'status'}
        parms['light']='3'
        parms['dark']='4'
        parms['blank']='5'
        parms['board']='[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 3, 4, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 4, 3, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
                          5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]'
        parms['integrity']='682b1bac788017f23b846862ce44f2c3efe03a22f49de36085e0e57fc6957416'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    
    def test300_020ShouldReturnStatusOkWithHighBoundLightAndNominalDarkBlankBoardAndIntegrity(self):  
        parms = {'light':"9", "dark":"2", "blank":"0"}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,2,0,0,0,0,2,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='5ab81cb67067273363db989119448a0b878896f7db5c268a50c4ae3062cb3647'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
        
    def test300_021ShouldReturnStatusOkWithLowBoundLightAndNominalDarkBlankBoardAndIntegrity(self):  
        parms = {'light':"0", "dark":"2", "blank":"1"}
        parms['op'] = 'status'
        parms['board']='[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,1,1,1,1,2,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]'
        parms['integrity']='1b7e612b959852acbaf6b55d3f6b8dab2cdc32248a58a89dcf022ae80e5b36de'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    
    def test300_022ShouldReturnStatusOkWithMissingLightAndNominalDarkBlankBoardAndIntegrity(self):  
        parms = {"dark":"2", "blank":"3"}
        parms['op'] = 'status'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
    
    def test300_030ShouldReturnStatusOkWithLowBoundDarkAndNominalLightBlankBoardAndIntegrity(self):  
        parms = {'light':"5", "dark":"0", "blank":"9"}
        parms['op'] = 'status'
        parms['board']='[9,9,9,9,9,9,9,9,9,9,9,9,9,9,5,0,9,9,9,9,0,5,9,9,9,9,9,9,9,9,9,9,9,9,9,9]'
        parms['integrity']='85c972c79b667135f99ad9380f4af4a7495c5b5de3768c9cb36c4bc73f0da08a'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)
        
    def test300_031ShouldReturnStatusOkWithHighBoundDarkAndNominalLightBlankBoardAndIntegrity(self):  
        parms = {'light':"5", "dark":"9", "blank":"3"}
        parms['op'] = 'status'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,5,9,3,3,3,3,9,5,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='34932b7f4bbafed18cf99e367e29407e6aae8b49b2ced711f31e429e7efc2a12'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)   
    
    def test300_032ShouldReturnStatusOkWithMissingDarkAndNominalLightBlankBoardAndIntegrity(self):  
        parms = {'light':"5", "blank":"3"}
        parms['op'] = 'status'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,5,2,3,3,3,3,2,5,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='a348c2dae89e65378fc64d889b1d394819c021b2e4cccb37310bbef9335bb900'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)  
    
    def test300_040ShouldReturnStatusOkWithLowBoundBlankAndNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"5", 'dark':'6',"blank":"0"}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,6,0,0,0,0,6,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='062f219e852404144cd7967bcbac5d5d82c151697d8eacfd8c29779acbc58b19'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status) 
    
    def test300_041ShouldReturnStatusOkWithHighBoundBlankAndNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"5", 'dark':'6',"blank":"9"}
        parms['op'] = 'status'
        parms['board']='[9,9,9,9,9,9,9,9,9,9,9,9,9,9,5,6,9,9,9,9,6,5,9,9,9,9,9,9,9,9,9,9,9,9,9,9]'
        parms['integrity']='5b698f38d9d1c1754df196ee688f3900ceba9d074cb74b5e17c19a197b69bf02'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status) 
    
    def test300_042ShouldReturnStatusOkWithMissingBlankAndNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"5", 'dark':'6'}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,6,0,0,0,0,6,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='062f219e852404144cd7967bcbac5d5d82c151697d8eacfd8c29779acbc58b19'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status) 
        
    def test300_050ShouldReturnStatusOkWithLowBoundSizeAndNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)    
    
    def test300_050ShouldReturnStatusOkWithHighBoundSizeAndNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='5df1fd1ccbd0dc74d65ab00d4d62f2e21c2def95dc47e7c73751986cdb5e8710'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)  
    
    def test300_060ShouldReturnStatusOkWithNominalLightDarkBoardAndIntegrityWhenDarkNextPlayer(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'3'}
        parms['op'] = 'status'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='f01977c17f801c43eeb13fb9f74a49bd0c761db3cdffe01510f47ddd23ab465a'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)   
        
    def test300_061ShouldReturnStatusOkWithNominalLightDarkBoardAndIntegrityWhenlightNextPlayer(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'3'}
        parms['op'] = 'status'
        parms['board']='[3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,2,3,3,3,3,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3]'
        parms['integrity']='66271cbb9037c515e73be3a74a37259a179f2d2861cf4e82130cd579a2141093'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status)   
        
    def test300_070ShouldReturnStatusOkWithNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'
        parms['integrity']='6c3ec0129f5e128f48e2541bd6663a52a825c35f99b9a69d9593f2fc44b0bb4b'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'], self.status) 
        
    def test300_071ShouldReturnStatusDarkWithNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,0,1,1,1,1,0]'
        parms['integrity']='e2f7b8593ebadc126833074a7d8653d3c12c36ab3b7622a9cc6ac5dc1a0d9698'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'],'dark')    
        
    def test300_072ShouldReturnStatusLightWithNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'3'}
        parms['op'] = 'status'
        parms['board']='[2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3]'
        parms['integrity']='7c53df9ff782bbbff544d876f4d69a1d87d5864295c0e4a6bf29e6a7ee5a96fc'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'],'light')    
        
    def test300_073ShouldReturnStatusEndWithNominalLightDarkBoardAndIntegrity(self):  
        parms = {'light':"1", 'dark':'2', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[1,1,1,1,1,1,1,1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0, 1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,2,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1]'
        parms['integrity']='8a1c0659575e8cdd01b2e4ff3f431c845e7e7960279bb7abfaa5465e4a755354'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'],'end')    
        
        
    def test300_074ShouldReturnStatusDarkWithNominalLightDarkBoardAndIntegrity(self):
        parms = {'light':"7", 'dark':'8', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[7, 7, 7, 7, 7, 7, 7, 7,\
                         7, 7, 7, 8, 7, 7, 7, 7,\
                         7, 7, 8, 8, 7, 8, 7, 7,\
                         7, 7, 7, 8, 7, 7, 7, 7,\
                         7, 7, 8, 8, 7, 7, 7, 7,\
                         7, 8, 7, 8, 7, 7, 0, 7,\
                         8, 8, 8, 8, 7, 7, 7, 7,\
                         8, 8, 7, 7, 7, 7, 7, 7]'
        parms['integrity']='44a33eba68c88f813935f9bb7db78a1eda58abbca148b1a7d7b5ca486ed7c704'
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'],'dark')    

    def test300_075ShouldReturnStatusEndWithNominalLightDarkBoardAndIntegrity(self):
        parms = {'light':"1", 'dark':'2', 'blank':'3'}
        parms['op'] = 'status'
        parms['board']='[2,2,2,2,2,2,2,2,\
                         2,2,2,2,2,2,2,1,\
                         2,2,1,2,2,2,1,1,\
                         2,2,2,2,2,1,2,1,\
                         2,2,2,2,1,2,2,1,\
                         2,2,2,2,2,1,2,1,\
                         2,2,1,1,1,2,1,1,\
                         2,1,1,1,1,1,1,1]'
        parms['integrity']='03a013efe054d17707224ae3fd329915ce2784464730a1b53c6e137996829db6'
        #integrityLight="102db9f0896b0d0e3dcdcf1ff4c2c050943cc83462f4e8b36c98bd1a26ee587c"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'],'end')   
    
    def test300_076ShouldReturnStatusLightWithNominalLightDarkBoardAndIntegrity(self):
        parms = {'light':"2", 'dark':'1', 'blank':'0'}
        parms['op'] = 'status'
        parms['board']='[1,2,1,0,0,0,0,0,\
                         1,2,1,0,0,0,0,1,\
                         1,2,1,1,1,1,1,1,\
                         1,2,1,1,1,1,1,1,\
                         1,2,2,1,1,1,0,0,\
                         1,2,1,1,1,1,1,1,\
                         1,2,1,0,1,1,0,0,\
                         1,2,1,1,1,1,0,0]'
        parms['integrity']='8230eb5fd467fd5ea2ae1777221fb17aba2dc540d7a4fc1ff19d67d2515456b4'
        #integrityLight="102db9f0896b0d0e3dcdcf1ff4c2c050943cc83462f4e8b36c98bd1a26ee587c"
        result = self.microservice(parms)
        self.assertEqual(len(result), 1)
        self.assertEquals(result['status'],'light')     
        
        
        
        
        
        
        
        
        
        
        
        
    

        
    