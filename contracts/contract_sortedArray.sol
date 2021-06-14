// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.5;

contract SortedArrayContract {
    address payable owner; // Currently only owner can use the assertion
    bytes32 public parameter_hash;
    uint256 public fund;
    bytes32 public target;
    address payable counterexample_finder;
    uint counterexample_parameter;
    
    struct Proof {
        address payable[] address_sender;
        uint[] parameter;
        uint size;
    }
    Proof proofs;
    
    uint test; // For testing purposes
    
    constructor () {
        owner = msg.sender;
        //0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        //FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
        target = bytes32(type(uint256).max >> 7);
        
    }
    
    function payFund () payable public {
        fund = msg.value;
    }
    
    function publishHash (int256 hash) public {
        parameter_hash = bytes32(hash);
    }
    
    function publishProof (uint parameter) public {
        proofs.address_sender.push(msg.sender);
        proofs.parameter.push(parameter);
        proofs.size += 1;
    }
    
    function publishCounterexample (uint parameter) public {
        require(counterexample_finder == address(0), "Counterexample already found");
        counterexample_finder = msg.sender;
        counterexample_parameter = parameter;
    }
    
     function SomeFunction(uint[] memory sortedArray) public returns (bool valid, uint retVal) {
        uint256 remaining_fund = fund;
        valid = true;
        retVal = 0;
        
        // Check Proofs
        for (uint i = 0; i < proofs.size; i++){
            bool comparison = (sortedArray[proofs.parameter[i]] > sortedArray[proofs.parameter[i]+1]);
            
            // Hash address with parameter and calculation result
            bytes32 hash = keccak256(abi.encodePacked(proofs.address_sender[i], proofs.parameter[i], comparison));
            
            // Check if hash is smaller than target hash ("mining")
            if (hash < target){
               // send incentive
               remaining_fund -= 0.2 ether; // Very high for testing purposes
               proofs.address_sender[i].transfer(0.2 ether); // ToDo: Reward must be defined correctly
            }
        }
        
        // Check Counterexamples
        if (counterexample_finder != address(0)) {
            if (sortedArray[counterexample_parameter] > sortedArray[counterexample_parameter+1]) {
                remaining_fund -= 1 ether; // Very high for testing purposes
                counterexample_finder.transfer(1 ether); // ToDo: Reward must be defined correctly
                valid = false; // Workaround, because "revert()" would also revert transfers
            }
        }
        
        if(valid){
            // Intended functionality happens here
            // ...
            test = 1;
            retVal = 1;
        }
        
        owner.transfer(remaining_fund); // Return remaining fund
        remaining_fund = 0;
    }
}
