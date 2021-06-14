"""
Author: JV
Date: 2021-04-26

Providing the assertion initiator functionalities

1. Compile Contract
2. Publish Contract
3. Pay Fund
4. Publish Parameter Hash
5. Send Assertion Challenge
6. Publish Transaction
"""
# Includes
import os, sys
from _pydecimal import Decimal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess

from web3 import Web3
from solcx import compile_source
from assertion.base_node import BaseNode
from assertion.functions import FUNCTIONS
from helper.assertion_message import pack_message
from helper.misc import pause

# Defines
TIMEOUT = 600  # 10 min


class AssertionInitiator(BaseNode):
    def compile_contract(self, contract):
        # Here the final compilation happens
        # Source: https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-existing-contracts
        if self._verbose:
            print("Compiling contract...", end=" ")
        
        with open(contract, 'r') as f:
            source = f.read()
        
        compiled_contract = compile_source(source) 
        
        if self._verbose:
            print("SUCCESS!")
        
        return compiled_contract
    
    def publish_contract(self, compiled_contract, passphrase):
        # Returns contract address
        # Source: https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-existing-contracts
        if self._w3 is None:
            print("E: Please connect first to ethereum client")
            return
        
        #contract_id, contract_interface = compiled_contract.popitem()
        _, contract_interface = compiled_contract.popitem()
        
        if self._verbose:
            print("Publishing contract...", end=" ")
        
        if not self._debug:
            # Contract only published once for debug purposes
            ret = self._w3.geth.personal.unlock_account(self._account_address, passphrase)
            if ret != True:
                print("E: Could not unlock account")
                return
            
            Contract = self._w3.eth.contract(
                address = self._account_address,
                abi=contract_interface['abi'],
                bytecode=contract_interface['bin'])
            
            tx_hash = Contract.constructor().transact()
        else:
            # transaction hash of the test 1 contract creation in the ropsten network
            #tx_hash = '0x8130e2d84ec06cb68ac5b4a97ee0ea78737b2b65a26442f6e30a223ac0b1d293'
            # Test 2
            tx_hash = Web3.toBytes(hexstr='0xd74d7d43db0350b77f4ac69d992def18c0c837c15380445306ea39dbb08f8af7')
            # Test 3
            #tx_hash = Web3.toBytes(hexstr='0x3a5ab9d2165971e7e5d9aa5e4e7b06945a19b87569446ea5603f9f41f8088e42')
        
        tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=TIMEOUT)
        contract_address = tx_receipt.contractAddress # '0x7f0A014d768b5051997C2193615946d29d9B69A3'
        
        if self._verbose:
            print("SUCCESS!")
            print("|- Transaction hash:", Web3.toHex(tx_hash))
            print("|- Contract address:", contract_address)
        
        contract = self._w3.eth.contract(
            address = contract_address,
            abi=contract_interface['abi'])
        
        # Debug
        #print("ABI:\n", contract_interface['abi'])
        
        return contract, contract_address
    
    def pay_fund(self, amount_wei, contract, passphrase):
        if self._verbose:
            print("Paying fund...", end=" ")
        
        try:
            # Sending transaction only once for debug purposes
            if not self._debug and not self._infura:  # Connecting via local client
                ret = self._w3.geth.personal.unlock_account(self._account_address, passphrase)
                if ret != True:
                    print("E: Could not unlock account!")
                    return
                
                tx_hash = contract.functions.payFund().transact({'value': amount_wei})
            elif not self._debug and self._infura: # Connecting via infura call
                print("E: Infura transacting not implemented yet!") # ToDo
                return
            else: # Debug
                # Test 2
                tx_hash = Web3.toBytes(hexstr='0xe60db752685dd07da44b2c6cff02a4785a206e75f5bd8649cb234249ebdc900a')
            
            tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=TIMEOUT)
            
            if self._verbose:
                print("SUCCESS!")
                print("|- Payed fund:", Web3.fromWei(amount_wei, 'ether'))
                print("|- Transaction hash:", Web3.toHex(tx_hash))
            
        except:
            print("E: Paying Fund went wrong!")
            return None
        
        return tx_receipt
    
    def publish_parameter_hash(self, contract, parameter, passphrase):
        if self._verbose:
            print("Publishing parameter hash...", end=" ")
        
        parameter_hash = self.calculate_parameter_hash(parameter)
        
        try:
            # Sending transaction only once for debug purposes
            if not self._debug and not self._infura:  # Connecting via local client
                ret = self._w3.geth.personal.unlock_account(self._account_address, passphrase)
                if ret != True:
                    print("E: Could not unlock account!")
                    return
                
                tx_hash = contract.functions.publishParameterHash(parameter_hash).transact()
                # Debug Test 3 - ToDo: Remove!!
                #tx_hash = contract.functions.testReturn(1).transact()
            elif not self._debug and self._infura: # Connecting via infura call
                print("E: Infura transacting not implemented yet!") # ToDo
                return
            else: # Debug
                # Test 1
                #tx_hash = '0x44c82fca078adb8752fba7cab5bcd31a46887e8c38d8d5601a23df8811d0087b'
                # Test 2
                tx_hash = Web3.toBytes(hexstr='0x136b558a2b99a069dc3c98e7d2fd96454a9c0b584a21b327d181aa5b08697016')
                # Test 3
                #tx_hash = Web3.toBytes(hexstr='0x59416e3eea98c8f33f389f56aeae5817c8574c96c32de4ee49d4cc2421e9d61f')
            
            tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=TIMEOUT)
            # Test 1
            # AttributeDict({'blockHash': HexBytes('0x0581b298ea20ebf8ca209dd718c3cd7b4f9f3da4013dd294db1b63b5177343e9'), 'blockNumber': 10166461, 'contractAddress': None, 'cumulativeGasUsed': 7430434, 'from': '0x179b70a2b0b26dfC207A8936DD9cc35144d64e27', 'gasUsed': 43918, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 1, 'to': '0x7f0A014d768b5051997C2193615946d29d9B69A3', 'transactionHash': HexBytes('0x44c82fca078adb8752fba7cab5bcd31a46887e8c38d8d5601a23df8811d0087b'), 'transactionIndex': 23, 'type': '0x0'})
            # Test 3
            # Transaction Receipt: AttributeDict({'blockHash': HexBytes('0x1f0ff9173a0162efef320553714c6ff221cecd2279dcd3121537e2873653979b'), 'blockNumber': 10250081, 'contractAddress': None, 'cumulativeGasUsed': 3848005, 'from': '0x179b70a2b0b26dfC207A8936DD9cc35144d64e27', 'gasUsed': 44092, 'logs': [], 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'status': 1, 'to': '0xa45650a120f11A6b54512b4167A2Ae8bC622bD35', 'transactionHash': HexBytes('0x38f232939c06f7af9c906a56627fbded23169506b60c372f7795064c9dc9b9e9'), 'transactionIndex': 17, 'type': '0x0'})
            
            if self._verbose:
                print("SUCCESS!")
                print("|- Parameter hash:", parameter_hash)
                print("|- Transaction hash:", Web3.toHex(tx_hash))
            
            #transfer_filter = contract.events.Transfer.createFilter(fromBlock="0x0")
            #print("True")
            #print("Filter entries:\n", transfer_filter.get_new_entries())
            
        except:
            print("E: Publishing Parameter went wrong!")
            return None
        
        return tx_receipt
    
    def send_assertion_challenge(self, contract_address : str,
                                 function_name :str,
                                 parameter):
        function_id = FUNCTIONS.get_id_by_name(function_name)
        if function_id == -1:
            print("E: Function seem not to exist!")
            return
        
        message = pack_message(contract_address, function_id, parameter)
        
        try:
            if self._verbose:
                print("Sending Waku message...", end=" ")
            
            if self._waku == True:
                ret = subprocess.check_output(["../waku/sender/release/sender", message])
                ret = ret.decode('utf-8')[:-1]
            else:
                ret = "Disabled"
            
            if ret == "True":
                if self._verbose:
                    print("SUCCESS!")
            elif ret == "Disabled":
                if self._verbose:
                    print("Waku disabled!")
            else:
                raise
            
            print("|- Message:", message)
        
        except:
            print("E: Sending challenge went wrong!")
            return
    
    '''
    Check if the final transaction can finally be published
    '''
    def check_process_readiness(self):
        pass
    
    def publish_transaction(self, contract, passphrase, parameter):
        # Returns transaction return
        if self._verbose:
            print("Publishing final transaction...", end=" ")
        
        try:            
            # Sending transaction only once for debug purposes
            if not self._debug and not self._infura:  # Connecting via local client
                ret = self._w3.geth.personal.unlock_account(self._account_address, passphrase)
                if ret != True:
                    print("E: Could not unlock account!")
                    return
                
                # Currently only called with one parameter
                tx_hash = contract.functions.someFunction(parameter).transact()
            elif not self._debug and self._infura: # Connecting via infura call
                print("E: Infura transacting not implemented yet!") # ToDo
                return
            else: # Debug
                tx_hash = Web3.toBytes(hexstr='0xae9f0d5808e946a2e955992c988ac57636514bb768e1a84ff8c6f5e65c35b3b0')
            
            tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=TIMEOUT)
            
            log_to_process = tx_receipt['logs'][0]
            processed_log = contract.events.GetFunctionResult().processLog(log_to_process)
            valid = processed_log['args']['valid']
            retVal = processed_log['args']['retVal']
            
            
            if self._verbose:
                print("SUCCESS!")
                print("|- Transaction hash:", Web3.toHex(tx_hash))
                print("|- Valid:", valid)
                print("|- Result:", retVal)
            
        except:
            print("E: Publishing Parameter went wrong!")
            return None
        
        #return valid, retVal


