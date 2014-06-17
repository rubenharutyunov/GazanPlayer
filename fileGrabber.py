#!usr/bin/python
# -*- coding: utf-8 -*-
import glob

def grabb_music_files():
    file_types = ('*.mp3', '*.wav', '*.ogg', '*.flac', '*.m4a')
    files = []
    for file_type in file_types:
        files.extend(glob.glob(file_type))
    return files

def grabb_music_file_types(*types):
    files = []
    for file_type in types:
        files.extend(glob.glob(file_type))
    return files
    
if __name__ == '__main__':    
    print grabb_music_files()        