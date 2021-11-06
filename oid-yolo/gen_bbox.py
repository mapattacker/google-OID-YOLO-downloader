import os

import pandas as pd
import yaml
from tqdm import tqdm

from utils_preprocess import get_file_list, image_attributes
from utils_bbox import Nxxyy2yolo


# import configs
f = open("config.yaml", "r")
cf = yaml.safe_load(f)

folder = cf["folders"]
attr = cf["attributes"]

IsOccluded = attr["IsOccluded"]
IsTruncated = attr["IsTruncated"]
IsDepiction = attr["IsDepiction"]
IsInside = attr["IsInside"]
IsGroupOf = attr["IsGroupOf"]


def gen_bbox(type_):
    """generate annotation bbox text files for each image downloaded"""

    download_file = f'{type_}-{cf["img_downloader"]}'
    dl_df = pd.read_csv(download_file, sep="/", names=["type", "img"])
    types = dl_df["type"].unique()

    bbox_file = f'{type_}-{cf["bbox_suffix"]}'
    bbox_path = os.path.join(folder["metadata"], bbox_file)

    print(f"reading {bbox_path}...")
    df = pd.read_csv(bbox_path)

    # filter by attributes
    df = image_attributes(df, 
            IsOccluded, IsTruncated, IsDepiction, IsInside, IsGroupOf)

    print(f"extracting from {type_}")
    img_list = dl_df[dl_df["type"]==type_]["img"].tolist()
    for img in tqdm(img_list):
        img_df = df[df["ImageID"]==img]
        img_df = img_df[["XMin", "XMax", "YMin", "YMax"]]

        # iterate each bbox within an image
        for _, box in img_df.iterrows():
            xmin, xmax, ymin, ymax = box
            yolo = Nxxyy2yolo(xmin, xmax, ymin, ymax)
            
            txt_path = os.path.join(folder["bbox"], type_, f'{img}.txt')
            f = open(txt_path, "a")
            f.write(f'0 {yolo[0]} {yolo[1]} {yolo[2]} {yolo[3]}\n')


def check_balance(
        type_,
        img_folder=folder["img"], 
        txt_folder=folder["bbox"], 
        img_ext=(".jpg", "jpeg", ".png", "bmp")):
    """check all images have corresponding YOLO annotation text files & vice versa"""

    img_folder = os.path.join(img_folder, type_)
    txt_folder = os.path.join(txt_folder, type_)

    imglist = get_file_list(img_folder, img_ext)
    txtlist = get_file_list(txt_folder, (".txt"))

    imglist_noext = [i.split(".")[0] for i in imglist]
    txtlist_noext = [i.split(".")[0] for i in txtlist]

    flag = False
    for img in imglist:
        imgname = img.split(".")[0]
        if imgname not in txtlist_noext:
            flag = True
            print("ERR:" + img + " does not have a corresponding txt annotation")

    for txt in txtlist:
        txtname = txt.split(".")[0]
        if txtname not in imglist_noext:
            flag = True
            print("ERR:" + txt + " does not have a corresponding image")

    if flag == False:
        print("image & label balance check: OK")
    
    return flag

