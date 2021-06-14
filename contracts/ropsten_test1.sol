// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.7.5;

contract ParameterHash {
    bytes32 parameterHash;
    
    function setParameterHash(bytes32 hash) public {
        parameterHash = hash;
    }
    
    function getParameterHash() public view returns(bytes32 hash){
        hash = parameterHash;
    }
}
