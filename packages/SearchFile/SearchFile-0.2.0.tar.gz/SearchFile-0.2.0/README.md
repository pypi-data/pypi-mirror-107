# SearchFile
#### Table of contents
1. [Installation](#Installation)
2. [Description](#Description)
3. [Using](#Using)
4. [Code](#Code)
## Installation
Installation using a terminal:

```pip install SearchFile```
## Description
This library is designed to search for files by a given path.
## Using
```import SearchFile```

or

```from SearchFile import search```

The argument of the `search` function is the path passed as a string.
#### For Windows
Also, the directory separator should be written in the form `\\`, so as not to form control characters (\n, \t, \r, etc.). Examples:
```
search("C:\\Users")
search("D:\\Downloads\\test.txt")
search("D:\\Git\\cmd")
```
#### Linux
The directory separator should be used `/`. Examples:
```
search("/home/artem/desktop/")
search("/home/artem/tmp/file1")
search("/home/artem/desktop/tmp/")
```
#### Mac OS
The directory separator should be used `/`. Examples:
```
search("/Library/Desktop Pictures")
search("/Library/Desktop Pictures/pictures1.jpg")
search("/Library/Desktop Pictures/gallery")
```
## Code
```
from os import path, listdir


def search(tpath):
    if path.isdir(tpath):
        try:
            for dirs in listdir(tpath):
                if path.isdir(path.join(tpath, dirs)):
                    search(path.join(tpath, dirs))
                else:
                    print("\n", path.basename(path.join(tpath, dirs)))
        except PermissionError:
            print("\n""Отказано в доступе - " + tpath)
    else:
        if path.isfile(tpath):
            print(path.basename(tpath))
        else:
            print("Неверно указан путь!")
```