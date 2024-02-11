import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py") and not event.src_path.endswith("watcher.py"): 
            print(f"Detected change in {event.src_path}")
            subprocess.run(["python", event.src_path], shell=True)

event_handler = MyHandler()
observer = Observer()

path_to_watch = input("What folder to watch? (skip to watch all filex) ")

# default path is a current folder'.'
path = path_to_watch or "." 

observer.schedule(event_handler, path, recursive=True)
observer.start()

print(f"I'm watching the {path} folder. Now go and do your job")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()