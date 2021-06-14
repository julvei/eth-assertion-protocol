"""
Author: JV
Date: 2021-05-03

Unit test of assertion message
"""
import unittest
from helper.assertion_message import pack_message, unpack_message

class Test_Assertion_Message(unittest.TestCase):
    def test_pack_message(self):
        address = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        function_id = 1
        parameter1 = 10000
        parameter2 = [1, 2, 3, 4]
        parameter3 = [[1, 2, 3, 4], [5, 6, 7, 8]]
        
        # Parameter
        ret = pack_message(address, function_id, parameter1)
        res = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, 10000]"
        self.assertEqual(ret, res)
        
        # Array
        ret = pack_message(address, function_id, parameter2)
        res = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, [1, 2, 3, 4]]"
        self.assertEqual(ret, res)
        
        # Double Array
        ret = pack_message(address, function_id, parameter3)
        res = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, [[1, 2, 3, 4], [5, 6, 7, 8]]]"
        self.assertEqual(ret, res)
    
    def test_unpack_message(self):
        msg1 = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, 10000]"
        msg2 = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, [1, 2, 3, 4]]"
        msg3 = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, [[1, 2, 3, 4], [5, 6, 7, 8]]]"
        
        # Parameter
        ret_ca, ret_fi, ret_p = unpack_message(msg1)
        res_ca = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        res_fi = 1
        res_p = 10000
        self.assertEqual(res_ca, ret_ca)
        self.assertEqual(res_fi, ret_fi)
        self.assertEqual(res_p, ret_p)
        self.assertIsInstance(ret_p, int)
        
        # Array
        ret_ca, ret_fi, ret_p = unpack_message(msg2)
        res_ca = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        res_fi = 1
        res_p = [1, 2, 3, 4]
        self.assertEqual(res_ca, ret_ca)
        self.assertEqual(res_fi, ret_fi)
        self.assertEqual(res_p, ret_p)
        for par in ret_p:
            self.assertIsInstance(par, int)
        
        # Double Array
        ret_ca, ret_fi, ret_p = unpack_message(msg3)
        res_ca = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        res_fi = 1
        res_p = [[1, 2, 3, 4], [5, 6, 7, 8]]
        self.assertEqual(res_ca, ret_ca)
        self.assertEqual(res_fi, ret_fi)
        self.assertEqual(res_p, ret_p)
        for arr in ret_p:
            for par in arr:
                self.assertIsInstance(par, int)
    
    def test_pack_unpack(self):
        address = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
        function_id = 1
        parameter = [[1, 2, 3, 4], [5, 6, 7, 8]]
        message = "['0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB', 1, [[1, 2, 3, 4], [5, 6, 7, 8]]]"
        
        # Pack -> Unpack
        ret_message = pack_message(address, function_id, parameter)
        ret_address, ret_function_id, ret_parameter = unpack_message(ret_message)
        self.assertEqual(ret_address, address)
        self.assertEqual(ret_function_id, function_id)
        self.assertEqual(ret_parameter, parameter)
        
        # Unpack -> Pack
        ret_address, ret_function_id, ret_parameter = unpack_message(message)
        ret_message = pack_message(ret_address, ret_function_id, ret_parameter)
        self.assertEqual(ret_message, message)
