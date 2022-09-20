"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

Written by Phani Pavan K <kphanipavan@gmail.com>
Use this code as per GPLv3 guidelines
"""


import enum


class bcolors:
    # bcolors class taken from https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Log(enum.Enum):
    SUC = 0
    INF = 1
    WRN = 2
    ERR = 3


def debug(comment: str, level: Log = Log.INF):
    if level == Log.INF:
        print(f'{bcolors.OKBLUE}[i]', comment, bcolors.ENDC)
    elif level == Log.WRN:
        print(f'{bcolors.WARNING}[!]', comment, bcolors.ENDC)
    elif level == Log.ERR:
        print(f'{bcolors.FAIL}[x]', comment, bcolors.ENDC)
    elif level == Log.SUC:
        print(f'{bcolors.OKGREEN}[✓]', comment, bcolors.ENDC)


if __name__ == "__main__":

    debug('info')
    debug('warn', Log.WRN)
    debug('error', Log.ERR)
    debug('success', Log.SUC)
