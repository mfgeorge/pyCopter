#!/bin/python
"""
..  module: push_code
    :platform: Linux
    :synopsis: A script for pushing code to a LoPy using an FTP client

..  topic:: Author

    | Michael George
    | California Polytechnic State University

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
    """
    A context manager class found on stackoverflow for capturing the
    stdout of a function.
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def main():
    """
    Program to copy files in a directory over to the LoPy via an FTP server.
    """
    # The available arguments for the program
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

    # Parse the arguments passed in
    args = parser.parse_args()

    # open an ftp connection and log in to the LoPy's ftp server
    ftp = FTP(args.ip_address, user="pycopter", passwd="calpoly123")

    # set the ftp session into passive mode
    ftp.set_pasv(True)

    # Print the welcome message of the ftp server
    ftp.getwelcome()

    # Change the working directory on the ftp server to the flash folder
    ftp.cwd('flash')

    # Capture the stdout of ftp.dir() into a list
    with Capturing() as files:
        ftp.dir()

    print("\nFiles on board: ")

    # Iterate through the files and print them out, as well as add
    # them to files to delete
    files_to_delete = []
    for line in files:
        line = line.split()
        line = line.pop()
        print(line)
        files_to_delete.append(line)

    # Pop off sys lib and cert, we want to leave these on the server
    # and not delete them
    files_to_delete.remove("sys")
    files_to_delete.remove("lib")
    files_to_delete.remove("cert")
    # Check if the argument was passed to change the boot file
    if not args.b:
        print("\nPreserving boot file...")
        files_to_delete.remove("boot.py")

    # Print out the files that will be deleted
    print("\nFiles to be deleted are: ")
    # Delete all of those files
    for file in files_to_delete:
        print(file)
        ftp.delete(file)
    print("Files Deleted!")

    # list all of the files in the dir to transfer over
    files_to_write = os.listdir(args.dir)

    # check if the boot file is going to be transfered over
    if not args.b:
        try:
            files_to_write.remove("boot.py")
        except ValueError:
            # it wasn't there anyways
            pass

    # Process file extension excludes
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

    # Write the files to the LoPy that are in the specified folder
    for num, file in enumerate(files_to_write):
        with open(args.dir+"/"+file, mode='rb') as file_to_send:
            # STOR command tells ftp server to store file
            ftp.storbinary("STOR "+file, file_to_send)
        print(file + " done." + "\t" + str(num+1) + "/" + str(len(files_to_write)))

    print("Transfer complete!")

    # Close the ftp connections
    ftp.quit()
    ftp.close()
    print("\nConnection Closed! ")


if __name__ == '__main__':
    main()

