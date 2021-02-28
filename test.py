import mass_download
from glob import glob
import json,os

def download_all_json(to_page):
    links=[]
    for page_number in range(to_page):
        links.append(("https://mars.nasa.gov/rss/api/?feed=raw_images&category={}&feedtype=json&num=100&page={}&order=sol+desc".format("msl",page_number),"json/{}.json".format(page_number)))
    mass_download.download(links,workers=15)

def join_jsons():
    jsons=glob("json/*.json")
    jsons.sort(key=lambda x: int(x.split("json\\")[1].split(".json")[0]))

    images=list()
    for json_path in jsons:
        with open(json_path,"r") as f:
            images+=json.load(f)["images"]
        
    with open("cache.json","w") as f:
        json.dump({"images":images,"max_page":int(jsons[-1].split("json\\")[1].split(".json")[0])},f)

    
def missing(max_page):
    missing=[i for i in range(max_page) if not os.path.exists("json/{}.json".format(i))]
    if len(missing)>0:
        print("Il manque {} fichiers: ".format(len(missing))," ".join(missing))    
    else:
        print("Tout est en ordre")

def download_all_images():
    with open("cache.json","r") as f:
        images=[image for image in json.load(f)["images"] if image["sample_type"]=="full"]

    cameras={image["camera"]["instrument"] for image in images}
    [os.makedirs("output_msl/{}".format(camera),exist_ok=True) for camera in cameras]

    links=[(image["image_files"]["full_res"].replace("mars.jpl.nasa.gov","mars.nasa.gov"),"output_msl/{}/Sol{:04d}_{}.jpg".format(image["camera"]["instrument"],image["sol"],image["imageid"])) for image in images]
    print("Total: {} images".format(len(links)))
    links=[link for link in links if not os.path.exists(link[1])]
    print("Downloading: {} images".format(len(links)))

    mass_download.download(links,workers=5)

    missing=list()
    for link, file_path in links:
        if not os.path.exists(file_path):
            missing.append((link,file_path))
    
    if len(missing)>0:
        print("Missing {} pictures".format(len(missing)))
    else:
        print("All files are downloaded")
    
def format_json():
    with open("cache.json","r") as f:
        images=[image for image in json.load(f)["images"] if image["sample_type"]=="full"]

    with open("output_msl/data.json","w") as f:
        json.dump(images,f)



def count_images_by_cameras():
    with open("cache.json","r") as f:
        images=[image for image in json.load(f)["images"] if image["sample_type"]=="full"]

    cameras={image["camera"]["instrument"] for image in images}
    for camera in cameras:
        print(len([image for image in images if image["camera"]["instrument"]==camera]))

download_all_images()

#format_json()
#count_images_by_cameras()
"""max_page=2975
missing(max_page)
join_jsons()"""