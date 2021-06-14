// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.5;

contract GetParameterHash {
    function getVariableHash(uint variable) pure public returns(bytes32 variableHash, bool smallHash) {
        smallHash = false;
        variableHash = keccak256(abi.encodePacked(variable));
        if(variableHash <= (bytes32(type(uint256).max >> 4))){
            smallHash = true;
        }
    }
    
    function getArrayHash(uint256[] memory sortedArray) pure public returns(bytes32 arrayHash, bool smallHash) {
        smallHash = false;
        arrayHash = keccak256(abi.encodePacked(sortedArray));
        if(arrayHash <= (bytes32(type(uint256).max >> 4))){
            smallHash = true;
        }
    }
} 
