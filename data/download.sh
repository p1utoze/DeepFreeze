#!/bin/bash
# This script downloads L1B echogram images (along with echo picks and map) provided in JPEG format
# The data is from the parent Radar type: Radar Depth Sounder (RDS)
# RDS data is provided here: https://data.cresis.ku.edu/data/rds/
# THe Wiki Guide for RDS is here: https://gitlab.com/openpolarradar/opr/-/wikis/Radar-Depth-Sounder

GREEN='\033[0;32m'
NC='\033[0m'

mapfile -t seasons < rds_seasons.txt 

FOLDER_TYPE="images"                  # Change this according to the cresis folder type you want to download
DATA_TYPE="jpg"                       # This is the file format extension type you want

for i in ${seasons[@]}; do         # Optionally you  can give a slice range for multi process extraction using multiple terminals like this: ${seasons[@]:I:N}
  url="https://data.cresis.ku.edu/data/rds/$i/$FOLDER_TYPE/"
  wget -r -np --accept  $url
  echo -e "${GREEN}Extraction for $i is completed! ${NC}" | tee -a completed_seasons.log
done 
