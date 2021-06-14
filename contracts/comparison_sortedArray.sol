// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.5;

contract SortedArrayComparisonContract {
    uint test;
    
    function SomeFunction(uint[] memory sortedArray) public returns(uint retVal) {
        // Manual assertion
        uint min = 0;
        uint max = sortedArray.length-2;
        
        for(uint i = min; i <= max; i++){
            require(sortedArray[i] < sortedArray[i+1], "Counterexample found!");
        }
        
        // Intended functionality happens here
        // ...
        test = 1;
        retVal = 1;
    }
}
