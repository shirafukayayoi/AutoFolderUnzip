from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import zipfile
import time

class Watcher:
    DIRECTORY_TO_WATCH = input("監視するフォルダのパスを入力してください：")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print("監視中...")
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("問題が発生したため、監視を終了します。")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.src_path.endswith('.zip'):
            print(f"{event.src_path} ファイルが作成されました。")
            unzip_and_delete(event.src_path)

def unzip_and_delete(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        unzip_path = os.path.splitext(zip_path)[0]
        zip_ref.extractall(unzip_path)
        print(f"{zip_path} を解凍しました。")
    os.remove(zip_path)
    print(f"{zip_path} を削除しました。")

if __name__ == '__main__':
    w = Watcher()
    w.run()