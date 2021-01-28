#!/usr/bin/env python
#-----------------------------------------------------------------------------
# qwiic_button_ex3.py
#
# Simple Example for the Qwiic Button. Checks whether the button is pressed and
# and the LED pulses if it is.
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
# Example 3

from __future__ import print_function
import qwiic_button
import time
import sys

brightness = 250    # The maximum brightness of the pulsing LED. Can be between 0 and 255
cycleTime = 1000    # The total time for the pulse to take. Set to a bigger number for a slower pulse or a smaller number for a faster pulse
offTime = 200       # The total time to stay off between pulses. Set to 0 to be pulsing continuously.

def runExample():

    print("\nSparkFun Qwiic Button Example 3")
    myButton = qwiic_button.QwiicButton()

    if myButton.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
    print("\nButton ready!")

    myButton.LEDoff()

    while True:
        
        if myButton.isButtonPressed() == True:

            print("\nThe button is pressed!")
            myButton.LEDconfig(brightness, cycleTime, offTime)
        
        else:
            print("\nThe button is not pressed.")
            myButton.LEDoff()
        
        time.sleep(0.02)    # Let's not hammer too hard on the I2C bus

if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 3")
        sys.exit(0)
