import requests
import dateutil.parser
from math import ceil
import json,os
from time import sleep
from tqdm import tqdm

def get_raw_photos(page_number,rover):
    while True:
        r=requests.get("https://mars.nasa.gov/rss/api/?feed=raw_images&category={}&feedtype=json&num=100&page={}&order=sol+desc".format(rover,page_number))
        if r.status_code==200:
            break
        else:
            sleep(10)

    return r.json()

def get_max_photos(rover) -> int:
    return get_raw_photos(0,rover)["total_images"]

def get_photos(rover="mars2020",cache=True):
    if os.path.exists("cache.json") and cache:
        with open("cache.json","r") as f:
            data=json.load(f)
            photos=[MarsPhoto(photo) for photo in data["images"]]
            page_start=max(0,data["max_page"]-1)
    else:
        photos=list()
        page_start=0
        
    max_page=ceil(get_max_photos(rover)/100)
    for page_number in tqdm(range(page_start,max_page)):
        page=get_raw_photos(page_number,rover)
        photos+=[MarsPhoto(photo) for photo in page["images"]]

    if cache:
        with open("cache.json","w") as f:
            api_data={"images":[photo.raw_data for photo in photos],"max_page":max_page}
            json.dump(api_data,f)
    
    return photos

class MarsPhoto():
    
    def __init__(self,json):
        self.raw_data=json
        self.link=json["image_files"]["full_res"]
        self.camera=json["camera"]["instrument"]
        self.is_thumbnail=json["sample_type"]=="Thumbnail"
        self.sol=json["sol"]
        self.id=json['imageid']
    
    @property
    def date_received(self):
        return dateutil.parser.isoparse(self.raw_data["date_received"])

    @property
    def date_taken(self):
        return dateutil.parser.isoparse(self.raw_data["date_taken_utc"])