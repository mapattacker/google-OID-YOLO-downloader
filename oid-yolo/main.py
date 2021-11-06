import os
import yaml

from gen_image_list import get_class_id, get_image_id
from gen_bbox import gen_bbox, check_balance
from downloader import download_all_images
from utils_preprocess import train_val_split



def create_folders(folder_list):
    """create folders if don't exist"""
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)


def dl_metadata(cf):
    """download metadata from OID"""
    meta_files = [f'{i}-{cf["bbox_suffix"]}' for i in cf["type"]]
    meta_files.append("class-descriptions-boxable.csv")
    meta_paths = [os.path.join(cf["folders"]["metadata"], i) for i in meta_files]

    not_exist = False
    for file_path in meta_paths:
        if not os.path.isfile(file_path):
            not_exist = True
    if not_exist:
        os.system("sh download_metadata.sh")


def main(cf, downloader_cf, split=True):
    # download metadata
    dl_metadata(cf)
    
    # # generate download.txt
    get_image_id(cf["class"], cf["limit"])

    # download images list in download.txt
    download_all_images(downloader_cf)

    # generate bbox text files
    gen_bbox()
    check_balance()

    folder = cf["folders"]
    if split:
        print("Executing train-val split")
        train_val_split(
            folder["img"], folder["bbox"], folder["split"],
            seed=cf["split"]["seed"],
            val_ratio=cf["split"]["val_ratio"],
            val_min=cf["split"]["val_min"])


if __name__ == "__main__":
    # import configs
    f = open("config.yaml", "r")
    cf = yaml.safe_load(f)

    folder = cf["folders"]
    folder_list = [folder[key] for key in folder.keys()]
    create_folders(folder_list)

    # adhere to original script args
    downloader_cf = {
            "image_list": cf["img_downloader"], 
            "num_processes": 10,
            "download_folder": folder["img"]}

    # execute pipeline
    main(cf, downloader_cf)

    