"""
Author: JV
Date: 2021-05-03

Unit test of functions structure
"""

import unittest
from assertion.functions import FUNCTIONS

class Test_Functions(unittest.TestCase):
    def test_get_function(self):
        ret_function = FUNCTIONS.get_function_by_id(0)
        self.assertTrue(callable(ret_function))
        
        ret_function = FUNCTIONS.get_function_by_name("sorted_array")
        self.assertTrue(callable(ret_function))
        
        ret_function = FUNCTIONS.get_function_by_name("not_in_list")
        self.assertEqual(ret_function, None)
        
        ret = FUNCTIONS.get_id_by_name("sorted_array")
        res = 200
        self.assertEqual(ret, res)
        
        ret = FUNCTIONS.get_id_by_name("not_in_list")
        res = -1
        self.assertEqual(ret, res)
    
    def test_function_groups(self):
        # Parameter
        # ToDo
        
        # Array
        function = FUNCTIONS.get_function_by_id(200) # Sorted Array
        ## Find counterexample
        ret = function([3, 2, 1], 1)
        self.assertTrue(ret)
        
        ## Do not find counterexample
        ret = function([1, 2, 3], 1)
        self.assertFalse(ret)
        
        # Double Array
        function = FUNCTIONS.get_function_by_id(300)
        ## Find counterexample
        ret = function(([4, 5, 6], [1, 2, 3]), (1, 1))
        self.assertTrue(ret)
        
        ## Do not find counterexample
        ret = function(([1, 2, 3], [4, 5, 6]), (1, 1))
        self.assertFalse(ret)
    
    def test_all_functions(self):
        pass  # Todo: Test all function entries