"""
Author: JV
Date: 2021-05-03

Base node for common functionalities between initiator
and validator.
"""
from web3 import Web3
import os
os.environ["WEB3_INFURA_PROJECT_ID"] = "8994c40415ea4b1db71ebcd9ec19ba67"
os.environ["WEB3_INFURA_API_SECRET"] = "d9b6ef9b967d48878962573a9a17b694"
from web3.auto.infura import ropsten
from helper.parameter_hash import ParameterHash
from web3.gas_strategies.time_based import fast_gas_price_strategy


class BaseNode:
    _w3 = None
    _account_address = None
    _ph = None
    _infura = False
    _debug = True
    _waku = True
    _verbose = False
    
    def __init__(self, account_address : str = None, infura : bool = False,
                 debug : bool = True, waku : bool = True, verbose = False):
        if account_address is not None:
            self.set_account_address(account_address)
        self._infura = infura  # Running in test mode
        self._debug = debug  # Running in debug mode
        self._waku = waku  # Enable waku protocol
        self._ph = ParameterHash()
        self._verbose = verbose
    
    """
    Connecting to a geth instance via ipc
    A geth node must be started and the ipc path must be known
    """
    def connect_to_client(self, ipc_path : str = '~/.ethereum/ropsten/geth.ipc',
                          address_cnt : int = 0) -> bool:
        try:
            if not self._infura:
                self._w3 = Web3(Web3.IPCProvider(ipc_path))
            else:
                self._w3 = ropsten.w3
            
            # Check if connected
            if self._w3.isConnected() == False:
                raise
            
            # Defining gas strategy
            self._w3.eth.set_gas_price_strategy(fast_gas_price_strategy)
            
            # Setting first account as account address
            if (self._account_address is None) and (not self._infura):
                self.set_account_address(
                    self._w3.geth.personal.list_accounts()[address_cnt])
            elif (self._account_address is None) and (self._infura):
                print("E: Please set account address for infura manually!")
                raise
            
            # Defining default address for requests
            self._w3.eth.default_account = self._account_address
            
            if self._verbose:
                print("Successfully connected!")
                print("|- Account address:", self._account_address)
            
                if self._infura:
                    print("|- Connected to Infura remote!")
                if self._debug:
                    print("|- Running in debug mode!")
                if not self._waku:
                    print("|- Waku disabled!")
            
            return True
        
        except:
            print("E: Connecting to provider went wrong!")
            return False
    
    def calculate_parameter_hash(self, parameter):
        return self._ph.parameter_hash(parameter)
    
    # Interact with the blockchain
    def get_balance(self):
        if self._w3 is None:
            print("E: Please connect first to an ethereum client!")
        else:
            balance = self._w3.eth.get_balance(self._account_address)
            if self._verbose:
                print("|- Account balance: %f Ether" % Web3.fromWei(balance, 'ether'))
            return balance
    
    # Getter and setters
    def get_account_address(self) -> str:
        return self._account_address
    
    def set_account_address(self, address : str):
        self._account_address = Web3.toChecksumAddress(address)
        if self._w3 is not None:
            self._w3.eth.default_account = self._account_address
    
    def switch_debug(self, debug : bool):
        self._debug = debug
