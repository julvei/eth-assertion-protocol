// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.5;

contract CheckProofContract {
    struct Proof {
        address payable[] address_sender;
        uint[] parameter;
        uint size;
    }
    Proof proofs;
    bytes32 target;
    
    constructor () {
        proofs.size = 0;
        target = 0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    }
    
    function PublishProof (uint parameter) public {
        proofs.address_sender.push(msg.sender);
        proofs.parameter.push(parameter);
        proofs.size += 1;
    }
    
    /* Helper Function - Debug */
    /*
    function ReturnProofsEntry (uint number) public view returns (address payable s, uint p) {
        require(number < proofs.size, "This entry does not exist");
        
        s = proofs.sender_address[number];
        p = proofs.parameter[number];
    }
    
    function ReturnTarget () public view returns (bytes32 ret) {
        ret = target;
    }
    */
    
    function CheckProofs (uint[] memory sortedArray) public view returns (bool result, bytes32 lastHash) {
        result = false;
        
        // Check Proofs
        for (uint i = 0; i < proofs.size; i++){
            bool comparison = (sortedArray[proofs.parameter[i]] > sortedArray[proofs.parameter[i]+1]);
        
            // Hash address with parameter and calculation result
            bytes32 hash = keccak256(abi.encodePacked(proofs.address_sender[i], proofs.parameter[i], comparison));
        
            // Check if hash is smaller than target hash ("mining")
            if (hash < target){
                // send incentive
                result = true;
            } 
            lastHash = hash;
        }
    }
}
