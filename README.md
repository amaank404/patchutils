# patchutils

patchutils provide utilities for making patches from directories and applying patches to directories.
If you like the library and use it in your project, please consider giving us a star :star:

Made with :heart: by [Contributers](https://github.com/xcodz-dot/patchutils/blob/master/AUTHORS.md/)

## Usage

### Installation

from pip:

```bash
pip install patchutils -U
```

from latest repo

```bash
git clone xcodz-dot/patchutils
pip install poetry
poetry install
```

**do not use poetry until you know how it works**


### API Documentation
You can check the steps to build documentation by doing this:

```python
>>> import patchutils
>>> help(patchutils)
```

For your convinience all documentation is pre-built under the docs directory.

### Concept

There are three things to be noted:
* directory information
* patch
* update files

#### Directory Information

Directory Information is a simple dictionary object containing 3 fields:

* ##### `files`
  Files is a list that contain relative paths for all the files for the
  provided directory.

* ##### `directories`
  Directories is a list that contain relative paths for all the subdirectories
  for the provided directory.

* ##### `hash`
  Hash is a dictionary with key as file names and values as `SHA-256` checksums
  for the respective files.

Here is a Sample Directory Information:
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

#### Patch

Patch is a dictionary that tells what changes have been made in comparision
to two different Directory Informations. It consists of the following feilds:

* ##### `files_added`
  List of Files added in comparision to the old directory information

* ##### `files_removed`
  List of Files removed in comparision to the old directory information

* ##### `files_modified`
  List of Files modified in comparision to the old directory information

* ##### `directories_added`
  List of directories added including empty directories

* ##### `directories_removed`
  List of directories removed including all their content within them

Here is an example patch:

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

#### Update Files

Update files are simple uncompressed zip archives that are made using
patch. Here is a typical workflow of a server and a client requesting
updates:

* Clients gives their version number to the server.
* Server checks the version number and loads up stored directory information for that version.
* Server creates a patch using the latest directory information and that specific version directory
  information.
* Server creates an uncompressed update file and starts streaming it to the client **OR** alternatively
  server sends the patch in json format and client starts querying the server for different files listed
  in the patch and applies the patch to required positions.
* If the client recieved the update file instead of patch information then the client applies the update
  file to the required positions.

Alternatively to above if their is no version specifications then the workflow might
look like this:

* Client generates directory information from local filesystem and sends it to the server
* Server creates a patch using client provided directory information and latest server
  directory information.
* *And from this point on the process of updating is same as in above example*

## Contributers

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://xcodz-dot.github.io/"><img src="https://avatars.githubusercontent.com/u/71920621?v=4?s=100" width="100px;" alt=""/><br /><sub><b>xcodz-dot</b></sub></a><br /><a href="https://github.com/xcodz-dot/patchutils/commits?author=xcodz-dot" title="Code">💻</a> <a href="https://github.com/xcodz-dot/patchutils/commits?author=xcodz-dot" title="Documentation">📖</a> <a href="#infra-xcodz-dot" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/xcodz-dot/patchutils/commits?author=xcodz-dot" title="Tests">⚠️</a> <a href="#maintenance-xcodz-dot" title="Maintenance">🚧</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
