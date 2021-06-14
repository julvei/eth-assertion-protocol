"""
Author: JV
Date: 2021-04-26

Unit test of parameter_hash
"""
import unittest
from helper.parameter_hash import ParameterHash


class Test_Parameter_Hash(unittest.TestCase):
    def setUp(self):
        self.ph = ParameterHash()
    
    def test_variable(self):
        parameter = 1
        res = '0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6'
        ret = self.ph.parameter_hash(parameter)
        self.assertEqual(res, ret)
        
        parameter = 5
        res = '0x036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db0'
        ret = self.ph.parameter_hash(parameter)
        self.assertEqual(res, ret)
        
        # Test integer function
        res = int('0x036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db0', 16)
        ret = self.ph.get_int()
        self.assertEqual(res, ret)
    
    def test_array(self):
        parameter = [1, 2, 3]
        res = '0x6e0c627900b24bd432fe7b1f713f1b0744091a646a9fe4a65a18dfed21f2949c'
        ret = self.ph.parameter_hash(parameter)
        self.assertEqual(res, ret)
        
        parameter = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        res = '0x00a74364039a6f7dd7eb710e0439e15996a5c32ad2976ac76d18e026b8f53de3'
        ret = self.ph.parameter_hash(parameter)
        self.assertEqual(res, ret)
    
    def test_other_type(self):
        parameter = 1.0
        res = '0'
        ret = self.ph.parameter_hash(parameter)
        self.assertEqual(res, ret)
        
        # Test integer function
        self.assertEqual(self.ph.get_int(), 0)
