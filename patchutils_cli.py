"""
Patchutils CLI
"""

import sys
import argparse
import patchutils
import json


parser_description = """
Official CLI for patchutils. It provides basic functionalities for using patchutils from the comfort of your
command line. You can create patches, directory_informations, update_files all from this single CLI. It also
supports doing the mensioned operations for GitHub Repositories, both private and public.
""".replace("\n", " ").strip()


def main(args=None):
    """
    perform the command-line operations using the given arguments.
    `args` default to `None` which converts to arguments given to
    the proggram through real command line
    """
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=parser_description)
    commands = parser.add_subparsers(dest="command_")

    local = commands.add_parser("local", help="Commands related to local filesystem actions")
    local_actions = local.add_subparsers(dest="action_")
    
    create_patch = local_actions.add_parser("create-patch", help="Create a patch from directory information")
    create_patch.add_argument("dir_info_file_old", help="Old directory information file")
    create_patch_directory_info = create_patch.add_mutually_exclusive_group()
    create_patch_directory_info.add_argument("dir_info_file_new", nargs="?", help="File containing directory information for the new file")
    create_patch_directory_info.add_argument("-c", "--create-directory-information", help="Create and use directory information using given directory")
    create_patch.add_argument("-o", "--output", help="Name of output file that contains patch", required=True)

    merge_patch = local_actions.add_parser("merge-patch", help="Merge two different patches")
    merge_patch.add_argument("patch1", help="File containing old patch")
    merge_patch.add_argument("patch2", help="File containing new patch")
    merge_patch.add_argument("-o", "--output", help="Name of output file that will contain patch", required=True)

    create_directory_information = local_actions.add_parser("create-dirinfo", help="Create directory information file using the given directory")
    create_directory_information.add_argument("directory", help="Directory to use for the operation", nargs="?", default=".")
    create_directory_information.add_argument("-o", "--output", help="Name of the output file that contains directory information", required=True)

    args = parser.parse_args(args)

    if args.command_ == "local":
        if args.action_ == "create-patch":
            with open(args.dir_info_file_old) as file:
                directory_information_old = json.load(file)
            if args.dir_info_file_new:
                with open(args.dir_info_file_new) as file:
                    dirctory_information_new = json.load(file)
            else:
                dirctory_information_new = patchutils.create_info_from_directory(args.create_directory_information)
            patch = patchutils.create_patch_from_info(directory_information_old, dirctory_information_new)
            with open(args.output, "w") as file:
                json.dump(patch, file)
        elif args.action_ == "merge-patch":
            with open(args.patch1) as file, open(args.patch2) as file2:
                patch1 = json.load(file)
                patch2 = json.load(file2)
            patch3 = patchutils.merge_patches(patch1, patch2)
            with open(args.output, "w") as file:
                json.dump(patch3, file)
        elif args.action_ == "create-dirinfo":
            dir_info = patchutils.create_info_from_directory(args.directory)
            with open(args.output, "w") as file:
                json.dump(dir_info, file)


if __name__ == "__main__":
    main()
