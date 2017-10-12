# Image Analysis 2.0 #


## Camera Triggering ##
camera.py is and asynchronously takes and saves pictures onto the disk.

p2.py is the original python2 code that takes a single image.

## Note: This library is in python 2
## Note: This library must be run on a linux host

### Setup ###
Before running camera.py, make sure that your Sony QX1 is on and that you're connected to the wifi network.

camera.py requires the following external python2 libraries:

* unirest
* pillow

## Image Transmission ##
Send_Image.py asynchronously monitors the Images folder for new file additions and sends any new file to 
the configured server

### Setup ### 
Before running Send_Image.py the following packages must be installed:
- Watchdog

## Note: This library is in python 3
