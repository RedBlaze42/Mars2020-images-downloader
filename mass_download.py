import urllib.request
from threading import Thread
from tqdm import tqdm
from time import sleep

def download_retry(url,path):
    while True:
        try:
            urllib.request.urlretrieve(url,path)
        except urllib.error.HTTPError:
            sleep(10)
            continue
        break


def download(data,workers=20):
    threads=[Thread(target=download_retry,args=(line[0],line[1])) for line in data]
    
    for thread in tqdm(threads):
        try:
            while sum([1 for thread in threads if thread.is_alive()])>=workers:
                pass
            thread.start()
        except KeyboardInterrupt:
            print("Arrêt...")
            break
    
    for thread in [thread for thread in threads if thread.is_alive()]:
        thread.join()