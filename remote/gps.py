import serial
import threading
import time

#Class to handle interactions with a GPS module
class gpsHandler (threading.Thread):
    
    # Method to initialize the communication port with the given COM port and baudrate
    def __init_serial(self, commPort, baudRate):
        self.__ser = serial.Serial()
        self.__ser.baudrate = baudRate
        self.__ser.port = commPort
        self.__ser.timeout = 1
        self.__ser.open()
    
    # Class initializer which takes a COM port and baudrate as parameters
    def __init__(self, commPort, baudRate):
        threading.Thread.__init__(self)
        self.__locationLock = threading.Lock()
        self.__end = False
        self.__goodFix = False
        self.__init_serial(commPort, baudRate)

    # Method that determines the actions the thread will take when run
    def run(self):
        self.__location = 0
        data = ''
        while not self.__end:
            line = self.__ser.readline()
            #print(line)
            data = line.strip().split(',')
            if data[0] == '$GPGGA' and (self.__goodFix and not(data[6] == 0)):
                result = data[2]+data[3]
                result += ','+data[4]+data[5]
                result += ','+data[9] 
                #print('Found: ' + result)
                self.__locationLock.acquire(1)
                self.__location = result
                self.__locationLock.release()
            elif data[0] == '$GPGSA':
                if(data[2] == '3'):
                    self.__goodFix = True
                    #print('Set goodFix true')
                else:
                    self.__goodFix = False
                    #print('Set goodFix false')
    
    # Thread-safe method to retrieve the GPS position from outside the currently running thread
    def getPos(self):
        self.__locationLock.acquire(1)
        temp = self.__location
        self.__locationLock.release()
        return temp
    
    # Thread-safe method to stop the otherwise infinite loop and exit the thread.
    def close(self):
        self.__end = True

# Example code for proper class usage

#thread = gpsHandler('/dev/ttyUSB0', 9600)
#thread.start()
#
#x = 0
#while x<5:
#   print(thread.getPos())
#   x += 1
#   time.sleep(5)
#
#thread.close()
#thread.join()
#print("Done")

    

