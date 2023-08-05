# listevery
![](https://shields.io/badge/pypi-0.1.51-blue) ![](https://shields.io/badge/made%20with-python-lightgray)

__A small program which can list contents of directories and subdirectories, without a depth limit!__ 

## Usage
Running the program in the Python shell is a little strange. You can only get the files and directories of the pip package location. Even though it is a little pointless, run `python -m listevery [folder]` and you will get a structure similar to this.
```
[folder1] [file1.txt, file2.py]
[] [thing.mp4]
```
I'll explain. The first list (folder1) shows the folders in the directory, and the second list (file1.txt, file2.py) shows the files. Then it will look in the first directory of the first list and show any files or folders availible.
It stops when a folder could not be found.

If you want to run this in a Python script, check out the usage.py example script included in the downloads!
This script operates a little differently from running in shell. 

First of all, you need to specify two arguments, `[folder]`, and `[index]`. If you want a specific file run `python usage.py [folder] 0` for example (this may be broken because of random \r\ns in the output). If you want all the files so you can index them in your own way, run `python usage.py [folder] *`. You may get whitespaces and trailing, but you can probably find a way around that. ( ಠ ͜ʖಠ)

## New updates
```
  - Fixed up the Python file to run the module. Gives a less buggy and a usable result!
```

<sub>Have issues? Post them <a href='https://github.com/themysticsavages/listevery/issues/new/choose'>here.</sub>