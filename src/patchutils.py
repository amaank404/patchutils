"""
Use pdoc to generate documentation:

```bash
pip install pdoc3
pdoc patchutils -o docs --html
cd docs
python -m http.server
```

now go to `http://localhost:8000/patchutils.html` to view api documentation.
To understand concept and what is this library all about please visit project
homepage and read the `README.md` at [this link](https://github.com/xcodz-dot/patchutils).
"""

import hashlib
import os
import zipfile
import json
import copy
import shutil


def create_info_from_directory(dir: str) -> dict:
    """
    Creates and returns a dictionary of all files, directories with sha-256 hashes for all files
    calculated for all files.

    Sample return value:
    
    ```json
    {
        "files": [
            "my_file_1.txt",
            "folder1/myfile2.txt",
            "folder2/another_folder/myfile3.txt"
        ],
        "directories": [
            "folder1",
            "folder2",
            "folder2/another_folder",
            "empty_folder"
        ],
        "hash": {
            "my_file_1.txt": "blablablablbalbalblblablblblblblblbl some sha hash blahblabla",
            "folder1/myfile2.txt": "blablablablablablablablablabla hash is in a hexdigest format",
            "folder2/another_folder/myfile3.txt": "blablablablbalbalblablg7ty913griubkeda"
        }
    }
    ```
    """
    dir_info = {"files": [], "directories": [], "hash": {}}
    dir = os.path.abspath(os.path.expanduser(dir))
    for root, directories, files in os.walk(dir):
        root = root[len(dir):]
        for x in directories:
            dir_info['directories'].append(os.path.join(root, x).replace("\\", "/").strip('/'))
        for x in files:
            dir_info['files'].append(os.path.join(root, x).replace("\\", "/").strip('/'))
            filename = dir+"/"+dir_info['files'][-1]
            filehash = hashlib.sha256()
            with open(filename, "rb") as file:
                while True:
                    buf = file.read(100000)
                    if len(buf) == 0:
                        break
                    filehash.update(buf)
            dir_info['hash'][dir_info['files'][-1]] = filehash.hexdigest()
    return dir_info



def create_patch_from_info(info1: dict, info2: dict) -> dict:
    """
    Takes two directorey information dictionaries created using `create_info_from_directory`
    and returns a patch that contains information about `files_added`, `files_removed`, `files_modified`,
    `directories_added`, `directories_removed` and `hash`.

    Sample return value:

    ```json
    {
        "files_added": ["new_file.txt"],
        "files_removed": ["i_hate_python.txt"],
        "files_modified": ["why_i_like_python.txt"],
        "directories_added": ["Temp"],
        "directories_removed": [".Temp"],
        "hash": {
            "new_file.txt": "blablablablbalbalbalbblablbablablbalbblabla",
            "why_i_like_python.txt": "blablablablablablablablablalbalgialbdblablbla"
        }
    }
    ```
    """
    difference_of_files = list(set(info1['files']).difference(set(info2['files'])))
    difference_of_directories = list(set(info1['directories']).difference(set(info2['directories'])))
    patch_info = {
        "files_added": [],
        "files_removed": [],
        "files_modified": [],
        "directories_added": [],
        "directories_removed": [],
        "hash": {}
    }
    for name in difference_of_files:
        if name in info1['files']:
            patch_info["files_removed"].append(name)
        else:
            patch_info["files_added"].append(name)
            patch_info['hash'][name] = info2['hash'][name]
            
    for name in difference_of_directories:
        if name in info1["directories"]:
            patch_info["directories_removed"].append(name)
        else:
            patch_info["directories_added"].append(name)
    
    files_in_both = set(info1["files"]).intersection(set(info2["files"]))
    
    for x in files_in_both:
        if info1["hash"][x] != info2["hash"][x]:
            patch_info["files_modified"].append(x)
            patch_info["hash"][x] = info2["hash"][x]
    
    return patch_info


def merge_patches(patch1, patch2):
    """
    Merge two continous patches into 1 single patch by using common logic.
    """
    patch_info = copy.deepcopy(patch1)
    for x in patch2["files_added"]:
        if x in patch_info['files_removed']:
            patch_info['files_modified'].append(x)
            patch_info['files_removed'].remove(x)
        else:
            patch_info['files_added'].append(x)
        patch_info['hash'][x] = patch2['hash'][x]
    for x in patch2["files_removed"]:
        if x in patch_info['files_added']:
            patch_info['files_added'].remove(x)
            del patch_info['hash'][x]
        elif x in patch_info['files_modified']:
            patch_info['files_modified'].remove(x)
            del patch_info['hash'][x]
            patch_info['files_removed'].append(x)
        else:
            patch_info['files_removed'].append(x)
    for x in patch2["files_modified"]:
        if x in patch_info['files_added']:
            patch_info['hash'][x] = patch2['hash'][x]
        else:
            if x not in patch_info['files_modified']:
                patch_info['files_modified'].append(x)
            patch_info['hash'][x] = patch2['hash'][x]
    patch_info['files_added'] = list(set(patch_info['files_added']))
    patch_info['files_removed'] = list(set(patch_info['files_removed']))
    patch_info['files_modified'] = list(set(patch_info['files_modified']))
    patch_info['directories_added'] = list(set(patch_info['directories_added']))
    patch_info['directories_removed'] = list(set(patch_info['directories_removed']))
    return patch_info


def apply_patch_on_info(patch, info):
    """
    Apply a patch on provided directory information that is generated by 
    `create_info_from_directory`, This does not apply patch to real hard drive,
    but only applies to directory information dictionary.
    """
    for x in patch['files_added']:
        if x not in info['files']:
            info['files'].append(x)
    for x in patch['files_removed']:
        if x in info['files']:
            info['files'].remove(x)
    hash2 = copy.deepcopy(info['hash'])
    info['hash'] = {}
    for k, v in ({**hash2, **patch['hash']}).items():
        if k in info['files']:
            info['hash'][k] = v


def create_update_file_from_patch(patch, dir: str, file: str):
    """
    Create a update file, that is basically a zipfile using the `patch` provided.
    `dir` is supposed to be the name of the real hard disk directory from which
    the patch files are to be taken. `file` is supposed to be the name of the zipfile
    to write to (Example: `patch.zip`, `update_version3.2.9.patch`)
    """
    file = zipfile.ZipFile(file, mode="w")
    file.writestr("patch.json", json.dumps(patch))
    for x in patch["files_added"]+patch["files_modified"]:
        file.write(os.path.abspath(os.path.join(dir, x)), f"contents/{x}")


def apply_update_file_to_directory(file: str, dir: str):
    """
    Apply a update file to directory.

    See also: `create_update_file_from_patch`

    .. warning::
        This function applies changes to real directory and have not yet been
        thoroughly tested. Although the implementation is complete and functional, 
        some special edge cases are there that might cause problems.
    """
    file = zipfile.ZipFile(file, "r")
    patch = json.loads(file.read("patch.json"))
    for x in patch['directories_added']:
        os.makedirs(os.path.join(dir, x), exist_ok=True)
    for x in patch['directories_removed']:
        shutil.rmtree(os.path.join(dir, x))
    for x in patch['files_added']+patch['files_modified']:
        with open(os.path.join(dir, x), "wb") as fpw:
            with file.open("contents/"+x) as fpr:
                while True:
                    buf = fpr.read(100000)
                    if len(buf) == 0:
                        break
                    fpw.write(buf)
    for x in patch['files_removed']:
        os.remove(os.path.join(dir, x))
