__author__ = 'eric'

import os
import sys


def open_file(file_path, mode='r'):
    '''
    Open file in various type

    @param file_path:
    @param mode: r, rt, rb, w, wt, wb
    @return: file handle
    '''
    if mode == "r" or mode == "rt":
        mode = "rb"
    elif mode == "w" or mode == "wt":
        mode = "wb"

    if file_path[-3:] == ".gz":
        import gzip

        return gzip.open(file_path, mode)
    elif file_path[-4:] == ".bz2":
        import bz2

        return bz2.open(file_path, mode)
    else:
        return open(file_path, mode)


def load_pickle(file_path):
    '''
    load pickle file
    @param file_handle:
    @return: data
    '''
    if file_path[-3:] == ".gz" or file_path[-4:] == ".bz2" or file_path[-4:] == ".pkl":
        file_handle = open_file(file_path)
    else:
        print >> sys.stderr, "WARNING: unknown pickle file type."

    import cPickle

    data = cPickle.load(file_handle)
    file_handle.close()
    return data


def load_yaml(file_path):
    '''
    load yaml file
    @param file_handle:
    @return: data
    '''
    if file_path[-5:] == ".yaml":
        file_handle = open_file(file_path)
    else:
        print >> sys.stderr, "WARNING: unknown pickle file type."

    import yaml

    data = yaml.load(file_handle)
    file_handle.close()
    return data


def extractZip(file_path):
    '''
    unzip to the current folder
    @param file_path:
    @return:
    '''
    from zipfile import ZipFile as zip

    zip(file_path).extractall()


def recur_get_filelist(dir, suffix='*', shuffle=False):
    '''
    recursively get (particular) file path

    @param dir: root dir
    @param suffix: particular type of file to search
    @param shuffle: shuffle resulting list
    @return: a file list with full path
    '''

    all = []
    assert os.path.isdir(dir)
    for root, dirs, files in os.walk(dir):
        #sys.stderr.write("Walking %s...\n" % root)
        for f in files:
            if suffix == '*':
                all.append(os.path.join(root, f))
            else:
                if f.lower().endswith('.' + suffix.lower()):
                    all.append(os.path.join(root, f))
    if shuffle:
        import random

        random.shuffle(all)
    return all


def create_dir(dir):
    """
    Create dir if it does not exist (including all parents).
    Do nothing if it does.
    """
    if not os.path.exists(dir):
        sys.stderr.write("Creating directory: %s\n" % dir)
        os.makedirs(dir)
    assert os.path.isdir(dir)
