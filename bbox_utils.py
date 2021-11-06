"""utility scripts for bbox format conversions"""


def xxyy2yolo(xmin, xmax, ymin, ymax):
    """convert normalised xxyy OID format to yolo format"""

    ratio_cx = (xmin + xmax)/2
    ratio_cy = (ymin + ymax)/2
    ratio_bw = xmax - xmin
    ratio_bh = ymax - ymin

    return (ratio_cx, ratio_cy, ratio_bw, ratio_bh)


def xxyy2yolo(size, box):
    """convert XMin	XMax YMin YMax coordinates to yolo format
    
    Args
    ----
    size (tuple): (width, height)
    box (tuple): (xmin, xmax, ymin, ymax)

    Returns
    -------
    yolo (tuple): (ratio-bbox-centre-x, ratio-bbox-centre-y, ratio-bbox-w, ratio-bbox-h)
    """
    width = size[0]
    height = size[1]
    xmin, xmax, ymin, ymax = box
    box_width = xmax - xmin
    box_height = ymax - ymin

    center_x = xmin + (box_width / 2.0)
    center_y = ymin + (box_height / 2.0)

    ratio_cx = center_x / width
    ratio_cy = center_y / height
    ratio_bw = box_width / width
    ratio_bh = box_height / height

    return (ratio_cx, ratio_cy, ratio_bw, ratio_bh)


def yolo2xxyy(yolo):
    """convert yolo to coordinates bbox format
    
    Args:
        yolo (tuple): (ratio-bbox-centre-x, ratio-bbox-centre-y, ratio-bbox-w, ratio-bbox-h)

    Rets:
        box (tuple): (xmin, xmax, ymin, ymax)
    """
    x,y,w,h = yolo
    x1, y1 = x-w/2, y-h/2
    x2, y2 = x+w/2, y+h/2
    return (x1, x2, y1, y2)


def yolo2coco(size, yolo):
    """convert yolo format to coco bbox

    Args:
        size (tuple): (width, height)
        yolo (tuple): (ratio-bbox-centre-x, ratio-bbox-centre-y, ratio-bbox-w, ratio-bbox-h)

    Rets:
        coco: xmin, ymin, boxw, boxh
    """
    width = size[0]
    height = size[1]

    centrex = yolo[0] * width
    centrey = yolo[1] * height
    boxw = yolo[2] * width
    boxh = yolo[3] * height

    halfw = boxw / 2
    halfh = boxh / 2

    xmin = centrex - halfw
    ymin = centrey - halfh

    coco = xmin, ymin, boxw, boxh
    return coco
    


if __name__ == "__main__":
    from PIL import Image
    img_path = "0002ab0af02e4a77.jpg"
    img_path = "000a546e910f0a6b.jpg"
    im = Image.open(img_path)
    w= int(im.size[0])/1000
    h= int(im.size[1])/1000
    
    box = (0, 1, 0.29783395, 1)
    x = bbox2yolo((w,h), box)