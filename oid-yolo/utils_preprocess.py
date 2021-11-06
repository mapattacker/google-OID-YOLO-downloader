import os


def get_file_list(folder, file_extensions):
    """get list of files from their extensions"""

    file_list = []
    for file in os.listdir(folder):
        if file.endswith(file_extensions):
            file_list.append(file)
    return sorted(file_list)


def image_attributes(df, IsOccluded, IsTruncated, IsDepiction, IsInside, IsGroupOf):
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
    return df