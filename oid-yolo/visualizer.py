"""Adapted from
https://stackoverflow.com/questions/64096953/how-to-convert-yolo-format-bounding-box-coordinates-into-opencv-format
"""

import os

import cv2
import matplotlib.pyplot as plt
import yaml


def display(img_id, img_folder, txt_folder, display=False):
    """plot yolo bbox in image"""

    img = cv2.imread(os.path.join(img_folder, img_id+".jpg"))
    dh, dw, _ = img.shape

    fl = open(os.path.join(txt_folder, img_id+".txt"))
    data = fl.readlines()
    fl.close()

    for dt in data:

        # Split string to float
        _, x, y, w, h = map(float, dt.split(' '))

        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)
        
        if l < 0: l = 0
        if r > dw - 1: r = dw - 1
        if t < 0: t = 0
        if b > dh - 1: b = dh - 1

        cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), thickness=3)

    # convert to RBG
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    if display:
        plt.show()
    else:
        plt.savefig("display.png", dpi=300)


if __name__ == "__main__":
    f = open("config.yaml", "r")
    cf = yaml.safe_load(f)
    folder = cf["folders"]

    img_id = "07f377b473ef2622"
    img_folder = os.path.join(folder["img"], "test")
    txt_folder = os.path.join(folder["bbox"], "test")
    display(img_id, img_folder, txt_folder, display=True)
