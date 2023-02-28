#!/bin/bash

FONT=/usr/share/fonts/urw-base35/Z003-MediumItalic.otf
OUTPUT_DIR=$1
mkdir -p $OUTPUT_DIR

while IFS='$\n' read -r line; do
  img_name=$(echo $line | awk '{print $1}')
  out_name=$OUTPUT_DIR/$(basename $img_name)
  label=$(echo $line | awk '{ $1=""; print substr($0,2) }')
  echo "Processing: $img_name, label: $label"
  python img_label.py $img_name $out_name "$label" $FONT
done
