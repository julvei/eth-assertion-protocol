// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ParameterComparisonContract {
    uint test;
    
    function SomeFunction(uint primeNumber) public returns(uint retVal) {
        // Manual assertion
        uint min = 2;
        uint max = primeNumber-1;
        
        for(uint i = min; i <= max; i++){
            require((primeNumber % i) != 0, "Counterexample found!");
        }
        
        // Intended functionality happens here
        // ...
        test = 1;
        retVal = 1;
    }
}
