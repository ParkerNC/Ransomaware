import sys
import time
import logging
from watchdog.observers import Observer  #creating an instance of the watchdog.observers.Observer from watchdogs class.
from watchdog.events import LoggingEventHandler  #implementing a subclass of watchdog.events.FileSystemEventHandler which is LoggingEventHandler in our case

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  #Scheduling monitoring of a path with the observer instance and event handler. There is 'recursive=True' because only with it enabled, watchdog.observers.Observer can monitor sub-directories
    observer.start()  #for starting the observer thread
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()