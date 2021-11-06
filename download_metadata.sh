mkdir metadata
cd metadata

# download train, val, test bboxes
wget https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv
wget https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv

# download class descriptions
wget https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv