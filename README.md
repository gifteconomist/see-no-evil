# See no evil


## Install all Project Requirments

1. Open up your terminal application.
2. If you are using a mac, you must install [Homebrew](https://brew.sh/), which is a package manger for macOS or Linux. To install run the following in your terminal.
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
To test that the installation worked - or to test that Homebrew has already been installed on your machine, run:
```
brew --version
```
You should see a print out of the current version of Homebrew installed on your machiene.

3. Using the Homebrew command `brew`, install [ImageMagick](https://imagemagick.org/index.php), a library this program uses to work with images. In your terminal run:
```
brew install imagemagick
```
4. Use Homebrew to install Python3. Python 3.6+ is required to run this project. In your terminal, type:
```
brew install python
```
5. See if you have [pip](https://pip.pypa.io/en/stable/) installed, which is the package manger for Python. Try running "`pip -h`" or "`pip3 -h`".

If you see a list of commands, pip is installed. If you get an error like `Command not found`, try runnning:
```
python get-pip.py
```
6. Install [virtualenv](https://packaging.python.org/key_projects/#virtualenv), which is a tool that allows you to manage Python packages for different projects. Run: 
```
python3 -m pip install --user virtualenv
```
7. Download the latest version of the code from the Github repository using the command:
```
git clone https://github.com/gifteconomist/see-no-evil.git
```
***Note: You might need to sign into Github via the terminal in order to access this repo. Follow the instructions [here](https://docs.github.com/en/free-pro-team@latest/github/using-git/setting-your-username-in-git).***

7. Once you've downloaded the github repository, navigate into the project directory. Once you're in the project directory, you're ready to install the project requirements. Run: 
```
cd see-no-evil
```
7. Create a Python 3.6+ virtual enviroment inside a hidden directory `.venv` using the `virtualenv` command. Replace the below prompt with your computer's path to your Python Installation:
```
virtualenv -p <Path To Python 3.6+ Installation Here> .venv
```
If you cannot locate the path to your Python 3.6+ Installation, try running:
```
virtualenv -p /Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6 .venv
```
8. Initiate the virtual enviroment that you will run the program inside:
```
source .venv/bin/activate
```
9. Install the python packages used in the project: requirements:
```
pip install -r requirements.txt
```
At this point the program should be ready to run!

## Run the Script

1. Make sure your terminal prompt is in the `see-no-evil` project directoty. To check run: 
```
pwd
```
If you are not in the directory navigate to it using the `cd` UNIX command.
2. Start your virtual environment, if you haven't already:
```
source .venv/bin/activate
```
2. Update the project configurations using the `parameters.json` file. To view and edit the file from a finder window, run: 
```
open .
```
This will open a finder window in the directory your terminal prompt is currently in.
3. Run the script:
```
python run.py
```


## Project Settings
In order for the script to run correctly, the text needs to be formatted as a PDF and be located at the root of the project directory. 

The drawing images need to be formatted as PNGs and placed in a directory that also lives at project root.

The following features of the project are configurable:
 - The opacity of the drawing images that overlay on the text
 - The text pdf source
 - The drawing images
 - The page height of the final pdf
 - The page width of the final pdf
 - The resolution of the final pdf
 - Whether the beginning of the text with images should begin on the right-hand or left-hand page.

The configurations for the project are exposed in the `parameter.json` file located in the project directory's root.

#### Changing the Opacity
Change the opacity of drawings by updating the `opacity` parameter exposed in the `parameter.json` file.

#### Changing or Updating the Image Drawings
The drawings that will appear overlayed n the final document are sourced from the directory specified by the `image_dir` parameter exposed in the `parameter.json` file.

The script will look for a directory named after the string value provided here, at the root of your project's directory.

#### Changing the Source Text
Change the source text by swapping out the source pdf located at the root of your project's directory.



