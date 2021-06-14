"""
Author: JV
Date: 2021-04-14

Checks locally if an proof eligible for obtaining
a reward has been found.

Contract code:
    [...]
    struct Proof {
        address payable[] sender_address;
        uint[] parameter;
        uint size;
    }
    Proof proofs;
    [...]
    bool comparison = (proofs.parameter[i] != 5);
    bytes32 hash = keccak256(abi.encodePacked(proofs.sender_address[i], proofs.parameter[i], comparison));
    [...]
"""
from web3 import Web3


class RewardChecker:
    __address = ""
    __target = 0
    __parameter = None
    __target_hashes = []
    __evaluation_function = None
    __results = []

    def __init__(self, address: str, target: str,
                 evaluation_function, parameter):
        self.__address = address
        self.__target = self.__string_for_comparison(target)
        self.__evaluation_function = evaluation_function
        self.__parameter = parameter

    """
    Searches for all counterexamples and hashes
    """
    def checkRange(self, min_val, max_val,
                   halt: bool = False) -> bool:
        self.__results = []
        self.__target_hashes = []
        
        if type(min_val) is int: # Single parameter
            for i in range(min_val, max_val):
                if self.__check(i, halt):
                    return True
        elif type(min_val) is tuple: # Multiple parameter
            for i in range(min_val[0], max_val[0]):
                for j in range(min_val[1], max_val[1]):
                    if self.__check((i, j), halt):
                        return True
        else:
            raise TypeError
        
        # Some hashes or counterexamples have been found
        if len(self.__results) > 0:
            return True
        else:
            return False
    
    """
    One checking function for both cases:
    single and multiple parameter
    """
    def __check(self, testcase, halt):
        evaluation = self.__checkCounterexample(testcase)
        if evaluation:
            self.__results.append(('counterexample', testcase))
            if halt:
                return True
        if self.__checkHash(testcase, evaluation):
            self.__results.append(('target_hash', testcase))
            if halt:
                return True

    """
    Searches for the first counterexample
    or hash in the search space
    """
    def checkFast(self, min_val, max_val) -> bool:
        return self.checkRange(min_val, max_val, True)

    def __checkCounterexample(self, testcase) -> bool:
        return self.__evaluation_function(self.__parameter, testcase)
    
    def __checkHash(self, testcase, evaluation: bool) -> bool:
        if type(self.__parameter) is int:
            hash_val = Web3.toHex(Web3.solidityKeccak(
                ['address', 'uint256', 'uint256', 'bool'],
                [self.__address, testcase, self.__parameter,
                 evaluation]))
        elif type(testcase) is int:
            hash_val =  Web3.toHex(Web3.solidityKeccak(
                ['address', 'uint256', 'uint256', 'bool'],
                [self.__address, testcase, self.__parameter[testcase],
                 evaluation]))
        elif type(testcase) is tuple:
            hash_val =  Web3.toHex(Web3.solidityKeccak(
                ['address', 'uint256', 'uint256', 'uint256', 'uint256', 'bool'],
                [self.__address, testcase[0], testcase[1],
                 self.__parameter[0][testcase[0]], self.__parameter[1][testcase[1]],
                 evaluation]))
        else:
            raise TypeError
        
        hash_val = self.__string_for_comparison(hash_val)
        
        if hash_val < self.__target:
            self.__target_hashes.append(self.__back_to_string(hash_val))
            return True
        
        return False
    
    """
    When finished results and hashes can be gathered with this functions
    """
    def getTargetHashes(self):
        return self.__target_hashes
    
    def getResults(self):
        return self.__results
    
    """
    Some helper functions
    """
    def __string_for_comparison(self, string_val: str):
        integer_val = int(string_val, 16)
        return integer_val
    
    def __back_to_string(self, value):
        return str(hex(value))
    
    """
    Some setter and getter functions for the parameters
    """
    def setTarget(self, target: str):
        self.__target = self.__string_for_comparison(target)

    def getTarget(self):
        return self.__back_to_string(self.__target)

    def setAddress(self, address: str):
        self.__address = address

    def getAddress(self):
        return self.__address
    
    def setEvaluationFunction(self, evaluation_function):
        self.__evaluation_function = evaluation_function
        
    def setParameter(self, parameter):
        self.__parameter = parameter
        
    def getParameter(self):
        return self.__parameter

