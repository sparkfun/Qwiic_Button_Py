Qwiic_Button_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-button/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-button.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Button_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_Button_Py.svg" /></a>
	<a href="https://qwiic-button-py.readthedocs.io/en/main/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-button-py/badge/?version=main&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_Button_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>

</p>

<img src="https://cdn.sparkfun.com/assets/parts/1/4/5/7/3/15932-SparkFun_Qwiic_Button_-_Red-01.jpg"  align="right" width=300 alt="SparkFun Qwiic Button">

Python module for the [SparkFun Qwiic Button](https://www.sparkfun.com/products/15932)

This module is also compatible with the following products:
* [SparkFun Qwiic Button - Green LED](https://www.sparkfun.com/products/16842)
* [SparkFun Qwiic Button Breakout](https://www.sparkfun.com/products/15931)
* [Qwiic Arcade - Red](https://www.sparkfun.com/products/15591)
* [Qwiic Arcade - Blue](https://www.sparkfun.com/products/15592)
* [Qwiic Switch](https://www.sparkfun.com/products/15586)

Please remember that SparkX products are experimental, therefore full functionality is not gauranteed.

This python package is a port of the existing [SparkFun Qwiic Button Arduino Library](https://github.com/sparkfun/SparkFun_Qwiic_Button_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
The Qwiic Button Python package current supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)
* [NVidia Jetson Nano](https://www.sparkfun.com/products/15297)
* [Google Coral Development Board](https://www.sparkfun.com/products/15318)

Dependencies
--------------
This driver package depends on the qwiic I2C driver:
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic Button module documentation is hosted at [ReadTheDocs](https://qwiic-button-py.readthedocs.io/en/main/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-button](https://pypi.org/project/sparkfun-qwiic-button/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-button
```
For the current user:

```sh
pip install sparkfun-qwiic-button
```
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun-qwiic-button-<version>.tar.gz
```

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_button 
import time
import sys

def run_example():

    print("\nSparkFun Qwiic Button Example 1")
    my_button = qwiic_button.QwiicButton()

    if my_button.begin() == False:
        print("\nThe Qwiic Button isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nButton ready!")
    
    while True:   
        
        if my_button.is_button_pressed() == True:
            print("\nThe button is pressed!")

        else:    
            print("\nThe button is not pressed!")
            
        time.sleep(0.02)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)


```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
