import requests
import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def send_image(filepath):
	print("Fuck")
	f = open(filepath, 'rb')
	print("Requesting")
	r = requests.post('http://keisenb.io:5000/api/image', files={'image': f})
	print(f)
	print("Printed")
	print(r.status_code)
	if(r.status_code is 200):
		return True
	else:
		return False

class FileCreateHandler(FileSystemEventHandler):
	def __init__(self, observer):
		self.observer = observer
	
	def on_created(self, event):
		print("e=", event)
		if not event.is_directory:
			print("File Created")
			send_image(event.src_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    event_handler = FileCreateHandler(observer)
    observer.schedule(event_handler, os.path.join(path, "Images"), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
	

		
send_image('sdfsd')