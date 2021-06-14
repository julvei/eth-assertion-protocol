"""
Author: JV
Date: 2021-04-25

Unit test of reward checker
"""
import unittest
from check_local.reward_checker import RewardChecker


class Test_Reward_Checker(unittest.TestCase):
    def setUp(self):
        self.simple_test_function = lambda parameter, testcase: testcase == parameter
        self.my_address = '0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'
        self.current_target = '0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        self.rc = RewardChecker(self.my_address, self.current_target, self.simple_test_function, 7)
    
    def test_getters_and_setters(self):
        # Evaluation Function
        newEvaluationFunction = lambda parameter, testcase: testcase == 3
        self.rc.setEvaluationFunction(newEvaluationFunction)
        ret = self.rc.checkRange(0, 4)
        self.assertTrue(ret)
        ret = self.rc.getResults()
        res = [('target_hash', 1), ('target_hash', 2), ('counterexample', 3)]
        self.assertEqual(ret, res)
        
        # Target
        newTarget = '0xff'
        self.rc.setTarget(newTarget)
        ret = self.rc.getTarget()
        self.assertEqual(newTarget, ret)
        
        # Address
        newAddress = '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'
        self.rc.setAddress(newAddress)
        ret = self.rc.getAddress()
        self.assertEqual(newAddress, ret)
        
        # Parameter
        newParameter = list(range(1, 16))
        self.rc.setParameter(newParameter)
        ret = self.rc.getParameter()
        self.assertEqual(newParameter,ret)
    
    def test_helper_functions(self):
        stringValue = "0x42"
        ret = self.rc._RewardChecker__string_for_comparison(stringValue)
        self.assertEqual(0x42, ret)
        
        ret = self.rc._RewardChecker__back_to_string(ret)
        self.assertEqual(stringValue, ret)
    
    def test_check_base(self):
        ret = self.rc.checkRange(0, 8)
        self.assertTrue(ret)
        
        ret = self.rc.getResults()
        res = [('target_hash', 1), ('target_hash', 2), ('target_hash', 5), ('target_hash', 6), ('counterexample', 7)]
        self.assertEqual(ret, res)
        
        ret = self.rc.getTargetHashes()
        res = ['0x7d0c9bbf9312c318257b684d86f0aa359245fde5214229810220763c28f655fe',
               '0x59729de5adb27d4bd22c7c8f0ba80b29d40e255d47310cb2bc384a79d978347a',
               '0x74b496a47fe7ddd31a0422d03974e35f5b9ff4924e10d85a8c44fe813d213e60',
               '0x717e2c1973869564b01272e94ae8e09e54c5b83a5862844a0c1cf0d06cf0e99']
        self.assertEqual(ret, res)
        
        ret = self.rc.checkRange(0, 0)
        self.assertFalse(ret)
    
    def test_check_equal(self):
        ret = self.rc.checkFast(0, 100)
        self.assertTrue(ret)
        
        ret = self.rc.getResults()
        res = [('target_hash', 1)]
        self.assertEqual(ret, res)
        
        ret = self.rc.getTargetHashes()
        res = ['0x7d0c9bbf9312c318257b684d86f0aa359245fde5214229810220763c28f655fe']
        self.assertEqual(ret, res)
        
    def test_hash_after_counterexample(self):
        ret = self.rc.checkRange(6, 11)
        self.assertTrue(ret)
        
        ret = self.rc.getResults()
        res = [('target_hash', 6), ('counterexample', 7), ('target_hash', 10)]
        self.assertEqual(ret, res)
        
        ret = self.rc.getTargetHashes()
        res = ['0x717e2c1973869564b01272e94ae8e09e54c5b83a5862844a0c1cf0d06cf0e99',
               '0x1353fd4837199f71143f5cc931c2786299e65e28266e74a0411f2f04df022eaa']
        self.assertEqual(ret, res)
    
    def test_hash_and_counterexample(self):
        self.rc.setAddress('0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2')
        ret = self.rc.checkRange(6, 9)
        self.assertTrue(ret)
        
        ret = self.rc.getResults()
        res = [('target_hash', 6), ('counterexample', 7), ('target_hash', 7), ('target_hash', 8)]
        self.assertEqual(ret, res)
        
        ret = self.rc.getTargetHashes()
        res = ['0x765a159702f13f8f1c5062d2f2fe97276efda95c00f9ee9156d72b2c99cbf278',
               '0x70cbc4d86b17d62b1beaf12ef06428b2d508f4d8e0dedc66ff2ccf51dd48ee44',
               '0x3dbad79332185d1b8072b7575687408f14527075c6d4999bccd89785e269f0d5']
        self.assertEqual(ret, res)
    
    def test_array_parameter(self):
        def sorted_array(parameter, testcase):
            return parameter[testcase] > parameter[testcase+1]
        self.rc.setEvaluationFunction(sorted_array)
        
        parameter = list(range(1, 76))
        parameter[62] = 65
        self.rc.setParameter(parameter)
        
        self.rc.setAddress('0xdD870fA1b7C4700F2BD7f44238821C26f7392148')
        self.rc.setTarget('0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        
        ret = self.rc.checkRange(0, len(parameter)-1)
        self.assertTrue(ret)
        
        ret = self.rc.getResults()
        res = [('target_hash', 14), ('counterexample', 62)]
        self.assertEqual(ret, res)
        
    
    def test_double_array_parameter(self):
        def two_arrays(parameter, testcase):
            return parameter[0][testcase[0]] >= parameter[1][testcase[1]]
        self.rc.setEvaluationFunction(two_arrays)
        
        parameter1 = list(range(1, 46))
        parameter2 = list(range(1001, 1046))
        parameter2[41] = 45
        parameter = (parameter1, parameter2)
        min_val = (0, 0)
        max_val = (len(parameter1), len(parameter2))
        self.rc.setParameter(parameter)
        
        self.rc.setAddress('0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB')
        self.rc.setTarget('0x007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        
        
        ret = self.rc.checkRange(min_val, max_val)
        self.assertTrue(ret)
        ret = self.rc.getResults()
        res = [('target_hash', (13, 13)), ('target_hash', (13, 39)), ('target_hash', (15, 35)), ('target_hash', (37, 5)), ('counterexample', (44, 41))]
        self.assertEqual(ret, res)


if __name__ == '__main__':
    unittest.main()
