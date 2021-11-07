import os
from urllib.request import urlretrieve

import yaml

from downloader import download_all_images
from gen_bbox import check_balance, gen_bbox
from gen_image_list import get_class_id, get_image_id


def create_folders(cf):
    """create folders if don't exist"""
    folder_dict = cf["folders"]
    limit_dict = cf["limit"]

    main_folder_list = [folder_dict[key] for key in folder_dict.keys()]
    img_subfolder_list = [os.path.join(folder_dict["img"], i) for i in limit_dict.keys()]
    txt_subfolder_list = [os.path.join(folder_dict["bbox"], i) for i in limit_dict.keys()]
    folder_list = main_folder_list + img_subfolder_list + txt_subfolder_list

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


def main(cf, annotation=True):
    """pipeline for downloading OID images & annotation files

    cf (dict): configuration params from config.yaml
    annotation (bool): if True, download annotation files
    """

    dl_metadata(cf)

    download_file_suffix = cf["img_downloader"]
    class_id = get_class_id(cf)
    for type_ in cf["limit"]:
        print(f"Generating {type_}-download.txt file...")
        get_image_id(class_id, cf, type_)

        download_file = f'{type_}-{download_file_suffix}'
        # adhere to original script args
        downloader_cf = {"image_list": download_file,
                         "num_processes": cf["threads"],
                         "download_folder": os.path.join(cf["folders"]["img"], type_)}
        download_all_images(downloader_cf)

        if annotation:
            gen_bbox(class_id, cf, type_)
            check_balance(cf, type_)

        print("\n")


if __name__ == "__main__":
    f = open("config.yaml", "r")
    cf = yaml.safe_load(f)
    create_folders(cf)
    main(cf, annotation=True)
