"""
Author: JV
Date: 2021-04-25

Get some return values for online evaluation of functionality
"""
from web3 import Web3
from check_local.reward_checker import RewardChecker
from assertion.functions import FUNCTIONS
from helper.parameter_hash import ParameterHash


# Addresses from remix compiler
tester_address1 = '0x5B38Da6a701c568545dCfcB03FcB875f56beddC4'
tester_address2 = '0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2'
tester_address3 = '0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db'
tester_address4 = '0x78731D3Ca6b7E34aC0F824c42a7cC18A495cabaB'
tester_address5 = '0x617F2E2fD72FD9D5503197092aC168c91465E7f2'
tester_address6 = '0x17F6AD8Ef982297579C203069C1DbfFE4348c372'
tester_address7 = '0x85F05208B6C3613f42366dE27BAFBd4df40a8ceb'
tester_address8 = '0x03C6FcED478cBbC9a4FAB34eF9f40767739D1Ff7'
tester_address9 = '0x1aE0EA34a72D944a8C7603FfB3eC30a6669E454C'
tester_address10 = '0x0A098Eda01Ce92ff4A4CCb7A4fFFb5A43EBC70DC'
tester_address11 = '0xCA35b7d915458EF540aDe6068dFe2F44E8fa733c'
tester_address12 = '0x14723A09ACff6D2A60DcdF7aA4AFf308FDDC160C'
tester_address13 = '0x4B0897b0513fdC7C541B6d9D7E929C4e5364D2dB'
tester_address14 = '0x583031D1113aD414F02576BD6afaBfb302140225'
tester_address15 = '0xdD870fA1b7C4700F2BD7f44238821C26f7392148'
# Adresses Ropsten Ethereum Network
initiator_address = Web3.toChecksumAddress('0x179b70a2b0b26dfc207a8936dd9cc35144d64e27')
validator_address = Web3.toChecksumAddress('0x8b74ed9f5c72797bf6f523d97aba9afda0c54083')


# Tests
def test_sortedArray():
    target = '0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    
    parameter1 = list(range(1, 26))
    
    parameter2 = list(range(1, 51))
    
    parameter3 = list(range(1, 76))
    parameter3_1 = list(range(1, 76))
    parameter3_1[62] = 65
    
    parameter4 = list(range(1, 101))
    
    # evaluation function
    def sorted_array(parameter, testcase):
        return parameter[testcase] > parameter[testcase+1]
    
    tester_address = tester_address15
    
    # Check all parameters and print results
    print("---------- TEST SORTED ARRAY ----------")
    rc = RewardChecker(tester_address, target, sorted_array, parameter1)
    ret = rc.checkFast(0, len(parameter1)-1)
    if ret is True:
        print("parameter1:", rc.getResults())
    
    rc.setParameter(parameter2)
    ret = rc.checkFast(0, len(parameter2)-1)
    if ret is True:
        print("parameter2:", rc.getResults())
    
    rc.setParameter(parameter3)
    ret = rc.checkFast(0, len(parameter3)-1)
    if ret is True:
        print("parameter3:", rc.getResults())
    
    rc.setParameter(parameter3_1)
    ret = rc.checkRange(0, len(parameter3_1)-1)
    if ret is True:
        print("parameter3_1:", rc.getResults())
    
    rc.setParameter(parameter4)
    ret = rc.checkFast(0, len(parameter4)-1)
    if ret is True:
        print("parameter4:", rc.getResults())


def test_twoArrays():
    target = '0x007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    min_val = (0, 0)
    
    parameter1_1 = list(range(1, 16))
    parameter1_2 = list(range(1001, 1016))
    parameter1 = (parameter1_1, parameter1_2)
    max_val1 = (len(parameter1_1), len(parameter1_2))
    
    parameter2_1 = list(range(1, 31))
    parameter2_2 = list(range(1001, 1031))
    parameter2 = (parameter2_1, parameter2_2)
    max_val2 = (len(parameter2_1), len(parameter2_2))
    
    parameter3_1 = list(range(1, 46))
    parameter3_2 = list(range(1001, 1046))
    parameter3 = (parameter3_1, parameter3_2)
    max_val3 = (len(parameter3_1), len(parameter3_2))
    
    parameter3_1_1 = list(range(1, 46))
    parameter3_1_1[41] = 1001
    parameter3_2_1 = list(range(1001, 1046))
    parameter3_2_1[41] = 45
    parameter3_e1 = (parameter3_1_1, parameter3_2)
    parameter3_e2 = (parameter3_1, parameter3_2_1)
    
    parameter4_1 = list(range(1, 61))
    parameter4_2 = list(range(1001, 1061))
    parameter4 = (parameter4_1, parameter4_2)
    max_val4 = (len(parameter4_1), len(parameter4_2))
    
    # evaluation function
    def two_arrays(parameter, testcase):
        return parameter[0][testcase[0]] >= parameter[1][testcase[1]]
    
    #tester_address = tester_address8
    tester_address = tester_address4
    
    # Check all parameters and print results
    print("---------- TEST TWO ARRAYS ----------")
    rc = RewardChecker(tester_address, target, two_arrays, parameter1)
    ret = rc.checkFast(min_val, max_val1)
    if ret is True:
        print("parameter1:", rc.getResults())
    
    rc.setParameter(parameter2)
    ret = rc.checkFast(min_val, max_val2)
    if ret is True:
        print("parameter2:", rc.getResults())
    
    rc.setParameter(parameter3)
    ret = rc.checkFast(min_val, max_val3)
    if ret is True:
        print("parameter3:", rc.getResults())
    
    rc.setParameter(parameter3_e1)
    ret = rc.checkRange(min_val, max_val3)
    if ret is True:
        print("parameter3_1:", rc.getResults())
    
    rc.setParameter(parameter3_e2)
    ret = rc.checkRange(min_val, max_val3)
    if ret is True:
        print("parameter3_2:", rc.getResults())
    
    rc.setParameter(parameter4)
    ret = rc.checkFast(min_val, max_val4)
    if ret is True:
        print("parameter4:", rc.getResults())


