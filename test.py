import re
import os
import pathlib
from collections.abc import Callable
from src.block_type import BlockType

def iter_dir(path: str):
    p = pathlib.Path(path)
    for child in p.iterdir():
        print(child)
        if child.is_dir():
            iter_dir(child)

#iter_dir("content")
p = pathlib.Path("content")
for root, dirs, files in p.walk():
    for file in files:
        path = os.path.join(root, file)
        print(path)


print("---")
folder_path = pathlib.Path("content")
test = str(folder_path)
print(f"type={type(test)} ; {test}")
print(folder_path)
for child in folder_path.iterdir():
    tmp = str(child)
    dest = tmp.replace(folder_path, "public")
    print(f"{tmp} is of type {type(tmp)}")
    print(dest)
    if child.is_file():
        continue