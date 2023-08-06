import sys, os 

testdir = os.path.dirname(__file__)
srcdir = '../super_calculator_banbar'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import add_subtract as base_module

def multiply_two_numbers(num1, num2):
    t = 0
    for i in range(num2): 
        t = t + base_module.add_two_numbers(num1, 0)
    
    return t

def divide_two_numbers(num1, num2):
    # integer division
    t = 0
    if(num1 > num2):
        remainder = num1
        while(remainder >= num2):
            t = t+1
            remainder = base_module.subtract_two_numbers(remainder, num2)
    else:
        return t
    
    return t
        
        