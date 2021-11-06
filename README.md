# google-OID-downloader

download google's open image dataset. official [website](https://storage.googleapis.com/openimages/web/download.html) of OID.

# Steps

1. Download metadata from OID, which include CSV of the class descriptions and bounding boxes of train, validation and test sets.
    - `class-descriptions-boxable.csv`
    - `train-annotations-bbox.csv`
    - `validation-annotations-bbox.csv`
    - `test-annotations-bbox.csv`

```bash
sh download_metadata.sh
```

3. Generate the list of image_ids in a text file using `gen_image_list.py`
4. Download the downloader 

```bash
wget https://raw.githubusercontent.com/openimages/dataset/master/downloader.py
```
5. Download the images 

```bash
python downloader.py download.txt --download_folder=$DOWNLOAD_FOLDER --num_processes=5
```
