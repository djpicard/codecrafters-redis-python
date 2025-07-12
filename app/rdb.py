"""rdb file utils"""

import os

MAGIC = "REDIS"
VERSION = "0011"


def exists(folder: str, file: str) -> None:
    """check to see if the rdb file exists and is readable/writable"""
    print("file exists")
    if not os.path.exists(f"{folder}/{file}"):
        save()


def save():
    """save all data to the datastore"""
    print("saved file")


def read():
    """read the rdb file and load the datastore"""
    print("read file")


def update():
    """update the rdb file with the latest data from the datastore"""
    print("updated file")
