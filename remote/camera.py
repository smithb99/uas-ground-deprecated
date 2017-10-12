import gps
import io
import json
from PIL import Image
import threading
import time
import unirest

#Class to handle interactions with the camera
class cameraHandler (threading.Thread):

    # Class initializer
    def __init__(self):
        threading.Thread.__init__(self)
        self.__url = 'http://192.168.122.1:8080/sony/camera'
        self.__headers = {'Content-Type':'application/json'}
        self.__requestData = json.dumps({"method": "actTakePicture","params": [],"id": 1,"version": "1.0"})
        self.__cameraLock = threading.Lock()
        self.__image = None
        self.__end = False

    # Method that runs when the thread is started
    #def run(self):

    # Method that saves the image.
    def __saveImage__(self, response):
        self.__image = Image.open(io.BytesIO(response.raw_body))

    # Method that gets the URL of the last image taken.
    def __getImageURL__(self, response):
        self.__imageURL = response.body.get('result')[0][0]
        self.__saveImage = unirest.get(self.__imageURL, callback=self.__saveImage__)

    # Method that sends an asynchronos post request to the camera to take an image.
    def __captureImage__(self):
        self.__captureImage = unirest.post(self.__url, headers=self.__headers, params=self.__requestData, callback=self.__getImageURL__)

    # Method that takes an image and returns it
    def getImage(self):
        self.__cameraLock.acquire()
        self.__captureImage__()
        while True:
            if(self.__image is not None):
                self.__cameraLock.release()
                return self.__image

    # Thread-safe method to stop the otherwise infinite loop and exit the thread.
    def close(self):
        self.__end = True

# Example code for proper class usage

#cameraThread = cameraHandler()
#cameraThread.start()
#image = cameraThread.getImage()
#cameraThread.close()
#cameraThread.join()
