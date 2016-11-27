#!/bin/python
"""
push_code.py
Michael George
California Polytechnic State University

A program to push all of the files in the src directory to the LoPy board via the FTP server.

Requires that the LoPy be connected to the same network, and the ip address of the LoPy to be
known.
"""

from ftplib import FTP
import argparse
from io import StringIO
import sys
import os

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def main():
    parser = argparse.ArgumentParser(description="Push directories code via FTP to the LoPy board.",
                                     prog="push_code.py")
    parser.add_argument("ip_address", help="IP address of the LoPy")
    parser.add_argument("--dir", default="./src",
                        help="Directory to transfer files from. ")
    parser.add_argument("-b", action="store_const", const=True, default=False,
                        help="use -b to overwrite boot.py with boot.py in directory")
    parser.add_argument("--exclude", nargs="+",
                        help="File extensions to exclude (e.g. txt for .txt) in transfer."
                        " Can also chain multiple by --exclude txt cpp ect...")

    args = parser.parse_args()

    ftp = FTP(args.ip_address, user="pycopter", passwd="calpoly123")

    ftp.set_pasv(True)

    ftp.getwelcome()

    ftp.cwd('flash')

    with Capturing() as files:
        ftp.dir()

    print("\nFiles on board: ")

    files_to_delete = []
    for line in files:
        line = line.split()
        line = line.pop()
        print(line)
        files_to_delete.append(line)

    files_to_delete.remove("sys")
    files_to_delete.remove("lib")
    files_to_delete.remove("cert")
    if not args.b:
        print("\nPreserving boot file...")
        files_to_delete.remove("boot.py")

    print("\nFiles to be deleted are: ")
    for file in files_to_delete:
        print(file)
        ftp.delete(file)
    print("Files Deleted!")

    files_to_write = os.listdir(args.dir)

    if not args.b:
        files_to_write.remove("boot.py")

    if args.exclude:
        print("\nExcluding ", args.exclude, " files")
        for file in files_to_write:
            file_sep = file.split(".")
            for extension in args.exclude:
                if len(file_sep) > 1:
                    if file_sep[1] == extension:
                        # print("removing ", file)
                        files_to_write.remove(file)

    print("\nWriting Files from folder: "+ args.dir)
    print("\nFile currently being written: ")
    for file in files_to_write:
        print(file)
        with open(args.dir+"/"+file, mode='rb') as file_to_send:
            ftp.storbinary("STOR "+file, file_to_send)

    ftp.quit()
    ftp.close()
    print("\nConnection Closed! ")


if __name__ == '__main__':
    main()

