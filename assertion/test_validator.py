"""
Author: JV
Date: 2021-05-02

Unit test of validator
"""
import unittest
from assertion.validator import AssertionValidator


class Test_Assertion_Validator(unittest.TestCase):
    def setUp(self):
        own_address = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        self.av = AssertionValidator(own_address)
    
    def test_message_decode(self):
        msg = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, [[1, 2, 3, 4], [5, 6, 7, 8]]]"
        
        ret_ca, ret_fi, ret_p = self.av._AssertionValidator__extract_message(msg)
        res_ca = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        res_fi = 1
        res_p = [[1, 2, 3, 4], [5, 6, 7, 8]]
        self.assertEqual(res_ca, ret_ca)
        self.assertEqual(res_fi, ret_fi)
        self.assertEqual(res_p, ret_p)
