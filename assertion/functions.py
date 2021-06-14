"""
Author: JV
Date: 2021-04-26

Holds all the functions for validation
"""
from typing import Sequence

class FunctionEntry:
    def __init__(self, function_id : int, name : str, function):
        self.function_id = function_id
        self.name = name
        self.function = function


class Functions:
    def __init__(self, entries : Sequence[FunctionEntry]):
        self.entries = dict()
        
        for entry in entries:
            self.entries[entry.function_id] = entry
    
    def get_function_by_id(self, function_id : int):
        return self.entries[function_id].function
    
    def get_function_by_name(self, name : str):
        for _, entry in self.entries.items():
            if entry.name == name:
                return entry.function
    
    def get_id_by_name(self, name : str):
        for _, entry in self.entries.items():
            if entry.name == name:
                return entry.function_id
        return -1
    
    def get_name_by_id(self, function_id : int):
        return self.entries[function_id].name

# Data structure which contains all functions
FUNCTIONS = Functions([
    # Dummy
    FunctionEntry(function_id = 0,      name = "dummy",             function = (lambda parameter, testcase: testcase == parameter)),
    
    # Parameter
    
    
    # Arrays
    FunctionEntry(function_id = 200,    name = "sorted_array",      function = (lambda parameter, testcase: parameter[testcase] > parameter[testcase+1])),
    
    # Double Arrays
    FunctionEntry(function_id = 300,    name = "greater_array",     function = (lambda parameter, testcase: parameter[0][testcase[0]] >= parameter[1][testcase[1]]))
])


def main():
    pass


if __name__ == '__main__':
    main()