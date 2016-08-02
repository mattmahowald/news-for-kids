# News For Kids Parsing Script

Note: Documentation written for Mac computers

## Overview

There are three major steps to setting up your environment to run this script:

1. Download the script
2. Assure you have Python installed on your machine. 
3. Install the dependent libraries from the Python Package Index

Then you will be ready to run the script.

### 1. Download Script

**Option 1: Store the script on your computer**

Click this link: https://github.com/mattmahowald/news-for-kids/archive/master.zip to start the 
download. Click on the download once it has finished to unzip it. In finder, move the folder
to wherever you want it stored on your computer. Then we need to navigate to 
this folder in your terminal.

If you already know how to get there using the `cd` command, use that. 

Otherwise, there is a useful shortcut to open a folder in System Preferences.

1. Open System Preferences
2. Navigate to Keyboard -> Shortcuts -> Services
3. Under *Files and Folders* enable New Terminal at Folder

Now that we have this shortcut, go back into finder and right click on the folder, then click
New Terminal at Folder, which will open up a terminal session in the correct directory.

If you cannot get that to work, open terminal which you can find if you open up finder, 
navigate to Applications then the Utilities folder, or using the cmd + space global search).

Once open you will be in your home folder. Type in `ls` to see what folders you can move to
from there. Use the `cd` command to change folders. Navigate this way until you are in the
`news-for-kids` folder.

**Option 2: Mount Google Drive on your computer**

@TODO write this

### 2. Python
All Mac and Linux-based Operating Systems come installed with python. You can then type into 
the command prompt, and expect to see a response somewhat like this.

```sh
$ python --version
Python 2.7.X
```

Note: In the above format, a line starting with a `$` denotes the prompt from the command line, 
so you do not actually need to type the symbol, only, in this example, `python --version`. 
The following line is the computer's response—in this case the version of python. You will 
need Python version 2.7 or later. If you do not have that, download the latest update from
www.python.org/downloads. You can install either Python 2 or Python 3. I recommend Python 2 if
you only plan to use Python for this script.

As soon as your terminal confirms you have the correct version, you are ready to continue.

### 3. Packages
In order to communicate with the web, there are some third-party modules that are necessary
to install. The first is the installer itself, called `pip` for Pip Installs Packages. To do
this, open the terminal, and navigate to the location of your download, as explained in part
1. Once there, type 

```sh
$ sudo python get-pip.py
Password: <your computer password here>
```

```sh
$ pip install -r requirements.txt
Collecting DateTime==4.1.1 (from -r requirements.txt (line 1))
...
Successfully installed DateTime-4.1.1 pytz-2016.6.1 requests-2.10.0 zope.interface-4.2.0
```

The details of the output are not important, as long as you don't see any indications
it didn't work, such as `error` or `failed` somewhere in the output.

If it worked, great! You're done and ready to run the script. If not, feel free to email 
me at mmahowald@lightsailed.com.

## Running the script

This portion is extremely straightforward. Fire up a terminal and navigate to the folder
with the script located in it. Then type

```sh
$ python news-4-kids.py
Welcome to the News-o-Matic Feed Parser™...
```

The script will create a folder labeled with the date with all the .html files for
the articles inside.

## Fixing errors

There are many possible errors you could run into, which I've tried to summarize here:

1. The url is broken. 
