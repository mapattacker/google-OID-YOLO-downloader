import os

import pandas as pd
import yaml

from utils_preprocess import image_attributes



def get_class_id(cf):
    """get class id"""
    path = os.path.join(cf["folders"]["metadata"], cf["class_csv"])
    class_df = pd.read_csv(path, names=["id", "class"])
    class_id = class_df[class_df["class"]==cf["class"]]["id"].values[0]
    return class_id


def get_image_id(class_id, cf, type_):
    """save list of imageids in text file
    Refer to https://storage.googleapis.com/openimages/web/download.html#download_manually
    
    Args:
        class (str): class_name as specified by OID
        type_ (str): "train", "validation", or "test"
        limit (int): number of images of each type to download
        type (str): "all", "train", "validation", or "test"
    """
    
    folder = cf["folders"]
    limit = cf["limit"][type_]
    csv_folder = folder["metadata"]
    class_ = cf["class"]
    attr = cf["attributes"]
    IsOccluded = attr["IsOccluded"]
    IsTruncated = attr["IsTruncated"]
    IsDepiction = attr["IsDepiction"]
    IsInside = attr["IsInside"]
    IsGroupOf = attr["IsGroupOf"]
    
    download_file_suffix = cf["img_downloader"]
    annotation_file_suffix = cf["bbox_suffix"]
    
    download_file = f'{type_}-{download_file_suffix}'
    annotation_file = f"{type_}-{annotation_file_suffix}"

    # delete output file if already exist
    if os.path.isfile(download_file):
        os.remove(download_file)

    # read annotation file
    path = os.path.join(csv_folder, annotation_file)
    usecols = ["ImageID", "LabelName", "IsOccluded", "IsTruncated", 
               "IsDepiction", "IsInside", "IsGroupOf"]
    df = pd.read_csv(path, usecols=usecols)

    # apply filters
    df = image_attributes(df, 
            IsOccluded, IsTruncated, IsDepiction, IsInside, IsGroupOf)
    df = df.drop_duplicates(subset=["ImageID"])
    image_ids = df[df["LabelName"].isin([class_id])][:limit]

    # add type path
    image_ids["ids"] = image_ids["ImageID"].apply(lambda x: type_ + "/" + x )

    # expend image ids to dl file
    with open(download_file, 'a') as f:
        image_ids["ids"].to_csv(f, header=False, index=False)


if __name__ == "__main__":
    get_image_id("Flower", "test", limit=cf["limit"])