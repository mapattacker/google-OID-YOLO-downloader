import os
import random
import shutil
from math import floor

from tqdm import tqdm


def get_file_list(folder, file_extensions):
    """get list of files from their extensions"""

    file_list = []
    for file in os.listdir(folder):
        if file.endswith(file_extensions):
            file_list.append(file)
    return sorted(file_list)


def train_val_split(img_folder, txt_folder, data_dir, \
                     seed=-1, val_ratio=0.1, val_min=50, \
                     img_ext=(".jpg", "jpeg", ".png", "bmp")):
    """randomised train-val split, copy result splits to data dir"""

    imglist = get_file_list(img_folder, img_ext)
    if seed >= 0:
        random.seed(seed)
    random.shuffle(imglist)
    
    # get train & val images
    total = len(imglist)
    val_total = total * val_ratio
    if val_total < val_min:
        val_total = val_min
    val_images = imglist[:int(val_total)]
    train_images = imglist[int(val_total):]

    # get train & val annotations
    val_txt = [i.split(".")[0] + ".txt" for i in val_images]
    train_txt = [i.split(".")[0] + ".txt" for i in train_images]

    # create train-val image & label folders
    train_f = os.path.join(data_dir, "train")
    val_f = os.path.join(data_dir, "val")
    train_img_dir, train_ann_dir, val_img_dir, val_ann_dir = \
        train_f, train_f, val_f, val_f
    if not os.path.exists(train_img_dir): os.makedirs(train_img_dir)
    if not os.path.exists(train_ann_dir): os.makedirs(train_ann_dir)
    if not os.path.exists(val_img_dir): os.makedirs(val_img_dir)
    if not os.path.exists(val_ann_dir): os.makedirs(val_ann_dir)

    # copy train-val images & labels to data dir
    for img in tqdm(train_images, desc="copy train img"):
        shutil.copy(os.path.join(img_folder, img), train_img_dir)
    for img in tqdm(val_images, desc="copy val img"):
        shutil.copy(os.path.join(img_folder, img), val_img_dir)
    for img in tqdm(train_txt, desc="copy train txt"):
        shutil.copy(os.path.join(txt_folder, img), train_ann_dir)
    for img in tqdm(val_txt, desc="copy val txt"):
        shutil.copy(os.path.join(txt_folder, img), val_ann_dir)

    train_total = len(train_images)
    val_total = len(val_images)
    print("train-val files transferred")
    print(f"Split: Train {train_total} - Val {val_total}")


if __name__ == "__main__":
    import yaml
    f = open("config.yaml", "r")
    cf = yaml.safe_load(f)
    folder = cf["download_folders"]

    train_val_split(
        folder["img"], 
        folder["bbox"], 
        folder["split"],
        seed=1,
        val_ratio=0.3334)