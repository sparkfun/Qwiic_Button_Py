#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_button_ex4.py
#
# Simple Example for the Qwiic Button. Shows how to use he FIFO Queue on the Qwiic Button.
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
# Example 4

from __future__ import print_function
import qwiic_button
import time
import sys

def runExample():

    print("\nSparkFun Qwiic Button Example 4")
    myButton = qwiic_button.QwiicButton()

    if myButton.isConnected() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    myButton.begin()

    while 1:

        # If the queue of pressed events is not empty
        if myButton.isPressedQueueEmpty() == False:
            # Then print the time since the last and first button press
            print("\n" + myButton.timeSinceLastPress() / 1000.0)
            print("s since he button was last pressed   ")
            print(myButton.timeSinceFistPress() / 1000.0)
            print("s since the button was first pressed ")
        # If the queue is empty
        else: 
            print("ButtonPressed Queue is empty! ")

        # If the queue of clicked events is not empty
        if myButton.isClickedQueueEmpty() == False:
            # Then print the time since the last and first button click
            print(myButton.timeSinceLastClick() / 1000.0)
            print("s since the button was last clicked  ")
            print(myButton.timeSinceFistClick() / 1000.0)
            print("s since the button was first clicked")
        # If the queue is empty
        else:
            print(" ButtonClicked Queue is empty!")
        
        print("\n")

        val = input()
        # If the character is c or C, then pop a value off of the clicked queue
        if char(val) == 'c' or char(val) == 'C':
            myButton.popClickedQueue()
            print("\nPopped ClickedQueue!")
        # If the character is p or P, then pop a value off of the pressed queue
        if char(val) == 'p' or char(val) == 'P':
            myButton.popPressedQueue()
            print("\nPopped PressedQueue!")

        wait(20)    # Let's not hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 4")
        sys.exit(0)