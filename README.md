# google-OID-downloader
download google's open image dataset

# Steps

1. Download `class-descriptions-boxable.csv`, `test-annotations-bbox.csv`, `train-annotations-bbox.csv`, `validation-annotations-bbox.csv`
2. Generate the list of image_ids in a text file using `gen_image_list.py`
3. Download the downloader `wget https://raw.githubusercontent.com/openimages/dataset/master/downloader.py`
4. `python downloader.py download.txt --download_folder=$DOWNLOAD_FOLDER --num_processes=5`
