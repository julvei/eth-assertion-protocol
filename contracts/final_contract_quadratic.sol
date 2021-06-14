// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract TestSortedArray {
    address payable owner; // Currently only owner can use the assertion
    bytes32 parameter_hash;
    uint256 fund;
    bytes32 target;
    bool running = false;
    
    // Counterexample
    address payable counterexample_finder;
    uint counterexample_testcase1;
    uint counterexample_testcase2;
    
    // Proof
    struct Proof {
        address[] address_sender;
        uint[] testcase1;
        uint[] testcase2;
    }
    Proof proofs;
    
    uint test; // For testing purposes
    
    constructor () {
        owner = payable(msg.sender);
        target = bytes32(type(uint256).max >> 3);
        
    }
    
    // Events
    event GetFunctionResult(bool valid, uint retVal);
    
    function someFunction(uint[] memory array1, uint[] memory array2) public returns (bool valid, uint retVal) {
        valid = true;
        
        // Check Proofs
        for (uint i = 0; i < proofs.testcase1.length; i++){
            bool comparison = (array1[proofs.testcase1[i]] >= array2[proofs.testcase2[i]]);

            // Hash address with parameter and calculation result
            bytes32 hash = keccak256(abi.encodePacked(
                proofs.address_sender[i], proofs.testcase1[i],
                proofs.testcase2[i], array1[proofs.testcase1[i]],
                array2[proofs.testcase2[i]], comparison));
            
            // Check if hash is smaller than target hash ("mining")
            if (hash < target){
               // Send incentive
               fund -= 14_640_983 gwei;
               payable(proofs.address_sender[i]).transfer(14_640_983 gwei);
            }
        }
        
        // Check Counterexamples
        if (counterexample_finder != address(0)) {
            if (array1[counterexample_testcase1] >= array2[counterexample_testcase2]) {
                // Send incentive
                fund -= 18_645_939 gwei;
                counterexample_finder.transfer(18_645_939 gwei);
                
                valid = false;
            }
        }
        
        // Return remaining fund: Not returned fund is currently lost forever! (Use debug function)
        //owner.transfer(fund);
        // Return all deposited ethers (debug)
        owner.transfer(address(this).balance);
        fund = 0;
        
        // Clean up
        running = false;
        delete counterexample_finder;
        delete counterexample_testcase1;
        delete counterexample_testcase2;
        delete proofs.address_sender;
        delete proofs.testcase1;
        delete proofs.testcase2;
        
        if(valid == false){
            emit GetFunctionResult(false, 0);
            return (false, 0); // Workaround, because "revert()" would also revert transfers
        }
        
        // Intended functionality happens here
        // ...
        test = 1;
        retVal = 1;
        
        emit GetFunctionResult(valid, retVal);
    }
    
    /******************************************************************************************/
    /* Standardized Interface */
    // Fund
    function payFund () payable public {
        // Minimum fund currently set to 0.2 ether
        // Sufficient to pay for one counterexample and at least 12 proofs
        require(msg.value >= 0.2 ether, "Not sufficient fund!");
        fund = msg.value;
        running = true;
    }
    
    function getFundAmount () public view returns (uint256 fundAmount) {
        fundAmount = fund;
    }
    
    // Parameter Hash
    function publishParameterHash (bytes32 hash) public {
        parameter_hash = hash;
    }
    
    function getParameterHash () public view returns (bytes32 hash) {
        hash = parameter_hash;
    }
    
    // Target
    function setTarget (bytes32 targetValue) public {
        // Not allowed to be set if process currently running!
        require(running == false, "Process currently running!");
        target = targetValue;
    }
    
    function getTarget () public view returns (bytes32 targetValue) {
        targetValue = target;
    }
    
    function publishProof (uint testcase1, uint testcase2) public {
        proofs.address_sender.push(msg.sender);
        proofs.testcase1.push(testcase1);
        proofs.testcase2.push(testcase2);
    }
    
    function publishCounterexample (uint testcase1, uint testcase2) public {
        require(counterexample_finder == address(0), "Counterexample already found");
        counterexample_finder = payable(msg.sender);
        counterexample_testcase1 = testcase1;
        counterexample_testcase2 = testcase2;
    }
}
