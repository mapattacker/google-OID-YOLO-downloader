import os
import yaml

from gen_image_list import get_class_id, get_image_id
from gen_bbox import gen_bbox, check_balance
from downloader import download_all_images



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


def main(cf):
    """pipeline for downloading OID images & annotation files

    cf (dict): configuration params from config.yaml
    downloader_cf (dict): customised params for downloader.py
    split (bool): execute train-val split of img & txt files
    """
    # download metadata
    dl_metadata(cf)

    # download images list in download.txt
    download_file_suffix = cf["img_downloader"]

    for type_ in cf["type"]:
        # generate *-download.txt
        get_image_id(cf["class"], type_, cf["limit"])

        # download images from *-download.txt
        download_file = f'{type_}-{download_file_suffix}'
            # adhere to original script args
        downloader_cf = {"image_list": download_file,
                         "num_processes": cf["threads"],
                         "download_folder": os.path.join(folder["img"], type_)}
        download_all_images(downloader_cf)

        # generate bbox text files
        gen_bbox(type_)
        check_balance(type_)


if __name__ == "__main__":
    # import configs
    f = open("config.yaml", "r")
    cf = yaml.safe_load(f)

    folder = cf["folders"]
    folder_list = [folder[key] for key in folder.keys()]
    type_list = [os.path.join(folder["img"], i) for i in cf["type"]]
    folder_list = folder_list + type_list
    create_folders(folder_list)

    # execute pipeline
    main(cf)

    