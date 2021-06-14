"""
Author: JV
Date: 2021-05-17

Defining the interface for contract interaction
"""

test1_interface = [
    {'inputs': [],
     'name': 'getParameterHash',
     'outputs': [{
         'internalType': 'bytes32',
         'name': 'hash',
         'type': 'bytes32'}],
     'stateMutability': 'view',
     'type': 'function'}]

default_interface = [
    {'inputs': [],
     'name': 'getFundAmount',
     'outputs': [{'internalType': 'uint256',
                  'name': 'fundAmount',
                  'type': 'uint256'}],
     'stateMutability': 'view',
     'type': 'function'},
    {'inputs': [],
     'name': 'getParameterHash',
     'outputs': [{'internalType': 'bytes32',
                  'name': 'hash',
                  'type': 'bytes32'}],
     'stateMutability': 'view',
     'type': 'function'},
    {'inputs': [],
     'name': 'getTarget',
     'outputs': [{'internalType': 'bytes32',
                  'name': 'targetValue',
                  'type': 'bytes32'}],
     'stateMutability':'view',
     'type': 'function'},
    {'inputs': [{'internalType': 'uint256',
                 'name': 'testcase',
                 'type': 'uint256'}],
     'name': 'publishCounterexample',
     'outputs': [],
     'stateMutability': 'nonpayable',
     'type': 'function'},
    {'inputs': [{'internalType': 'uint256',
                 'name': 'testcase',
                 'type': 'uint256'}],
     'name': 'publishProof',
     'outputs': [],
     'stateMutability': 'nonpayable',
     'type': 'function'},
]
