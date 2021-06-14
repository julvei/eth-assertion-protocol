// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract TestSortedArray {
        function test_hash(uint[] memory parameter, uint testcase, bool comparison) public view returns (bytes32 hash){
            // Hash address with parameter and calculation result
            hash = keccak256(abi.encodePacked(
                msg.sender, testcase, parameter[testcase], comparison));
        }
}
