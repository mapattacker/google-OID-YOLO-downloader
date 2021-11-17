import os

from joblib import Parallel, delayed


def get_file_list(folder, file_extensions):
    """get list of files from their extensions"""

    file_list = []
    for file in os.listdir(folder):
        if file.endswith(file_extensions):
            file_list.append(file)
    return sorted(file_list)


def image_attributes(df, IsOccluded, IsTruncated, IsDepiction, IsInside, IsGroupOf):
    """
    Filter out image object attributes as defined by OID

    Args:
        df (dataframe): pandas dataframe
        IsOccluded (bool): Indicates that the object is occluded by another object in the image.
        IsTruncated (bool): Indicates that the object extends beyond the boundary of the image.
        IsGroupOf (bool): Indicates that the box spans a group of objects (e.g., a bed of flowers or a crowd of people). We asked annotators to use this tag for cases with more than 5 instances which are heavily occluding each other and are physically touching.
        IsDepiction (bool): Indicates that the object is a depiction (e.g., a cartoon or drawing of the object, not a real physical instance).
        IsInside (bool): Indicates a picture taken from the inside of the object (e.g., a car interior or inside of a building).
    """
    
    if IsOccluded:
        df = df[df["IsOccluded"].isin([1])]
    elif IsOccluded == False:
        df = df[df["IsOccluded"].isin([0])]
    if IsTruncated:
        df = df[df["IsTruncated"].isin([1])]
    elif IsTruncated == False:
        df = df[df["IsTruncated"].isin([0])]
    if IsGroupOf:
        df = df[df["IsGroupOf"].isin([1])]
    elif IsGroupOf == False:
        df = df[df["IsGroupOf"].isin([0])]
    if IsDepiction:
        df = df[df["IsDepiction"].isin([1])]
    elif IsDepiction == False:
        df = df[df["IsDepiction"].isin([0])]
    if IsInside:
        df = df[df["IsInside"].isin([1])]
    elif IsInside == False:
        df = df[df["IsInside"].isin([0])]
    return df


def total_instances(folder, n_jobs=1):
    """find total number of objects, i.e. bounding boxes"""
    file_list = get_file_list(folder, ".txt")

    def get_instance_file(file):
        f = open(os.path.join(folder, file))
        f = [cnt for cnt, _ in enumerate(f)][-1]+1
        return f

    total = Parallel(n_jobs=n_jobs, backend="threading")(
                delayed(get_instance_file)(f) for f in file_list)

    return sum(total)



if __name__ == "__main__":
    folder = "/Users/Desktop/self/yolov5/datasets/train"
    total = total_instances(folder)
    print(total)
