# CompuCanvas MP series

The CompuCanvas MP series uses an Adafruit [Matrix Portal](https://www.adafruit.com/product/4745) (running [CircuitPython](https://circuitpython.org/)) as the system controller.  One of several RGB matrix panels are placed behind the canvas to produce a low resolution display.

### CompuCanvas MP series variants
* CompuCanvas MP32s - 32x32 matrix
* CompuCanvas MP32h - 64x32 (horizontal) matrix
* CompuCanvas MP32v - 32x64 (vertical) matrix
* CompuCanvas MP64 - 64x64 matrix

The `CCMP` folder here contains a CircuitPython program that will drive the Matrix Portal with features like clocks, background images, message board and more. To try it, copy the contents of the `CCMP` folder into the Matrix Portal `CIRCUITPY` folder. Edit the `cc_config.py` file to configure for your hardware setup. Also, don't forget to create a `secrets.py` file with your WiFi details.
