import os
from os.path import join
import fnmatch
from typing import List
import win32api

def find_files(filename: str) -> List[str]:

    res = []

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]

    for disc in drives:
        for root, dirs, files in os.walk(disc):
            for found in fnmatch.filter(files, filename):
                res.append(join(root, found))
                        
    return res
