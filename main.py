import nasa_photo
import os
import mass_download

photos=nasa_photo.get_photos(rover="mars2020")

def update_photos():
    dirs={photo.camera for photo in photos}
    [os.makedirs("output/{}".format(directory),exist_ok=True) for directory in dirs]
    download_list=[(photo.link,"output/{}/{}.{}".format(photo.camera,photo.id,photo.link[-4:])) for photo in photos if not os.path.exists("output/{}/{}.png".format(photo.camera,photo.id)) and not photo.is_thumbnail and photo.raw_data["camera"]["filter_name"] in ["ZCAM_R0_RGB","UNK"]]
    mass_download.download(download_list,workers=30)

update_photos()
