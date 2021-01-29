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

    # Pressed Queue Status Flags
    pressedPopRequest = 0
    pressedIsEmpty = 0
    pressedIsFull = 0

    # Clicked Queue Status Flags
    clickedPopRequest = 0
    clickedIsEmpty = 0
    clickedIsFull = 0

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
        return qwiic_i2c.isDeviceConnected(self.address)
    
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

            :param newAddress: the new I2C address to set the Qwiic Button to
                The function itself checks if the entered parameter is a valid I2C address
            :return: True if the change was successful, false otherwise.
            :rtype: bool
        """
        # First, check if the specified address is valid
        if newAddress < 0x08 or newAddress > 0x77:
            return False
        
        # Write new address to the I2C address register of the Qwiic Button
        self._i2c.writeByte(self.address, self.I2C_ADDRESS, newAddress)

        self.address = newAddress
    
    # ---------------------------------------------------
    # getI2Caddress()
    #
    # Returns the I2C address of the device
    def getI2Caddress(self):
        """
            Returns the current I2C address of the Qwiic Button

            :return: current I2C address
            :rtype: int
        """
        return self.address

    # ---------------------------------------------------
    # isPressed()
    #
    # Returns 1 if the button/switch is pressed, 0 otherwise
    def isButtonPressed(self):
        """
            Returns the value of the isPressed status bit of the BUTTON_STATUS register

            :return: isPressed bit
            :rtype: bool
        """
        # Read the button status register
        buttonStatus = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear all bits but isPressed
        self.isPressed = int(buttonStatus) & ~(0xFB)
        # Shift isPressed to the zero bit
        self.isPressed = self.isPressed >> 2
        # Return isPressed as a bool
        return bool(self.isPressed)
    
    # ----------------------------------------------------
    # hasBeenClicked()
    #
    # Returns 1 if the button/switch is clicked, and 0 otherwise
    def hasButtonBeenClicked(self):
        """
            Returns the value of the hasBeenClicked status bit of the BUTTON_STATUS register

            :return: hasBeenClicked bit
            :rtype: bool
        """
        # Read the button status register
        buttonStatus = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear all bits but hasBeenClicked
        self.hasBeenClicked = int(buttonStatus) & ~(0xFD)
        # Shift hasBeenClicked to the zero bit
        self.hasBeenClicked = self.hasBeenClicked >> 1
        # Return hasBeenClicked as a bool
        return bool(self.hasBeenClicked)
    
    # ------------------------------------------------------
    # getDebounceTime()
    #
    # Returns the time that the button waits for the mechanical
    # contacts to settle in milliseconds.
    def getDebounceTime(self):
        """
            Returns the value in the BUTTON_DEBOUNCE_TIME register

            :return: debounce time in milliseconds
            :rtype: int
        """
        # TODO: just so you know, this will return a list. You need to find out how to concatenate the two items into one time silly
        timeList = self._i2c.readBlock(self.address, self.BUTTON_DEBOUNCE_TIME, 2)
        time = int(timeList[0]) + int(timeList[1]) * 16 ** (2)
        return time
        
    # -------------------------------------------------------
    # setDebounceTime(time)
    #
    # Sets the time that the button waits for the mechanical 
    # contacts to settle in milliseconds.
    def setDebounceTime(self, time):
        """
            Write two bytes into the BUTTON_DEBOUNCE_TIME register

            :param time: the time in milliseconds to set debounce time to
                The max debounce time is 0xFFFF milliseconds, but the function checks if
                the entered parameter is valid
            :return: Nothing
            :rtype: void
        """
        # First check that time is not too big
        if time > 0xFFFF:
            time = 0xFFFF
        time1 = time & ~(0xFF00)
        time2 = time & ~(0x00FF)
        time2 = time2 >> 8
        timeList = [time1, time2]
        # Then write two bytes
        self._i2c.writeWord(self.address, self.BUTTON_DEBOUNCE_TIME, time)
        #self._i2c.writeBlock(self.address, self.BUTTON_DEBOUNCE_TIME, timeList)
        
    # -------------------------------------------------------
    # enablePressedInterrupt()
    #
    # The interrupt will be configured to trigger when the button
    # is pressed. If enableClickedInterrupt() has also been called,
    # then the interrupt will trigger on either a push or a click.
    def enablePressedInterrupt(self):
        """
            Set pressedEnable bit of the INTERRUPT_CONFIG register to a 1

            :return: Nothing
            :rtype: Void
        """
        # First, read the INTERRUPT_CONFIG register
        interruptConfig = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.pressedEnable = 1
        # Set the pressedEnable bit
        interruptConfig = interruptConfig | (self.pressedEnable << 1)
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interruptConfig)
    
    # -------------------------------------------------------
    # disablePressedInterrupt()
    # 
    # Interrupt will no longer be configured to trigger when the
    # button is pressed. If enableClickedInterrupt() has also been called, 
    # then the interrupt will still trigger on the button click.
    def disablePressedInterrupt(self):
        """
            Clear the pressedEnable bit of the INTERRUPT_CONFIG register

            :return: Nothing
            :rtype: Void
        """
        # First, read the INTERRUPT_CONFIG register
        interruptConfig = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.pressedEnable = 0
        # Clear the pressedEnable bit
        interruptConfig = interruptConfig & ~(1 << 1)
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interruptConfig)

    # -------------------------------------------------------
    # enableClickedInterrupt()
    #
    # The interrupt will be configured to trigger when the button
    # is clicked. If enablePressedInterrupt() has also been called, 
    # then the interrupt will trigger on either a push or a click.
    def enableClickedInterrupt(self):
        """
            Set the clickedEnable bit of the INTERRUPT_CONFIG register

            :return: Nothing
            :rtype: Void
        """
        # First, read the INTERRUPT_CONFIG register
        interruptConfig = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.clickedEnable = 1
        # Set the clickedEnable bit
        interruptConfig = interruptConfig | self.clickedEnable
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interruptConfig)

    # -------------------------------------------------------
    # disableClickedInterrupt()
    #
    # The interrupt will no longer be configured to trigger when
    # the button is clicked. If enablePressedInterrupt() has also
    # been called, then the interrupt will still trigger on the 
    # button press.
    def disableClickedInterrupt(self):
        """
            Clear the clickedEnable bit of the INTERRUPT_CONFIG register

            :return: Nothing
            :rtype: Void
        """
        # First, read the INTERRUPT_CONFIG register
        interruptConfig = self._i2c.readByte(self.address, self.INTERRUPT_CONFIG)
        self.clickedEnable = 0
        # Clear the clickedEnable bit
        interruptConfig = interruptConfig & (self.clickedEnable)
        # Write the new interrupt configure byte
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, interruptConfig)
    
    # -------------------------------------------------------
    # available()
    #
    # Returns the eventAvailble bit. This bit is set to 1 if a
    # button click or press event occurred.
    def available(self):
        """
            Return the eventAvailable bit of the BUTTON_STATUS register
            
            :return: eventAvailable bit
            :rtye: bool
        """
        # First, read BUTTON_STATUS register
        buttonStatus = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear all bits but the eventAvailable bit
        self.eventAvailable = int(buttonStatus) & ~(0xFE)
        # Return eventAvailable bit as a bool
        return bool(self.eventAvailable)
    
    # -------------------------------------------------------
    # clearEventBits()
    # 
    # Sets all button status bits (isPressed, hasBeenClicked, 
    # and eventAvailable) to zero.
    def clearEventBits(self):
        """
            Clear the isPressed, hasBeenClicked, and eventAvailable
            bits of the BUTTON_STATUS register

            :return: Nothing
            :rtype: Void
        """
        # First, read BUTTON_STATUS register
        buttonStatus = self._i2c.readByte(self.address, self.BUTTON_STATUS)
        # Convert to binary and clear the last three bits
        buttonStatus = int(buttonStatus) & ~(0x7)
        # Write to BUTTON_STATUS register
        self._i2c.writeByte(self.address, self.BUTTON_STATUS, buttonStatus)
        
    # -------------------------------------------------------
    # resetInterruptConfig()
    #
    # Resets the interrupt configuration back to defaults.
    def resetInterruptConfig(self):
        """
            Enable pressed and clicked interrupts and clear the
            eventAvailable bit of BUTTON_STATUS register

            :return: Nothing
            :rtype: Void
        """
        self.pressedEnable = 1
        self.clickedEnable = 1
        # write 0b11 to the INTERRUPT_CONFIG register
        self._i2c.writeByte(self.address, self.INTERRUPT_CONFIG, 0b11)
        self.eventAvailable = 0
        # Clear hasBeenClicked, isPressed too
        # TODO: not sure if this is right
        self.hasBeenClicked = 0
        self.isPressed = 0
        # Clear the BUTTON_STATUS register by writing a 0
        self._i2c.writeByte(self.address, self.BUTTON_STATUS, 0x00)
    
    # -------------------------------------------------------
    # isPressedQueueFull()
    #
    # Returns true if queue of button press timestamps is full,
    # and false otherwise.
    def isPressedQueueFull(self):
        """
            Returns the isFull bit of the PRESSED_QUEUE_STATUS register

            :return: pressedIsFull
            :rtype: bool
        """
        # First, read the PRESSED_QUEUE_STATUS register
        pressedQueueStat = self._i2c.readByte(self.address, self.PRESSED_QUEUE_STATUS)
        # Convert to binary and clear all bits but isFull
        self.pressedIsFull = int(pressedQueueStat) & ~(0xFE)
        # Return pressedIsFull as a bool
        return bool(self.pressedIsFull)
    
    # -------------------------------------------------------
    # isPressedQueueEmpty()
    #
    # Returns true if the queue of button press timestamps is
    # empty, and false otherwise.
    def isPressedQueueEmpty(self):
        """
            Returns the isEmpty bit of the PRESSED_QUEUE_STATUS register
            
            :return: pressedIsEmpty
            :rtype: bool
        """
        # First, read the PRESSED_QUEUE_STATUS register
        pressedQueueStat = self._i2c.readByte(self.address, self.PRESSED_QUEUE_STATUS)
        # Convert to binary and clear all bits but isEmpty
        self.pressedIsEmpty = int(pressedQueueStat) & ~(0xFD)
        # Shift pressedIsEmpty to the zero bit
        self.pressedIsEmpty = self.pressedIsEmpty >> 1
        # Return pressedIsEmpty as a bool
        return bool(self.pressedIsEmpty)

    # ------------------------------------------------------
    # timeSinceLastPress()
    #
    # Returns how many milliseconds it has been since the last
    # button press. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def timeSinceLastPress(self):
        """
            Returns the four bytes of PRESSED_QUEUE_FRONT.
            Time in milliseconds.

            :return: PRESSED_QUEUE_FRONT
            :rtype: int
        """
        # TODO: not sure if this will work because this read might return a list?
        timeList = self._i2c.readBlock(self.address, self.PRESSED_QUEUE_FRONT, 4)
        time = int(timeList[0]) + int(timeList[1]) * 16 ** (2) + int(timeList[2]) * 16 ** (4) + int(timeList[3]) * 16 ** (6) 
        return time
        
    # -------------------------------------------------------
    # timeSinceFirstPress()
    #
    # Returns how many milliseconds it has been since the first 
    # button press. Since this returns a 32-bit int, it will 
    # roll over about every 50 days.
    def timeSinceFirstPress(self):
        """
            Returns the four bytes of PRESSED_QUEUE_BACK.
            Time in milliseconds

            :return: PRESSED_QUEUE_BACK
            :rtype: int
        """
        timeList = self._i2c.readBlock(self.address, self.PRESSED_QUEUE_BACK, 4)
        time = int(timeList[0]) + int(timeList[1]) * 16 ** (2) + int(timeList[2]) * 16 ** (4) + int(timeList[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------
    # popPressedQueue()
    #
    # Returns the oldest value in the queue (milliseconds since 
    # first button press), and then removes it.
    def popPressedQueue(self):
        """
            Returns contents of PRESSED_QUEUE_BACK register and 
            writes a 1 to popRequest bit of PRESSED_QUEUE_STATUS
            register.

            :return: PRESSED_QUEUE_BACK
            :rtype: int
        """
        # Get the time in milliseconds since the button was first pressed
        tempData = self.timeSinceFirstPress()
        # Read PRESSED_QUEUE_STATUS register
        pressedQueueStat = self._i2c.readByte(self.address, self.PRESSED_QUEUE_STATUS)
        self.pressedPopRequest = 1
        # Set popRequest bit to 1
        pressedQueueStat = pressedQueueStat | (self.pressedPopRequest << 2)
        self._i2c.writeByte(self.address, self.PRESSED_QUEUE_STATUS, pressedQueueStat)
        return tempData
    
    # ---------------------------------------------------------
    # isClickedQueueFull()
    #
    # Returns true if the queue of button click timestamps is full
    # and false otherwise.
    def isClickedQueueFull(self):
        """
            Reads the isFull bit of the CLICKED_QUEUE_STATUS register

            :return: clickedIsFull
            :rtype: bool
        """
        # First, read the CLICKED_QUEUE_STATUS register
        clickedQueueStat = self._i2c.readByte(self.address, self.CLICKED_QUEUE_STATUS)
        # Convert to binary and clear all bits but clickedIsFull
        self.clickedIsFull = int(clickedQueueStat) & ~(0xFE)
        # Return clickedIsFull as a bool
        return bool(self.clickedIsFull)
    
    # ----------------------------------------------------------
    # isClickedQueueEmpty()
    #
    # Returns true if the queue click timestamps is empty and false
    # otherwise.
    def isClickedQueueEmpty(self):
        """
            Reads the isEmpty bit of the CLICKED_QUEUE_STATUS register

            :return: clickedIsEmpty
            :rtype: bool
        """
        # First, read the CLICKED_QUEUE_STATUS register
        clickedQueueStat = self._i2c.readByte(self.address, self.CLICKED_QUEUE_STATUS)
        # Convert to binary and clear all bits but clickedIsEmpty
        self.clickedIsEmpty = int(clickedQueueStat) & ~(0xFD)
        # Shift clickedIsEmpty to the zero bit
        self.clickedIsEmpty = self.clickedIsEmpty >> 1
        # Return clickedIsEmpty as a bool
        return bool(self.clickedIsEmpty)

    # ------------------------------------------------------------
    # timeSinceLastClick()
    #
    # Returns how many milliseconds it has been since the last button
    # click. Since this returns a 32-bit int, it will roll over about
    # every 50 days
    def timeSinceLastClick(self):
        """
            Returns the four bytes of CLICKED_QUEUE_FRONT register.
            Time in milliseconds

            :return: CLICKED_QUEUE_FRONT
            :rtype: int
        """
        timeList = self._i2c.readBlock(self.address, self.CLICKED_QUEUE_FRONT, 4)
        time = int(timeList[0]) + int(timeList[1]) * 16 ** (2) + int(timeList[2]) * 16 ** (4) + int(timeList[3]) * 16 ** (6)
        return time
        
    # ------------------------------------------------------------
    # timeSinceFirstClick()
    #
    # Returns how many milliseconds it has been since the first button
    # click. Since this returns a 32-bit int, it will roll over about 
    # every 50 days
    def timeSinceFirstClick(self):
        """
            Returns the four bytes of CLICKED_QUEUE_BACK register.
            Time in milliseconds

            :return: CLICKED_QUEUE_BACK
            :rtype: int
        """
        timeList = self._i2c.readBlock(self.address, self.CLICKED_QUEUE_BACK, 4)
        time = int(timeList[0]) + int(timeList[1]) * 16 ** (2) + int(timeList[2]) * 16 ** (4) + int(timeList[3]) * 16 ** (6)
        return time
        
    # -------------------------------------------------------------
    # popClickedQueue()
    #
    # Returns the oldest value in the queue (milliseconds since first
    # button click), and then removes it.
    def popClickedQueue(self):
        """
            Returns contents of CLICKED_QUEUE_BACK register and 
            writes a 1 to popRequest bit of CLICKED_QUEUE_STATUS
            register.

            :return: CLICKED_QUEUE_BACK
            :rtype: int
        """
        # Get the time in milliseconds since the button was first clicked
        tempData = self.timeSinceFirstClick()
        # Read CLICKED_QUEUE_STATUS register
        clickedQueueStat = self._i2c.readByte(self.address, self.CLICKED_QUEUE_STATUS)
        self.clickedPopRequest = 1
        # Set popRequest bit to 1
        clickedQueueStat = clickedQueueStat | (self.clickedPopRequest << 2)
        self._i2c.writeByte(self.address, self.CLICKED_QUEUE_STATUS, clickedQueueStat)
        return tempData

    # -------------------------------------------------------------
    # LEDconfig(brightness, cycleTime, offTime, granularity)
    #
    # Configures the LED with the given max brightness, granularity
    # (1 is fine for most applications), cycle time, and off time.
    def LEDconfig(self, brightness, cycleTime, offTime, granularity = 1):
        """
            Write brightness, cycleTime, offTime, and granularity
            parameters to their respective registers: LED_BRIGHTNESS,
            LED_PULSE_CYCLE_TIME, LED_PULSE_OFF_TIME, LED_PULSE_GRANULARITY

            :param brightness: between 0 (led off) and 255 (max brightness)
            :param cycleTime: total pulse cycle in in milliseconds
                Range 0 to 0xFFFF
            :param offTime: off time between pulses in milliseconds
                Range 0 to 0xFFFF
            :param granularity: the amount of steps it takes to get to led brightness
                If not provided, granularity defaults to 1
            :return: Nothing
            :rtype: Void
        """
        # Write brightness
        self._i2c.writeByte(self.address, self.LED_BRIGHTNESS, brightness)
        # Write cycleTime
        self._i2c.writeWord(self.address, self.LED_PULSE_CYCLE_TIME, cycleTime)
        # Write offTime
        self._i2c.writeWord(self.address, self.LED_PULSE_OFF_TIME, offTime)
        # Write granularity
        self._i2c.writeByte(self.address, self.LED_PULSE_GRANULARITY, granularity)
    
    # --------------------------------------------------------------
    # LEDoff()
    #
    # Turn the onboard LED off
    def LEDoff(self):
        """
            Write zero's to all the LED registers: LED_BRIGHTNESS,
            LED_PULSE_CYCLE_TIME, LED_PULSE_OFF_TIME, and LED_PULSE_GRANULARITY
            defaults to zero.

            :return: Nothing
            :rtype: void
        """
        self.LEDconfig(0, 0, 0)
    
    # --------------------------------------------------------------
    # LEDon(brightness)
    #
    # Turns the onboard LED on with specified brightness. Set brightness
    # to an integer between 0 and 255, where 0 is off and 255 is max
    # brightness.
    def LEDon(self, brightness):
        """
            Set LED on without pulse

            :param brightness: between 0 (led off) and 255 (max brightness)
            :return: Nothing
            :rtype: Void
        """
        self.LEDconfig(brightness, 0, 0)
