#!/usr/bin/python

import os
import errno
import argparse
from version import __version__
from multiprocessing import Process
from crefi_helper import singledir, multipledir


def multiple(mnt_pnt, brdth, depth, files, fop, file_type="text", inter="1000",
             size="100K", mins="10K", maxs="500K", rand=False, l=10,
             randname=False, threads=1):
    threadlist = []
    for i in range(threads):
        print threads
        if threads == 1:
            dir_path = mnt_pnt
        else:
            dir_path = mnt_pnt+"/"+"thread"+str(i)
        try:
            os.makedirs(dir_path)
        except OSError as ex:
            if ex.errno is not errno.EEXIST:
                raise

        t = Process(target=multipledir, name="thread-"+str(i),
                    args=(dir_path, brdth, depth, files, fop, file_type,
                    inter, size, mins, maxs, rand, l, randname))
        threadlist.append(t)
        t.start()
    for thr in threadlist:
        thr.join()


def single(mnt_pnt, files, fop, file_type="text", inter="1000",
           size="100K", mins="10K", maxs="500K", rand=False, l=10,
           randname=False, threads=1):
    threadlist = []
    for i in range(threads):
        if threads == 1:
            dir_path = mnt_pnt
        else:
            dir_path = mnt_pnt+"/"+"thread"+str(i)
        try:
            os.makedirs(dir_path)
        except OSError as ex:
            if ex.errno is not errno.EEXIST:
                raise

        t = Process(target=singledir, name="thread-"+str(i),
                    args=(dir_path, files, fop, file_type, inter, size,
                    mins, maxs, rand, l, randname))
        threadlist.append(t)
        t.start()
    for thr in threadlist:
        thr.join()


def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.
                                     ArgumentDefaultsHelpFormatter)
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {version}'.
                        format(version=__version__))
    parser.add_argument("-n", dest="files", type=int, default=100,
                        help="number of files in each level ")
    parser.add_argument("--size", action="store", default="100k",
                        help="size of the files to be used ")
    parser.add_argument("--random",  action="store_true", default=False,
                        help="random size of the file between --min and --max")
    parser.add_argument("--max", action="store", default="500K",
                        help="maximum size of the files, if random is True")
    parser.add_argument("--min", action="store", default="10K",
                        help="minimum size of the files, if random is True")
    parser.add_argument("--single", action="store_true", dest="dir",
                        default=True, help="create files in single directory")
    parser.add_argument("--multi", action="store_false", dest="dir",
                        help="create files in multiple directories")
    parser.add_argument("-b", dest="brdth", type=int, default=5,
                        help="number of directories in one level(works " +
                        "with --multi) ")
    parser.add_argument("-d", dest="depth", type=int, default=5,
                        help="number of levels of directories  (works " +
                        "with --multi) ")
    parser.add_argument("-l", dest="flen", type=int, default=10,
                        help="number of bytes for filename ( Used only when " +
                        "randname is enabled) ")
    parser.add_argument("-t", action="store", dest="file_type",
                        default="text", choices=["text", "sparse", "binary",
                                                 "tar"],
                        help="type of the file to be created ()")
    parser.add_argument("-I", dest="inter", type=int, default=100,
                        help="print number files created of interval")
    parser.add_argument("--fop", action="store", dest="fop", default="create",
                        choices=["create", "rename", "chmod", "chown", "chgrp",
                                 "symlink", "hardlink", "truncate",
                                 "setxattr"],
                        help="fop to be performed on the files")
    parser.add_argument("-R", dest="randname", action="store_false",
                        default=True, help="To disable random file name " +
                        "(default: Enabled)")
    parser.add_argument("mntpnt", help="Mount point")
    parser.add_argument("-T", dest="threads", type=int, default=1,
                        help="Number of threads used to create files")

    args = parser.parse_args()
    args.mntpnt = os.path.abspath(args.mntpnt)

    if args.dir:
        single(args.mntpnt, args.files, args.fop, args.file_type,
               args.inter, args.size, args.min, args.max,
               args.random, args.flen, args.randname, args.threads)
    else:
        multiple(args.mntpnt, args.brdth, args.depth, args.files,
                 args.fop, args.file_type, args.inter, args.size,
                 args.min, args.max, args.random, args.flen,
                 args.randname, args.threads)


if __name__ == '__main__':
    main()
