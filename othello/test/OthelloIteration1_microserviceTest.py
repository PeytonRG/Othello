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
        self.assertIn('status', result['status'])
        
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
        print(result)
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

    

        
    