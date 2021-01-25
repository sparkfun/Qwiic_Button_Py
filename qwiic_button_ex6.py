#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_button_ex6.py
#
# Simple Example for the Qwiic Button. Daisy chain together two Qwiic Buttons 
# with different I2C addresses. To change the address of a Qwiic Button, please
# visit example 5.
#------------------------------------------------------------------------
#
# Written by Priynka Makin @ SparkFun Electronics, January 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================
# Example 6

from __future__ import print_function
import qwiic_i2c
import qwiic_button
import time
import sys

def runExample():

    print("\nSparkFun Qwiic Button Example 6")
    myButton1 = qwiic_button.QwiicButton()
    myButton2 = qwiic_button.QwiicButton()

    if myButton1.isConnected() == False:
        print("\nThe Qwiic Button 1 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
            return
    if myButton2.isConnected() == False:
        print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
            file=sys.stderr)
            return
    
    myButton1.begin()
    myButton2.begin()

    while 1:

        # Check if button 1 is pressed
        if myButton1.isPressed() == True:
            print("\nButton 1 is pressed!")

            while myButton1.isPressed() == True:
                wait(10)    # Wait for the user to stop pressing
            print("\nButton 1 is not pressed.")
        
        # Check if button2 is pressed
        if myButton2.isPressed() == True:
            print("\nButton 2 is pressed!")

            while myButton2.isPressed() == True:
                wait(10)    # Wait for the user to stop pressing
            print("\nButton 2 is not pressed.")
        
        wait(20)    # Don't hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)
