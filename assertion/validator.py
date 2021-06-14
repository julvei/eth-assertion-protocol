"""
Author: JV
Date: 2021-04-26

Providing the assertion validator functionalities

1. Check Fund
2. Check Parameter Hash
3. Verifiable Computation
4. Publish Proofs
5. Publish Counterexamples
"""
# Includes
import os, sys
from _pydecimal import Decimal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
from web3 import Web3
from typing import Tuple
from helper.assertion_message import unpack_message
from assertion.base_node import BaseNode
from assertion.functions import FUNCTIONS
from check_local.reward_checker import RewardChecker
from helper.misc import pause
from assertion.interface import default_interface

# Defines
TIMEOUT = 600  # 10 min


"""
Class Assertion Validator
"""
class AssertionValidator(BaseNode):
    """
    Blocking function until message has been received
    """
    def receive_message(self):
        if self._verbose:
                print("Waiting for assertion message...", end=" ")
        
        try:
            if self._waku:
                message = subprocess.check_output(["../waku/receiver/release/receiver"])
                message = message.decode('utf-8')[:-1]
            else:
                # Some dummy message
                message = "['0x1a3eE9be6635284b0Df1933B691Fd95366de7Bee', 200, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]"
        
        except:
            print("Receiving went wrong!")
            return
        
        if self._verbose:
            print("SUCCESS!")
            print("|- Message:", message)
        
        return unpack_message(message)
    
    def get_contract(self, contract_address):    
        contract = self._w3.eth.contract(
            address = contract_address,
            abi=default_interface)
        
        return contract
    
    def get_target(self, contract):
        if self._verbose:
            print("Retrieving target from contract...", end=" ")
        
        if not self._debug:
            target = Web3.toHex(contract.functions.getTarget().call())
        else:
            target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF' 
        
        if self._verbose:
            print("SUCCESS!")
            print("|- Target:", target)
        
        return target
    
    def check_target(self, target, goal_target) -> bool:
        target_int = Web3.toInt(hexstr=target)
        goal_target_int = Web3.toInt(hexstr=goal_target)
        
        res = target_int >= goal_target_int
        print("|- Target sufficient big:", res)
        
        return res
    
    def get_function(self, function_id):
        if self._verbose:
            function_name = FUNCTIONS.get_name_by_id(function_id)
            print("|- Validation function:", function_name)
        return FUNCTIONS.get_function_by_id(function_id)
    
    def check_fund(self, contract, min_fund_wei):
        # ToDo: Fund calculator
        if self._verbose:
            print("Retrieving fund from contract...", end=" ")
        
        if not self._debug:
            fund = Web3.toInt(contract.functions.getFundAmount().call())
        else:
            fund = Web3.toWei(Decimal('0.2'), 'ether')
        
        eval_fund = True
        if fund < min_fund_wei:
            eval_fund = False
        
        if self._verbose:
            print("SUCCESS!")
            print("|- Fund:", Web3.fromWei(fund, 'ether'))
            print("|- Sufficient:", eval_fund)
        
        return eval_fund
    
    def check_parameter_hash(self, contract, parameter):
        if self._verbose:
            print("Verify hash of transmitted parameter...", end=" ")
        
        calculated_hash = self.calculate_parameter_hash(parameter)
        if not self._debug:
            on_chain_hash = Web3.toHex(contract.functions.getParameterHash().call())
        else:
            on_chain_hash = calculated_hash
        
        ret = on_chain_hash == calculated_hash
        
        if self._verbose:
            if ret:
                print("SUCCESS!")
            else:
                print("Hash not valid!")
            print("|- Parameter Hash:", on_chain_hash)
        
        return ret
    
    def run_validation(self, target, evaluation_function, parameter,
                       min_testcase : int, max_testcase : int,
                       contract, passphrase : str,
                       publish_proof : bool = False,
                       publish_counterexample : bool = False):
        if self._verbose:
            print("Running validation...", end=" ")
        
        # Initialise the Reward Checker
        rc = RewardChecker(self._account_address, target,
                           evaluation_function, parameter)
        
        # Check range
        ret = rc.checkRange(min_testcase, max_testcase)
        
        if self._verbose:
            print("SUCCESS!")
            print("|- Reward found:", ret)
        
        # Publish proofs or counterexamples
        results = None
        if ret == True:
            results = rc.getResults()
            
            for result in results:
                if (result[0] == 'target_hash') and publish_proof:
                    self.publish_proof(result, contract, passphrase)
                if (result[0] == 'counterexample') and publish_counterexample:
                    self.publish_counterexample(result, contract, passphrase)
         
        return results
    
    def publish_proof(self, proof : Tuple[str, int], contract, passphrase : str):
        if self._verbose:
            print("Publishing proof...", end=" ")
        
        try:            
            # Sending transaction only once for debug purposes
            if not self._debug and not self._infura:  # Connecting via local client
                ret = self._w3.geth.personal.unlock_account(self._account_address, passphrase)
                if ret != True:
                    print("E: Could not unlock account!")
                    return
                
                # Currently only called with one parameter
                tx_hash = contract.functions.publishProof(proof[1]).transact()
            elif not self._debug and self._infura: # Connecting via infura call
                print("E: Infura transacting not implemented yet!") # ToDo
                return
            else: # Debug
                tx_hash = Web3.toBytes(hexstr='0xb9c29e1288ff5b1593c80bc48d968b7a7365157560de35cf0724fbb82d5c4a4c')
            
            tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=TIMEOUT)
        
            if self._verbose:
                print("SUCCESS!")
                print("|- Transaction hash:", Web3.toHex(tx_hash))
                print("|- Published proof:", proof)
        
        except:
            print("E: Publishing proof went wrong!")
            return None
        
        return tx_receipt
    
    def publish_counterexample(self, counterexample : Tuple[str, int], contract, passphrase : str):
        if self._verbose:
            print("Publishing counterexample...", end=" ")
        
        try:            
            # Sending transaction only once for debug purposes
            if not self._debug and not self._infura:  # Connecting via local client
                ret = self._w3.geth.personal.unlock_account(self._account_address, passphrase)
                if ret != True:
                    print("E: Could not unlock account!")
                    return
                
                # Currently only called with one parameter
                tx_hash = contract.functions.publishCounterexample(counterexample[1]).transact()
            elif not self._debug and self._infura: # Connecting via infura call
                print("E: Infura transacting not implemented yet!") # ToDo
                return
            else: # Debug
                tx_hash = '' # ToDo
            
            tx_receipt = self._w3.eth.wait_for_transaction_receipt(tx_hash, timeout=TIMEOUT)
        
            if self._verbose:
                print("SUCCESS!")
                print("|- Transaction hash:", Web3.toHex(tx_hash))
                print("|- Published counterexample:", counterexample)
        
        except:
            print("E: Publishing counterexample went wrong!")
            return None
        
        return tx_receipt


