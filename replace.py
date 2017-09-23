#!/usr/bin/python

import os
import codecs
import sys

def rename(substring, new, path):
    """Rename file or directory containing substring
    
    Inputs:
        - substring: file or directory name substring
        - new: string to replace
        - top: top directory
    
    Returns:
        - newpath: renamed file or directory name
        - count: number of substring occurences
    """
    k = path.rfind('/')
    count = path[k:].count(substring)
    newpath = path[:k] + path[k:].replace(substring, new)
    os.rename(path, newpath)
    return (newpath, count)

def replace(substring, new, filename):
    """Replace substrings in a file with new strings
    
    Inputs:
        - substring: file or directory name substring
        - new: string to replace
        - filename: file name to search substrings
        
    Returns:
        - count: number of substring occurences
    """
    with codecs.open(filename, 'r', 'utf-8') as file:
        data = file.read()
        count = data.count(substring)
        data = data.replace(substring, new)
    with codecs.open(filename, 'w', 'utf-8') as file:
        file.write(data)
    return count
            
def renames(substring, new, top, verbal=False, ignore_hidden_files=True):
    """Rename files and directories containing substring
    
    Inputs:
        - substring: directory name substring
        - new: string to replace substring
        - top: top directory for search directories recursively
        - verbal: prints intermediate results
    """
    num_string_changes = 0
    num_path_changes = 0
    for dirname, dirnames, filenames in os.walk(top, topdown=False):
        for filename in filenames:
            if ignore_hidden_files:
                if filename.startswith('.'):
                    continue
            path = os.path.join(dirname, filename)
            (newpath, count) = rename(substring, new, path)
            num_path_changes += count
            count = replace(substring, new, newpath)
            num_string_changes += count
        (newpath, count) = rename(substring, new, dirname)
        num_path_changes += count
    if verbal: 
        print('renamed files/dirs: %d' % num_path_changes)
        print('changed substrings: %d' % num_string_changes)

if __name__ == "__main__":
    renames(sys.argv[1], sys.argv[2], sys.argv[3], verbal=True)