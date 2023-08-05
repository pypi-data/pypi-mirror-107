# listevery

[![](https://shields.io/badge/pypi-0.1.6-blue?style=flat&logo=pypi)](https://pypi.org/project/listevery)
[![](https://shields.io/badge/made%20with-python-lightgray?style=flat&logo=python)](https://python.org/downloads)

__A Python package which can list contents of directories and subdirectories, without a depth limit!__ 

<sub>(yes, I know there's os.walk i don't care)</sub>

## Usage
Running the program in the Python shell is a little strange. You can only get the files and directories of the pip package location. Even though it is a little pointless, run `python -m listevery [folder]` and you will get a structure similar to this.
```
[folder1] [file1.txt, file2.py]
[] [thing.mp4]
```
I'll explain. The first list (folder1) shows the folders in the directory, and the second list (file1.txt, file2.py) shows the files. Then it will look in the first directory of the first list and show any files or folders availible.
It stops when a folder could not be found.

If you want to run this in a Python script, check out the import.py.test usage script in the downloads. This script is a guide to help you run the package by import.

Luckily, running listevery in a Python script is so much better. For starters, you can actually get the contents of directories besides the pip package, and the result is given in a lovely and usable list. Ha take that, tree command!
Speaking of lists, listevery can index specific things for you.

Here's a few different usages:

#

*Get all the files and directories:*
```
from listeveryu import listevery
listevery('.', '*')
```
*Get specific items:*
```
from listevery import listevery
listevery('.', int)
```

#

Not too hard right?
You may get whitespaces and trailing, but you can probably find a way around that. (ಠuಠ)

## New updates
```
  - Fixed up the Python file to run the module. Gives a less buggy and a usable result!
```

### Compatibility
```
Will work ✔:
  - Windows 7 or above
  - GNU/Linux
  - MacOS

Does not work properly ⚠:
  - Replit
  - Heroku

Will not work ❌:
  - Online compilers (e.g: TutorialsPoint, OnlineGDB)
```

<sub>Have issues? Post them <a href='https://github.com/themysticsavages/listevery/issues/new/choose'>here.</sub>
