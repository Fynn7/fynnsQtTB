# venv Startup:
```
$ cd C:\Users\Fynn\OneDrive\_Docs\CODING\fynns_ws\PROJECT_NAME
$ python -m venv venv

```

# Start running project:
```
# If you are not in project folder
$ cd C:\Users\Fynn\OneDrive\_Docs\CODING\fynns_ws\PROJECT_NAME

# Activate venv
$ .\venv\Scripts\activate

# install req
$ pip install -r requirements.txt

# deactivate
$ deactivate

```


# design the ui
to open designer, use `$ pyside6-designer` since `C:\Users\Fynn\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts` was already added in the user path

compile xml (.ui) into .py
`pyuic6 input.ui -o output.py`


# building the package

## for testing: use `pyinstaller`
easier

### How to use

```
# 使用--onefile选项将所有文件打包成一个单独的可执行文件：

$ pyinstaller --onefile --distpath=pyinstaller_output src/main.py


```


https://pyinstaller.org/en/stable/operating-mode.html#hiding-the-source-code
### Hiding the Source Code
The bundled app does not include any source code. However, PyInstaller bundles compiled Python scripts ( files). These could in principle be decompiled to reveal the logic of your code..pyc

If you want to hide your source code more thoroughly, one possible option is to compile some of your modules with Cython. Using Cython you can convert Python modules into C and compile the C to machine language. PyInstaller can follow import statements that refer to Cython C object modules and bundle them.

## for future better performance + smaller size of the package
instead of using `pyinstaller`, use `pyoxidizer`

NOTE: DO NOT INSTALL THIS INSIDE VENV
$ pip install pyoxidizer