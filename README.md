# Arduino RX5808 5.8GHz VRX RSSI Logging

Recently, there have been [some projects](https://github.com/voroshkov/Chorus-RF-Laptimer) trying to use the RSSI signal of an RX5808 5.8GHz video receiver to detect when a quadcopter is passing close to the "base-station" to be able to count the laptimes.

I wanted to try this with my 90mm brushless quad in my little garden racetrack.

Unfortunately, it seems the RSSI signal is not really usable in such close ranges. That's why I've more-or-less abandoned this project.

## Hardware

The whole project consists of an [Arduino Micro](https://www.arduino.cc/en/Main/arduinoBoardMicro), a [128x64 I2C OLED display](https://learn.adafruit.com/monochrome-oled-breakouts/wiring-1-dot-3-128x64), an [SD card module](https://www.adafruit.com/product/254) and of course the [RX5808 module](https://www.banggood.com/de/FPV-5_8G-Wireless-Audio-Video-Receiving-Module-RX5808-p-84775.html) with the [SPI mod done](https://github.com/sheaivey/rx5808-pro-diversity/blob/master/docs/rx5808-spi-mod.md).

The pins used on the Arduino can be modified at the beginning of the included Sketch.

[![Photo of RX5808 hardware](http://xythobuz.de/img/rx5808-test-1_small.jpg)](http://xythobuz.de/img/rx5808-test-1.jpg)
[![Photo of RX5808 hardware](http://xythobuz.de/img/rx5808-test-2_small.jpg)](http://xythobuz.de/img/rx5808-test-2.jpg)
[![Photo of RX5808 hardware](http://xythobuz.de/img/rx5808-test-3_small.jpg)](http://xythobuz.de/img/rx5808-test-3.jpg)
[![Photo of RX5808 hardware](http://xythobuz.de/img/rx5808-test-4_small.jpg)](http://xythobuz.de/img/rx5808-test-4.jpg)

## SD-Card CSV logfile

The CSV logfile stored on the SD card looks like this:

    4058, 159
    4212, 161
    4367, 163
    4521, 161
    4674, 160
    4826, 160
    4977, 160

The fist column contains the milliseconds uptime of the Arduino. The seconds column contains the averaged RSSI value read from the ADC hardware.

## Video Overlay Rendering

The included `overlay.py` Python-script can be used to render an overlay plot of the logged RSSI data over flight footage.

See the beginning of the script file for the configuration options you have to change!

[![RSSI Overlay on DVR flight footage](http://img.youtube.com/vi/M0PgVxSJDHw/0.jpg)](http://www.youtube.com/watch?v=M0PgVxSJDHw "RSSI Overlay on DVR flight footage")

## Sources & Licensing

The SPI and RX5808 interfacing code has been taken and modified from the [Chorus-RF-Laptimer](https://github.com/voroshkov/Chorus-RF-Laptimer) by Andrey Voroshkov. This code, as well as all of my code, is released under the MIT license. See the `COPYING` file in this repository.

