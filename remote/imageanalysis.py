from camera import cameraHandler
from gps import gpsHandler
from PIL import Image
import time

# Start GPS
gpsThread = gpsHandler('/dev/ttyUSB0', 9600)
gpsThread.start()

# Get image and save it
cameraThread = cameraHandler()
cameraThread.start()
image = cameraThread.getImage()
cameraThread.close()
cameraThread.join()
saveLocation = "Images/"+time.strftime("%Y%m%d%H%M%S")+".jpg"
image.save(saveLocation)
print("Image Saved!\n")
print(gpsThread.getPos())

gpsThread.close()
gpsThread.join()
