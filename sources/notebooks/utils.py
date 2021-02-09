"""
Some high-level file operations
"""

import os

def list_images(data_dir, suffix):
    """
    returns a list of file names, contained in a directory, with a name that matches a suffix
    :param data_dir: directory to browse for files
    :param suffix: suffix of the files to search for
    """
    list_im = []
    for root, dirs, files in os.walk(data_dir):
        for name in files:
            if name.endswith(suffix):
                list_im.append(str(root)+"/"+str(name))

    print(len(list_im)," images will be used")
    return list_im

def list_images(data_dir, prefix, suffix):
    """
    returns a list of file names, contained in a directory, with a name that matches a suffix
    :param data_dir: directory to browse for files
    :param prefix: prefix of the files to search for
    :param suffix: suffix of the files to search for
    """
    list_im = []
    for root, dirs, files in os.walk(data_dir):
        for name in files:
            if name.endswith(suffix) and name.startswith(prefix):
                list_im.append(str(root)+"/"+str(name))

    print(len(list_im)," images will be used")
    return list_im
