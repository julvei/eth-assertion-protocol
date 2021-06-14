// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.5;

contract CheckProofContract {
    struct Proof {
        address payable[] address_sender;
        uint[] smallerParameter;
        uint[] biggerParameter;
        uint size;
    }
    Proof proofs;
    bytes32 target;
    
    constructor () {
        proofs.size = 0;
        target = 0x007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    }
    
    function publishProof (uint smallerParameter, uint biggerParameter) public {
        proofs.address_sender.push(msg.sender);
        proofs.smallerParameter.push(smallerParameter);
        proofs.biggerParameter.push(biggerParameter);
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
    
    function CheckProofs (uint[] memory smallerArray, uint[] memory biggerArray) public view returns (bool result, bytes32 lastHash) {
        result = false;
        
        // Check Proofs
        for (uint i = 0; i < proofs.size; i++){
            bool comparison = (smallerArray[proofs.smallerParameter[i]] >= biggerArray[proofs.biggerParameter[i]]);
        
            // Hash address with parameter and calculation result
            bytes32 hash = keccak256(abi.encodePacked(proofs.address_sender[i], proofs.smallerParameter[i], proofs.biggerParameter[i], comparison));
        
            // Check if hash is smaller than target hash ("mining")
            if (hash < target){
                // send incentive
                result = true;
            } 
            lastHash = hash;
        }
    }
}
