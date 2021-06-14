# Validation of Contracts
* `<Testcase>` : `<Result>`

## Ropsten Test 2
* Deploy Contract -> ... : **Success**
* Pay Fund : **Success**
* Get Target : **Success**
* Set Target -> Get Target : **Success**
* Publish Parameter Hash -> Get Parameter Hash : **Success**
* Pay Fund -> Get Fund Amount : **Success**
* Pay Fund -> Publish Proof : **Success**
* Pay Fund -> Publish Proof -> Function -> *Check Balances* -> *Check Return* : **Success**
* Pay Fund -> Publish Proof (2x correct, 1x incorrect) -> Function -> *Check Balances* : **Success**
* Pay Fund -> Publish Proof -> Publish Counterexample -> Function -> *Check Balances* -> *Check Return* : **Success**
* Pay Fund -> Publish Proof -> Publish Counterexample (incorrect) -> Function -> *Check Balances* -> *Check Return* : **Success**
* 2x (Pay Fund -> Publish Proof -> Publish Counterexample (1. correct, 2. incorrect) -> Function -> *Check Balances* -> *Check Return*) : **Success**
* Pay Fund -> Publish Counterexample -> Publish Counterexample -> *Error* : **Success**
* Pay Fund -> Set Target -> *Error* : **Success**
    * ... -> Publish Proof -> Set Target -> *Error* : **Success**
    * ... -> Publish Counterexample -> Set Target -> *Error* : **Success**
    * ... -> Function -> Set Target -> *No Error* : **Success**
