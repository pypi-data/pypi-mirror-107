
# Path File 1.0.4<a id="home"></a>
___
# Table of contents
1. [Installation](#Installation)
2. [How to use](#manual)
3. [Example](#Example)

# Installation<a id="Installation"></a>
___
pip install PathFile
# How to use<a id="manual"></a>
___
1. Add to your code: from PathFile.PathFile import find_files
2. In order to insert find path to file use find_files('filename.exe/txt/jpg/doc/...')  

# Example<a id="Example"></a>

```python
from PathFile.PathFile import find_files

a = find_files('cat.jpeg')
```
____
# Notes
For the library to work properly, must specify the file extension

[UP](#home)