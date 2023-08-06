# dnpak.py

A python package to manipulate Dragon Nest pak file.

Based on data definitions from [vincentzhang96/DragonNestFileFormats](http://vincentzhang96.github.io/DragonNestFileFormats/files/pak)

## Installation
```shell
$ pip install dnpak.py
```

## Getting Started

```python
import dnpak

pak = dnpak.EtFileSystem.write("filename.pak")
pak.add_file("path/to/file", "/location/in/pak")
pak.close_file_system()  # Make sure to close file after adding files


pak = dnpak.EtFileSystem.read("filename.pak")
pak.extract()


```