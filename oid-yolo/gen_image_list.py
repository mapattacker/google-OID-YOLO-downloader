import os

import pandas as pd
import yaml


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



def get_class_id(class_, csv_folder=folder["metadata"]):
    """get class id"""
    path = os.path.join(csv_folder, "class-descriptions-boxable.csv")
    class_df = pd.read_csv(path, names=["id", "class"])
    class_id = class_df[class_df["class"]==class_]["id"].values[0]
    return class_id


def get_image_id(class_, limit, csv_folder=folder["metadata"]):
    """save list of imageids in text file
    Refer to https://storage.googleapis.com/openimages/web/download.html#download_manually
    
    Args:
        class (str): class_name as specified by OID
        limit (int): number of images of each type to download
        IsOccluded (bool): Indicates that the object is occluded by another object in the image.
        IsTruncated (bool): Indicates that the object extends beyond the boundary of the image.
        IsGroupOf (bool): Indicates that the box spans a group of objects (e.g., a bed of flowers or a crowd of people). We asked annotators to use this tag for cases with more than 5 instances which are heavily occluding each other and are physically touching.
        IsDepiction (bool): Indicates that the object is a depiction (e.g., a cartoon or drawing of the object, not a real physical instance).
        IsInside (bool): Indicates a picture taken from the inside of the object (e.g., a car interior or inside of a building).
        type (str): "all", "train", "validation", or "test"
    """

    class_id = get_class_id(class_, csv_folder)

    # # get file names
    # image_file = "-annotations-bbox.csv"
    # if type == "all":
    #     image_file_list = [f"train{image_file}", f"test{image_file}", f"validation{image_file}"]
    # else:
    #     image_file_list = [f"{type}{image_file}"]

    
    download_file_suffix = cf["img_downloader"]
    annotation_file_suffix = cf["bbox_suffix"]
    for type_ in cf["type"]:
        download_file = f'{type_}-{download_file_suffix}'
        annotation_file = f"{type_}-{annotation_file_suffix}"

        # delete output file if already exist
        if os.path.isfile(download_file):
            os.remove(download_file)

        path = os.path.join(csv_folder, annotation_file)
        print(f"reading {path}...")
        df = pd.read_csv(path)

        # filter by attributes
        if IsOccluded:
            df = df[df["IsOccluded"]==1]
        elif IsOccluded == False:
            df = df[df["IsOccluded"]==0]
        if IsTruncated:
            df = df[df["IsTruncated"]==1]
        elif IsTruncated == False:
            df = df[df["IsTruncated"]==0]
        if IsGroupOf:
            df = df[df["IsGroupOf"]==1]
        elif IsGroupOf == False:
            df = df[df["IsGroupOf"]==0]
        if IsDepiction:
            df = df[df["IsDepiction"]==1]
        elif IsDepiction == False:
            df = df[df["IsDepiction"]==0]
        if IsInside:
            df = df[df["IsInside"]==1]
        elif IsInside == False:
            df = df[df["IsInside"]==0]
        
        df = df.drop_duplicates(subset=['ImageID'])

        # limit result
        if limit:
            image_ids = df[df["LabelName"]==class_id][:limit]
        else:
            image_ids = df[df["LabelName"]==class_id]

        # add type path
        image_ids["ids"] = image_ids["ImageID"].apply(lambda x: type_ + "/" + x )

        # expend image ids to dl file
        with open(download_file, 'a') as f:
            image_ids["ids"].to_csv(f, header=False, index=False)


if __name__ == "__main__":
    get_image_id("Flower", limit=cf["limit"])