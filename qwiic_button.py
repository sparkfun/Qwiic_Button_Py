#-----------------------------------------------------------------------------
# qwiic_button.py
#
# Python library for the SparkFun qwiic button.
#   https://www.sparkfun.com/products/15932
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, January 2021
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
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

"""
qwiic_button
============
Python module for the Qwiic Button.

This python package is a port of the exisiting [SparkFun Qwiic Button Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).

"""
#-----------------------------------------------------------------------------------

import math
import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at runtime.

# This is the name of the device
_DEFAULT_NAME = "Qwiic Button"

# Some devices have  multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the 
# device.
_AVAILABLE_I2C_ADDRESS = [0x6F]

# Define the class that encapsulates the device being created. All information associated 
# with this device is encapsulated by this class. The device class should be the only value
# exported from this module.

class QwiicButton(object):
    """"
    QwiicButton
        
        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The GPIO device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device ID for all Qwiic Buttons
    DEV_ID = 0x5D

    # Registers
    ID = 0x00
    FIRMWARE_MINOR = 0x01
    FIRMWARE_MAJOR = 0x02
    BUTTON_STATUS = 0x03
    INTERRUPT_CONFIG = 0x04
    BUTTON_DEBOUNCE_TIME = 0x05
    PRESSED_QUEUE_STATUS = 0x07
    PRESSED_QUEUE_FRONT = 0x08
    PRESSED_QUEUE_BACK = 0x0C
    CLICKED_QUEUE_STATUS = 0x10
    CLICKED_QUEUE_FRONT = 0x11
    CLICKED_QUEUE_BACK = 0x15
    LED_BRIGHTNESS = 0x19
    LED_PULSE_GRANULARITY = 0x1A
    LED_PULSE_CYCLE_TIME = 0x1B
    LED_PULSE_OFF_TIME = 0x1D
    I2C_ADDRESS = 0x1F

    # Status Flags
    eventAvailable = 0
    hasBeenClicked = 0
    isPressed = 0

    # Interrupt Configuration Flags
    clickedEnable = 0
    pressedEnable = 0

    # Queue Status Flags
    popRequest = 0
    isExmpty = 0
    isFull = 0

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self.address = address if address != None else self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver == None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c == None:
                print("Unable to load I2C driver for this platform.")
                return
            else: 
                self._i2c = i2c_driver

    # -----------------------------------------------
    # isConnected()
    #
    # Is an actual board connected to our system?
    def isConnected(self):
        """
            Determine if a Qwiic Button device is connected to the system.

            :return: True if the device is connected, otherwise False.
            :rtype: bool
        """
        return qwiic._i2c.isDeviceConnected(self.address)
    
    # ------------------------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    def begin(self):
        """
            Initialize the operation of the Qwiic Button
            Run isConnected() and check the ID in the ID register

            :return: Returns true if the intialization was successful, otherwise False.
            :rtype: bool
        """
        if self.isConnected() == True:
            id = self._i2c.readByte(self.address, self.ID)
            
            if id == self.DEV_ID:
                return True
        
        return False
    
    # ------------------------------------------------
    # getFirmwareVersion()
    #
    # Returns the firmware version of the attached devie as a 16-bit integer.
    # The leftmost (high) byte is the major revision number, 
    # and the rightmost (low) byte is the minor revision number.
    def getFirmwareVersion(self):
        """
            Read the register and get the major and minor firmware version number.

            :return: 16 bytes version number
            :rtype: int
        """
        version = self._i2c.readByte(self.address, self.FIRMWARE_MAJOR) << 8
        version |= self._i2c.readByte(self.address, self.FIRMWARE_MINOR)
        return version

    # -------------------------------------------------
    # setI2Caddress(address)
    #
    # Configures the attached device to attach to the I2C bus using the specified address
    def setI2Caddress(self, newAddress):
        """
            Change the I2C address of the Qwiic Button

            :return: True if the change was successful, false otherwise.
            :rtype: bool
        """
        # First, check if the specified address is valid
        if newAddress < 0x08 or newAddress > 0x77:
            return False
        
        # Write new address to the I2C address register of the Qwiic Button
        success = self._i2c.writeByte(self.address, self.I2C_ADDRESS, newAddress)

        # Check if the write was successful
        if success == True:
            self.address = newAddress
            return True
        
        else:
            return False
    
    # ---------------------------------------------------
    # getI2Caddress()
    #
    # Returns the I2C address of the device
    def getI2Caddress(sel):
        """
            Returns the current I2C address of the Qwiic Button

            :return: current I2C address
            :rtype: int
        """
        return self.address