// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.5;

contract TwoArraysComparisonContract {
    uint test;
    
    function SomeFunction(uint[] memory smallerArray, uint[] memory biggerArray) public returns(uint retVal) {
        // Manual assertion
        uint min = 0;
        uint max_smallerArray = smallerArray.length;
        uint max_biggerArray = biggerArray.length;
        
        for(uint i = min; i <= max_smallerArray-1; i++){
            for(uint j = min; j <= max_biggerArray-1; j++){
                require(smallerArray[i] < biggerArray[j], "Counterexample found!");
            }
        }
        
        // Intended functionality happens here
        // ...
        test = 1;
        retVal = 1;
    }
}
