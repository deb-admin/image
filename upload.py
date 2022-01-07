# -*- coding: utf-8 -*-
# @Time    : 2022/1/7 16:51
# @Author  : XiaoD
# @File    : upload.py
# @Software: PyCharm


import io
import os
import sys
import argparse
from shutil import copy
import hashlib
import locale
from dialog import Dialog

__version__ = "1.0.0"

MOUNT_POINT = "/mnt"
STORAGE_POOL = "/iso"
VM_TEMPLATE = "/vmtemplate"

for dir in [MOUNT_POINT, STORAGE_POOL, VM_TEMPLATE]:
    if not os.path.exists(dir):
        os.makedirs(dir)

def get_args():
    parser = argparse.ArgumentParser(description="Upload iso or vmtemplate to VCT.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {}".format(__version__))
    return parser.parse_args()


def find_file(path):
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

def upload_file(file):
    if file.endswith(".iso"):
        dir = STORAGE_POOL
        copy(file, dir)
    elif file.endswith(".qcow2"):
        dir = VM_TEMPLATE
        copy(file, dir)
    else:
        pass

def hash_sum(path):
    def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE):
        """Yield pieces of data from a file-like object until EOF."""
        while True:
            chunk = file.read()
            if not chunk:
                break
            yield chunk

    def hash_file(path, blocksize=1 << 20):
        h = hashlib.sha256()
        length = 0
        with open(path, 'rb') as f:
            for block in read_chunks(f, size=blocksize):
                length += len(block)
                h.update(block)
        return h, length
    return hash_file(path)

if __name__ == '__main__':
    args = get_args()
    locale.setlocale(locale.LC_ALL, '')
    d = Dialog(dialog="dialog")
    d.set_background_title("Upload and verify large files")
    files = find_file(MOUNT_POINT)
    files_list = []
    for file in files:
        files_list.append((file, "", True))

    code, tags = d.checklist("Please select the file(s) you want to upload:", choices=files_list, title="Select files")

    if code == d.OK:
        for tag in tags:
            file_size = os.path.getsize(tag)
            target_size = 0
            record_size = file_size / 100
            text = "Uploading {} ....".format(tag)
            d.gauge_start(text, percent=0, title="Uploading")
            for i in range(1, 101):
                d.gauge_update(i, update_text=False)
            exit_code = d.gauge_stop()
    else:
        print("You cancelled the dialog!")