def getting_values():
    ph = ParameterHash()
    
    # Setting up test case
    target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    parameter = list(range(1, 7))
    parameter[1] = 4
    print("Parameter:", parameter)
    print("Parameter Hash:", ph.parameter_hash(parameter))
    function = FUNCTIONS.get_function_by_name("sorted_array")
    tester_address = tester_address4
    
    # Getting values
    rc = RewardChecker(tester_address, target, function, parameter)
    ret = rc.checkRange(0, len(parameter)-1)
    if ret is True:
        print("Rewards:", rc.getResults())
        print("Hashes:", rc.getTargetHashes())
        
def checking_ropsten():
    ph = ParameterHash()
    
    # Setting up test case
    target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    parameter = list(range(1, 11))
    print("Parameter:", parameter)
    print("Parameter Hash:", ph.parameter_hash(parameter))
    function = FUNCTIONS.get_function_by_name("sorted_array")
    tester_address = validator_address
    
    # Getting values
    rc = RewardChecker(tester_address, target, function, parameter)
    ret = rc.checkRange(0, len(parameter)-1)
    if ret is True:
        print("Rewards:", rc.getResults())
        print("Hashes:", rc.getTargetHashes())

def final_test_linear():
    ph = ParameterHash()
    parameter1 = list(range(1, 26))
    parameter2 = list(range(1, 51))
    parameter3 = list(range(1, 76))
    parameter4 = list(range(1, 101))
    parameter_list = [parameter1, parameter2, parameter3, parameter4]
    
    target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    
    # evaluation function
    def sorted_array(parameter, testcase):
        return parameter[testcase] > parameter[testcase+1]
    
    tester_address = tester_address15
    
    rc = RewardChecker(tester_address, target, sorted_array, parameter1)
    
    print("Validator address:", tester_address)
    print("")
    
    for parameter in parameter_list:
        print("[%i, ..., %i] :" %(parameter[0], parameter[-1]), ph.parameter_hash(parameter))
        rc.setParameter(parameter)
        ret = rc.checkFast(0, len(parameter)-1)
        if ret is True:
            print("Validator testcase:", rc.getResults()[0][1])
            print("")


def final_test_quadratic():
    ph = ParameterHash()
    
    min_val = (0, 0)
    parameter1 = (list(range(1, 16)), list(range(1001, 1016)))
    max_val1 = (len(parameter1[0]), len(parameter1[1]))
    parameter2 = (list(range(1, 31)), list(range(1001, 1031)))
    max_val2 = (len(parameter2[0]), len(parameter2[1]))
    parameter3 = (list(range(1, 46)), list(range(1001, 1046)))
    max_val3 = (len(parameter3[0]), len(parameter3[1]))
    parameter4 = (list(range(1, 61)), list(range(1001, 1061)))
    max_val4 = (len(parameter4[0]), len(parameter4[1]))
    
    parameter_list = [parameter1, parameter2, parameter3, parameter4]
    max_list = [max_val1, max_val2, max_val3, max_val4]
    
    target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    
    # evaluation function
    def two_arrays(parameter, testcase):
        return parameter[0][testcase[0]] >= parameter[1][testcase[1]]
    
    tester_address = tester_address2
    rc = RewardChecker(tester_address, target, two_arrays, parameter1)
    
    print("Validator address:", tester_address)
    print("")
    
    for parameter, max_val in zip(parameter_list, max_list):
        print("[%i, ..., %i], [%i, ..., %i] :" %(parameter[0][0], parameter[0][-1], parameter[1][0], parameter[1][-1]), ph.parameter_hash(parameter))
        rc.setParameter(parameter)
        ret = rc.checkFast(min_val, max_val)
        if ret is True:
            print("Validator testcase:", rc.getResults()[0][1])
            print("")


def final_test_parameter():
    ph = ParameterHash()
    
    min_val = 2
    parameter_list = [11, 829, 1667, 2503]
    target = '0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
    
    # evaluation function
    def is_prime(parameter, testcase):
        return (parameter % testcase == 0)
    
    tester_address = tester_address2
    rc = RewardChecker(tester_address, target, is_prime, 11)
    
    print("Validator address:", tester_address)
    print("")
    
    for parameter in parameter_list:
        print(parameter, ":", ph.parameter_hash(parameter))
        rc.setParameter(parameter)
        ret = rc.checkFast(min_val, parameter)
        if ret is True:
            print("Validator testcase:", rc.getResults()[0][1])
            print("")


def main():
    #test_sortedArray()
    #test_twoArrays()
    #getting_values()
    #checking_ropsten()
    #final_test_linear()
    #final_test_quadratic()
    final_test_parameter()


if __name__ == '__main__':
    main()