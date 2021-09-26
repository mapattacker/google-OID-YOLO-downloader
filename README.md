# google-OID-downloader
download google's open image dataset

# Steps

1. Generate the list of image_ids in a text file using `gen_image_list.py`
2. Download the downloader `wget https://raw.githubusercontent.com/openimages/dataset/master/downloader.py`
3. `python downloader.py download.txt --download_folder=$DOWNLOAD_FOLDER --num_processes=5`
