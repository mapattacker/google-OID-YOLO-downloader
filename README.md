# google-OID-downloader

Download Google's open image dataset v6 (OID), with corresponding YOLO annotation files.

Official [website](https://storage.googleapis.com/openimages/web/download.html).

# TL;DR

```bash
cd oid-yolo
pip install -r requirements.txt
```

Add [class name](https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv) and other parameters in `config.yaml`.

```bash
python main.py
```