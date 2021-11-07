import os

import pandas as pd
from tqdm import tqdm

from utils_bbox import Nxxyy2yolo
from utils_preprocess import get_file_list, image_attributes



def gen_bbox(class_id, cf, type_):
    """generate annotation bbox text files for each image downloaded"""

    # load configs
    folder = cf["folders"]
    attr = cf["attributes"]
    IsOccluded = attr["IsOccluded"]
    IsTruncated = attr["IsTruncated"]
    IsDepiction = attr["IsDepiction"]
    IsInside = attr["IsInside"]
    IsGroupOf = attr["IsGroupOf"]

    download_file = f'{type_}-{cf["img_downloader"]}'
    dl_df = pd.read_csv(download_file, sep="/", names=["type", "img"])
    types = dl_df["type"].unique()

    # read annotation file
    bbox_file = f'{type_}-{cf["bbox_suffix"]}'
    bbox_path = os.path.join(folder["metadata"], bbox_file)
    usecols = ["ImageID", "LabelName", "XMin", "XMax", "YMin", "YMax",
                "IsOccluded", "IsTruncated", "IsDepiction", 
                "IsInside", "IsGroupOf"]
    df = pd.read_csv(bbox_path, usecols=usecols)

    # apply filters
    df = image_attributes(df, 
            IsOccluded, IsTruncated, IsDepiction, IsInside, IsGroupOf)
    df = df[df["LabelName"].isin([class_id])]

    img_list = dl_df[dl_df["type"]==type_]["img"].tolist()
    for img in tqdm(img_list, desc="Generating annotations"):
        img_df = df[df["ImageID"].isin([img])]
        img_df = img_df[["XMin", "XMax", "YMin", "YMax"]]

        # iterate each bbox within an image
        for _, box in img_df.iterrows():
            xmin, xmax, ymin, ymax = box
            yolo = Nxxyy2yolo(xmin, xmax, ymin, ymax)
            
            txt_path = os.path.join(folder["bbox"], type_, f'{img}.txt')
            f = open(txt_path, "a")
            f.write(f'0 {yolo[0]} {yolo[1]} {yolo[2]} {yolo[3]}\n')


def check_balance(cf, type_, img_ext=(".jpg", "jpeg", ".png", "bmp")):
    """check all images have corresponding YOLO annotation text files & vice versa"""
    
    folder = cf["folders"]
    img_folder = folder["img"]
    txt_folder = folder["bbox"]

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
        print("Image & label balance check: OK")
    
    return flag

