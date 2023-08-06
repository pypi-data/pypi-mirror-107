import os
from os.path import join, isdir, isfile, splitext
import fnmatch
from posixpath import basename
from typing import List
import win32api


def my_walk(path: str) -> List[str]:
    objects = os.listdir(path)
    files = [join(path, file) for file in objects if isfile(join(path, file))]

    for dir in [file for file in objects if isdir(join(path, file))]:
        files = [*files, *my_walk(join(path, dir))]

    return files


def find_files(filename: str) -> List[str]:

    res = []

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

    for disc in drives:
        for root, dirs, files in my_walk(disc):
            for found in fnmatch.filter(files, filename):
                res.append(join(root, found))
                        
    return res


def find_files_dir(dir:str, filename: str) -> List[str]:

    res = []
    
    for file in my_walk(dir):
        if os.path.basename(file) == filename:
            res.append(file)

    return res