def main():
    """
    # When running from the command line
    if len(sys.argv) != 2:
        print("Number of arguments does not match! Usage: python3 initiator.py <parameter>")
        sys.exit(1)
    
    parameter = sys.argv[1]
    """
    
    initiator_address = '0x179b70a2b0b26dfc207a8936dd9cc35144d64e27' 
    test_contract_path = '../contracts/ropsten_test2.sol'
    passphrase = 'uLfBVRIHGZb7fejp53DC'
    assertion = "sorted_array"
    parameter = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    verbose_flag = True
    pause_flag = True
    
    # Connect to client and check status
    # Tested with account address 0x7f0A014d768b5051997C2193615946d29d9B69A3
    ai = AssertionInitiator(debug = True, waku = False, verbose = verbose_flag)
    ai.set_account_address(initiator_address)
    if ai.connect_to_client() == False:
        return
    
    balance_start = ai.get_balance()
    
    pause(pause_flag)
    if verbose_flag:
        print("------------------------------------------------------------------------------------------\n")
    
    # Compile and publish contract
    compiled = ai.compile_contract(test_contract_path)
    pause(pause_flag)
    
    contract, contract_address = ai.publish_contract(compiled, passphrase)
    pause(pause_flag)
    if verbose_flag:
        print("")
    
    ai.pay_fund(Web3.toWei(Decimal('0.2'), 'ether'), contract, passphrase)
    
    balance_intermediate = ai.get_balance()
    balance_difference = abs(balance_start - balance_intermediate)
    print("|- Balance difference: %f Ether\n" % Web3.fromWei(balance_difference, 'ether'))
    pause(pause_flag)
    
    # Publish parameter hash on blockchain and check agains local calculation
    _ = ai.publish_parameter_hash(contract, parameter, passphrase)
    pause(pause_flag)
    if verbose_flag:
        print("------------------------------------------------------------------------------------------\n")
    
    # Publish assertion challenge
    ai.send_assertion_challenge(contract_address, assertion, parameter)
    pause(pause_flag)
    if verbose_flag:
        print("------------------------------------------------------------------------------------------\n")
    
    while True:
        val = input("> Waiting for validators process to finish, continue [yes]? ")
        if val == "yes":
            break
    
    ai.publish_transaction(contract, passphrase, parameter)
    pause(pause_flag)
    
    if verbose_flag:
        print("\nFinished!")
    
    balance_end = ai.get_balance()
    balance_difference = abs(balance_start - balance_end)
    print("|- Balance difference: %f Ether" % Web3.fromWei(balance_difference, 'ether'))


if __name__ == '__main__':
    main()
