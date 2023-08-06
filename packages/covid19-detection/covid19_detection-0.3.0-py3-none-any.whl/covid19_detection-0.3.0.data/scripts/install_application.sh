#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <models_path>"
  exit 1
fi

# install packages
conda create --name covid19-detection tensorflow==2.3.0 -y
conda activate covid19-detection
pip install covid19-detection
pip install gdown

# download models
models_path=$1
cd "$models_path"
models_path=$(pwd)
bash "$(dirname $0)"/download_models.sh "$models_path"

# download icon
icons_path=~/.local/share/icons
cd $icons_path
icon_path=$(pwd)
icon_path="$icon_path/covid19-detector.jpeg"
wget -q https://raw.githubusercontent.com/franco-ruggeri/dd2424-covid19-detection/master/covid19/ui/qt_designer/images/logo.jpeg -O "$icon_path"

# create desktop entry
cd ~/.local/share/applications
filename="covid19-detector.desktop"
echo "[Desktop Entry]" > $filename
echo "Version=0.3.0" >> $filename
echo "Type=Application" >> $filename
echo "Terminal=false" >> $filename
echo "Exec=bash -i \"conda activate covid19-detection && covid19-detector $models_path\"" >> $filename
echo "Name=COVID-19 Detector" >> $filename
echo "Icon=$icon_path" >> $filename
