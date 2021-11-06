import os
from urllib.request import urlretrieve

import yaml

from downloader import download_all_images
from gen_bbox import check_balance, gen_bbox
from gen_image_list import get_class_id, get_image_id


def create_folders(folder_list):
    """create folders if don't exist"""
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)


def dl_metadata(cf):
    """download metadata from OID"""
    folders = cf["folders"]

    # download class csv if not exist
    class_path = os.path.join(folders["metadata"], cf["class_csv"])
    if not os.path.isfile(class_path):
        print(f'Downloading {cf["class_csv"]}...')
        urlretrieve(cf["url"]["class"], class_path)
    
    # download train-val-test annotation csv
    for type_ in cf["limit"].keys():
        annotation_file = f'{type_}-{cf["bbox_suffix"]}'
        annotation_path = os.path.join(folders["metadata"], annotation_file)
        if not os.path.isfile(annotation_path):
            print(f'Downloading {annotation_file}...')
            urlretrieve(cf["url"][type_], annotation_path)


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

    for type_ in cf["limit"]:
        # generate *-download.txt
        get_image_id(cf["class"], type_, cf["limit"][type_])

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
    type_list = [os.path.join(folder["img"], i) for i in cf["limit"].keys()]
    folder_list = folder_list + type_list
    create_folders(folder_list)

    # execute pipeline
    main(cf)

    