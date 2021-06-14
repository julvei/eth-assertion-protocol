# Implemantation of Assertion Concept
This is an implementation of the Ethereum assertion protocol for checking its functionality.

# Prerequisites
## Install Python Packages
* web3: `pip install web3`
* solcx: `pip install py-solc-x`

## Further Installs
* Go: [Installation Manual](https://golang.org/doc/install)
* Geth: [Installation Manual](https://geth.ethereum.org/docs/install-and-build/installing-geth)
* Solc: [Installation Manual](https://docs.soliditylang.org/en/latest/installing-solidity.html)

## Connect to Ropsten (PoW)
1. Start Geth: `geth --ropsten --syncmode "light"`
3. Create Account: Using Web3 API and Python
	* https://web3py.readthedocs.io/en/stable/quickstart.html
	* `pip install web3`
	* `>>> from web3 import Web3`
	* `>>> w3 = Web3(Web3.IPCProvider('~/.ethereum/ropsten/geth.ipc'))`
	* `>>> <address> = w3.geth.personal.new_account(<passphrase>)`
4. Get Test Ether: https://faucet.ropsten.be/
5. Explore Ropsten: https://ropsten.etherscan.io

## Disclaimer
The code has been tested on two machines, one debian based (Ubuntu 20.04) and one arch based (Manjaro). No further operating system and no clean set-up has been tested. So there occur very likely unforseen problems.

# Blockchain
## Addresses
For testing purposes two addresses have been created, one for the Initiator and one for the Validator. The private keys for those will not be published, so new addresses have to be created and the program has to be adapted accordingly by changing following variables: `initiator_address`, `validator_address`, and `passphrase` of both. Nevertheless, the already conducted test runs can be explored on the blockchain.

* Initiator: `0x179b70a2b0b26dfc207a8936dd9cc35144d64e27`
    * [Link Block Explorer](https://ropsten.etherscan.io/address/0x179b70a2b0b26dfc207a8936dd9cc35144d64e27)
* Validator: `0x8b74ed9f5c72797bf6f523d97aba9afda0c54083`
    * [Link Block Explorer](https://ropsten.etherscan.io/address/0x8b74ed9f5c72797bf6f523d97aba9afda0c54083)

## Contracts
Contracts can be found in the subfolder `contracts`. The test contracts have already been published to the Ropsten test network.

* ropsten_test1.sol: `0x7f0A014d768b5051997C2193615946d29d9B69A3`
	* [Link Block Explorer](https://ropsten.etherscan.io/address/0x7f0A014d768b5051997C2193615946d29d9B69A3)
	* transaction hash: `0x8130e2d84ec06cb68ac5b4a97ee0ea78737b2b65a26442f6e30a223ac0b1d293`
* ropsten_test2.sol: `0x1a3eE9be6635284b0Df1933B691Fd95366de7Bee`
	* [Link Block Explorer](https://ropsten.etherscan.io/address/0x1a3eE9be6635284b0Df1933B691Fd95366de7Bee)
	* transaction hash: `0xd74d7d43db0350b77f4ac69d992def18c0c837c15380445306ea39dbb08f8af7`
* ropsten_test3.sol: `0xa45650a120f11A6b54512b4167A2Ae8bC622bD35`
	* [Link Block Explorer](https://ropsten.etherscan.io/address/0xa45650a120f11A6b54512b4167A2Ae8bC622bD35)
	* transaction hash: `0xe78041d813d2097ab312efdf5b19fdebb5c96c1bb48df0adc6f284f83796dc07`
* ropsten_test3.sol (2): `0xb6bAAcD262adEc7B3600000b6cfC5b8Cb7eb23A3`
	* [Link Block Explorer](https://ropsten.etherscan.io/address/0xb6bAAcD262adEc7B3600000b6cfC5b8Cb7eb23A3)
	* transaction hash: `0x3a5ab9d2165971e7e5d9aa5e4e7b06945a19b87569446ea5603f9f41f8088e42`

# Python Code
There are two main python programs, the Initiator found under `assertion/initiator.py` and the Validator found under `assertion/validator.py`. If they are executed as are, then some debug code is conducted which shows how it would happen. It still needs to connect to the geth node.  

The instances can be called with some flags to change the behaviour.
* `infura = False`: Infura http call instead of geth ipc (Not fully implemented yet!)
* `debug = True`: Running debug code instead of real transaction calls
* `waku = True`: Publish and receive the message via waku, else only dummy
* `verbose = False`: Printing information about the code which is conducted

## Initiator
Some variables are predefined but can be changes for a different test run.
* `test_contract_path`: Defines the contract path to the contract which shall be compiled and published
* `assertion`: Defines the assertion which shall be done (see `assertion/functions.py`), must fit with the published contract
* `parameter`: Defines the parameter which shall be asserted

## Validator
Some variables define what the Validator expects from the contract such that it can be decided if the assertion should be conducted. In a real scenario those must either be gathered automatically or predefined by the user.
* `goal_target`: Real target must be equal or higher for the assertion, otherwise too few hashes might be found
* `min_fund`: Fund in the contract must be equal or higher so that the Validator can be paid out

## Debug
Some variables in the main programs are there for debug purposes.
* `verbose_flag = True`: Printing information about the program execution
* `pause_flag = True`: Halting the program after a while to check the status

# Waku Code
The code for transmitting an receiving the messages over waku is written in go and the programs can be found in the `waku` folder. Those are modified examples from the [go-waku github repository](https://github.com/status-im/go-waku). The resulting binaries are called from python as a subprocess. The topic used for the communication is the random string `udtraei`, but can be changed in the code.
