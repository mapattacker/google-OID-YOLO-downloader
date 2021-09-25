import os

import pandas as pd


def get_class_id(class_, csv_folder="csv_folder"):
    """get class id"""
    path = os.path.join(csv_folder, "class-descriptions-boxable.csv")
    class_df = pd.read_csv(path, names=["id", "class"])
    class_id = class_df[class_df["class"]==class_]["id"].values[0]
    return class_id


def get_image_id(
        class_id,
        limit=None,
        IsOccluded=None,
        IsTruncated=None,
        IsGroupOf=None,
        IsDepiction=None,
        IsInside=None,
        type="all", 
        csv_folder="csv_folder"
    ):
    """save list of imageids in text file
    Refer to https://storage.googleapis.com/openimages/web/download.html#download_manually
    
    Args:
        IsOccluded (bool): Indicates that the object is occluded by another object in the image.
        IsTruncated (bool): Indicates that the object extends beyond the boundary of the image.
        IsGroupOf (bool): Indicates that the box spans a group of objects (e.g., a bed of flowers or a crowd of people). We asked annotators to use this tag for cases with more than 5 instances which are heavily occluding each other and are physically touching.
        IsDepiction (bool): Indicates that the object is a depiction (e.g., a cartoon or drawing of the object, not a real physical instance).
        IsInside (bool): Indicates a picture taken from the inside of the object (e.g., a car interior or inside of a building).
"""

    # get file names
    image_file = "-annotations-bbox.csv"
    if type == "all":
        image_file_list = [f"train{image_file}", f"test{image_file}", f"validation{image_file}"]
    else:
        image_file_list = [f"{type}{image_file}"]

    
    # delete output file if already exist
    download_file = 'download.txt'
    if os.path.isfile(download_file):
        os.remove(download_file)

    for file in image_file_list:
        type = file.split("-")[0]
        path = os.path.join(csv_folder, file)
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
        
        # limit result
        if limit:
            image_ids = df[df["LabelName"]==class_id][:limit]
        else:
            image_ids = df[df["LabelName"]==class_id]

        # add type path
        image_ids["ids"] = image_ids["ImageID"].apply(lambda x: type + "/" + x )

        # expend image ids to dl file
        with open(download_file, 'a') as f:
            image_ids["ids"].to_csv(f, header=False, index=False)


if __name__ == "__main__":
    class_id = get_class_id("Flower")
    get_image_id(class_id, 
                    IsOccluded=False, 
                    IsTruncated=False,
                    IsDepiction=False,
                    IsInside=False,
                    limit=20000, type="all")