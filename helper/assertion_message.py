"""
Author: JV
Date: 2021-04-26

Function for the assertion message between initiator and validator.
Currently only supports integer, single and double array parameters.
"""
from copy import copy

"""
Pack the message for sending it over the waku network
Input:    contract_address - Which contract should be used
          function_id - Which assertion function should be used
          parameter - Which parameter should be asserted
Returns:  message - Packed message as string
"""
def pack_message(contract_address : str, function_id : int, parameter) -> str:
    message = "['%s', %d, %s]" % (contract_address, function_id, str(parameter))
    return message

"""
Unpack the message after receiving it over the waku network
Input:    message - Packed message as string
Returns:  contract_address - Which contract should be used
          function_id - Which assertion function should be used
          parameter - Which parameter should be asserted
"""
def unpack_message(message : str):
        msg = copy(message)
        msg = msg.split(',')
        contract_address = msg[0].replace('[', '').replace('\'', '')
        function_id = int(msg[1].replace(' ', ''))
        
        if msg[2][1] != '[':  # Simple Parameter
            parameter = int(msg[2][:-1].replace(' ', ''))
        else:
            if msg[2][2] != '[':  # One Array Parameter
                parameter = []
                parameter.append(int(msg[2][2:]))
                for i in range(3, len(msg)):
                    parameter.append(int(msg[i].replace(' ', '')
                                         .replace(']', '')))
            
            else:  # Two Array Parameter
                parameter = [[], []]
                j = 0
                parameter[j].append(int(msg[2][3:]))
                for i in range(3, len(msg)):
                    parameter[j].append(int(msg[i].replace(' ', '')
                                         .replace(']', '').replace('[', '')))
                    if msg[i][-1] == ']':  # Next array
                        j = 1
        
        ret = (contract_address, function_id, parameter)
        return ret


def main():
    pass


if __name__ == '__main__':
    main()
