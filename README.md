# See no evil

## Requirements
Python 3.6+ is required to run this project:
https://www.python.org/downloads/

ImageMagick is required to run this project:
```
brew install freetype imagemagick
```

## Installation

- Create a Python 3.6+ virtual enviroment inside a hidden directory `.venv` using the `virtualenv` command. Replace prompt with your computer's path to your Python Installation:
```
virtualenv -p <Path To Python 3.6+ Installation Here> .venv
```
- Run virtual enviroment:
```
source .venv/bin/activate
```
- Install python requirements:
```
pip install -r requirements.txt
```

## Project Setup
In order for the script to run correctly, the text needs to be formatted as a PDF and be located at the root of the project directory. 

The drawing images need to be formatted as PNGs and placed in a directory that also lives at project root.

The following features of the project are configurable:
 - The opacity of the drawing images that overlay on the text
 - The text pdf source
 - The drawing images

The configurations for the project are exposed in the `parameter.json` file located in the project directory's root.

### Changing the Opacity
Change the opacity of drawings by updating the `opacity` parameter exposed in the `parameter.json` file.

### Changing or Updating the Image Drawings
The drawings that will appear overlayed n the final document are sourced from the directory specified by the `image_dir` parameter exposed in the `parameter.json` file.

The script will look for a directory named after the string value provided here, at the root of your project's directory.

### Changing the Source Text
Change the source text by swapping out the source pdf located at the root of your project's directory.


## Run the Script
TLDR: 
```
python run.py
```

1. Start your virtual environment:
```
source .venv/bin/activate
```
2. Update the project configurations using the `parameters.json` file
3. Run the script:
```
python run.py
```
