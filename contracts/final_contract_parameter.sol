// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract TestParameter {
    address payable owner; // Currently only owner can use the assertion
    bytes32 parameter_hash;
    uint256 fund;
    bytes32 target;
    bool running = false;
    
    // Counterexample
    address payable counterexample_finder;
    uint counterexample_testcase;
    
    // Proof
    struct Proof {
        address[] address_sender;
        uint[] testcase;
    }
    Proof proofs;
    
    uint test; // For testing purposes
    
    constructor () {
        owner = payable(msg.sender);
        target = bytes32(type(uint256).max >> 3);
        
    }
    
    // Events
    event GetFunctionResult(bool valid, uint retVal);
    
    function someFunction(uint primeNumber) public returns (bool valid, uint retVal) {
        valid = true;
        
        // Check Proofs
        for (uint i = 0; i < proofs.testcase.length; i++){
            bool comparison = ((primeNumber % proofs.testcase[i]) == 0);

            // Hash address with parameter and calculation result
            bytes32 hash = keccak256(abi.encodePacked(
                proofs.address_sender[i], proofs.testcase[i],
                primeNumber, comparison));
            
            // Check if hash is smaller than target hash ("mining")
            if (hash < target){
               // Send incentive: 
               // Transaction costs for publishProof: 104_671
               // Gas costs on 06.05.2021: 73 Gwei, Incentive: 7_000_000 Gwei
               // (104_671 gas * 73 Gwei) + 7_000_000 Gwei = 14_640_983 Gwei = 0.014640983 Ether
               // => Has to be adapted individually, or one fix reward?
               fund -= 14_640_983 gwei;
               payable(proofs.address_sender[i]).transfer(14_640_983 gwei);
            }
        }
        
        // Check Counterexamples
        if (counterexample_finder != address(0)) {
            if ((primeNumber % counterexample_testcase) == 0) {
                // Send incentive:
                // Transaction costs for publishCounterexample: 63_643
                // Gas costs on 06.05.2021: 73 Gwei, Incentive: 14_000_000
                // (63_643 gas * 73 Gwei) + 14_000_000 Gwei = 18_645_939 = 0.018645939 Ether
                // => Has to be adapted individually, or one fix reward?
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
        delete counterexample_testcase;
        delete proofs.address_sender;
        delete proofs.testcase;
        
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
    
    function publishProof (uint testcase) public {
        proofs.address_sender.push(msg.sender);
        proofs.testcase.push(testcase);
    }
    
    function publishCounterexample (uint testcase) public {
        require(counterexample_finder == address(0), "Counterexample already found");
        counterexample_finder = payable(msg.sender);
        counterexample_testcase = testcase;
    }
}
