"""
Author: JV
Date: 2021-04-26

Getting the hash of an parameter 
"""
from web3 import Web3


class ParameterHash:
    __hash = None
    
    def parameter_hash(self, parameter) -> str:
        parameter_hash = '0'
        if type(parameter) == int:  # Parameter
            self.__hash = Web3.solidityKeccak(
                ['uint256'], [parameter])
            parameter_hash =  Web3.toHex(self.__hash)
        elif type(parameter) == list:  # Linear Time Complexity
            self.__hash = Web3.solidityKeccak(
                ['uint256[]'], [parameter])
            parameter_hash =  Web3.toHex(self.__hash)
        elif type(parameter) == tuple:  # Quadratic Time Complexity
            self.__hash = Web3.solidityKeccak(
                ['uint256[]', 'uint256[]'],
                [parameter[0], parameter[1]])
            parameter_hash =  Web3.toHex(self.__hash)
        return parameter_hash
    
    """
    Get integer value of last hash
    """
    def get_int(self):
        if self.__hash is not None:
            return Web3.toInt(self.__hash)
        else:
            return 0
