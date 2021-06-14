// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract TestReturn {
    event NewSum(uint sum);
    
    uint old_value = 0;
    
    function testReturn(uint new_value) public {
        uint sum = old_value + new_value;
        emit NewSum(sum);
        
        old_value = new_value;
    }
}