def main():
    passphrase = 'Hpt9UFgW9BPBCkoRXUfJjiXAkHignp'
    validator_address = '0x8b74ed9f5c72797bf6f523d97aba9afda0c54083'
    goal_target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    min_fund = Web3.toWei(Decimal('0.2'), 'ether')
    verbose = True
    pause_flag = True
    
    av = AssertionValidator(debug = True, waku = False, verbose = verbose)
    av.set_account_address(validator_address)
    if not av.connect_to_client(address_cnt=1):
        return
    
    balance_start = av.get_balance()
    
    pause(pause_flag)
    if verbose:
        print("------------------------------------------------------------------------------------------\n")
    
    contract_address, function_id, parameter = av.receive_message()
    function = av.get_function(function_id)
    
    contract = av.get_contract(contract_address)
    
    pause(pause_flag)
    ret = av.check_parameter_hash(contract, parameter)
    if not ret:
        return
    
    pause(pause_flag)
    ret = av.check_fund(contract, min_fund)
    if not ret:
        return
    
    pause(pause_flag)
    target = av.get_target(contract)
    if not av.check_target(target, goal_target):
        return
    
    pause(pause_flag)
    if verbose:
        print("------------------------------------------------------------------------------------------\n")
    
    min_testcase = 0  # Should be better evaluated
    max_testcase = len(parameter)-1  # Should be better evaluated
    av.run_validation(target, function, parameter,
                      min_testcase, max_testcase,
                      contract, passphrase,
                      publish_proof=True,
                      publish_counterexample=True)
    
    pause(pause_flag)
    if verbose:
        print("------------------------------------------------------------------------------------------\n")
    
    while True:
        val = input("> Waiting for reward to be payed out, continue [yes]? ")
        if val == "yes":
            break
    
    if verbose:
        print("\nFinished!")
    
    balance_end = av.get_balance()
    balance_difference = abs(balance_start - balance_end)
    print("|- Balance Difference: %f Ether" % Web3.fromWei(balance_difference, 'ether'))


if __name__ == '__main__':
    main()