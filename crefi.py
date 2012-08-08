#!/usr/bin/python

from __future__ import with_statement
import sys
import os
import random
from optparse import OptionParser

def os_rd(src, size):
    fd = os.open(src,os.O_RDONLY)
    data = os.read(fd, size)
    os.close(fd)
    return data

def os_wr(dest, data):
    fd = os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0644)
    os.write(fd, data)
    os.close(fd)
    return

def create_sparse_file(fil):
    if option.size:
        option.random = False
        size = option.size
    else:
        size = random.randint(option.min, option.max)
    data = os_rd("/dev/zero", size*1024)
    os_wr(fil, data)
    return

def create_txt_file(fil):
    if option.size:
        option.random = False
        size = option.size
    else:
        size = random.randint(option.min, option.max)
    if size < 500:
        data = os_rd("/etc/services", size*1024)
        os_wr(fil, data)
    else:
        data = os_rd("/etc/services", 500*1024)
        file_size = 0
        fd = os.open(fil,os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0644)
        while file_size < size:
            os.write(fd, data)
            file_size += 500
        os.close(fd)
    return

def text_files(files, file_count):
    for k in range(files):
        if not file_count%100:
            print file_count
        create_txt_file("file"+str(k))
        file_count += 1
    return file_count

def sparse_files(files, file_count):
    for k in range(files):
        if not file_count%100:
            print file_count
        create_sparse_file("file"+str(k))
        file_count += 1
    return file_count

def multipledir(mnt_pnt,brdth,depth,files):
    files_count = 0
    for i in range(brdth):
        breadth = mnt_pnt+"/"+str(i)
        os.makedirs(breadth)
        os.chdir(breadth)
        dir_depth = breadth
        print breadth
        for j in range(depth):
            dir_depth = dir_depth+"/"+str(j)
            os.makedirs(dir_depth)
            os.chdir(dir_depth)
            if option.file_type:
                files_count = text_files(files, files_count)
            else:
                files_count = sparse_files(files, files_count)

def singledir(mnt_pnt, files):
    files_count = 0
    os.chdir(mnt_pnt)
    if option.file_type:
        files_count = text_files(files, files_count)
    else:
        files_count = sparse_files(files, files_count)


if __name__ == '__main__':
    usage = "usage: %prog [option] <MNT_PT>"
    parser = OptionParser(usage=usage)
    parser.add_option("-b", dest="brdth",type="int",default=5,
                      help="number of directories in one level [default: %default]")
    parser.add_option("-d", dest="depth",type="int",default=5,
                      help="number of levels of directories [default: %default]")
    parser.add_option("-n", dest="files",type="int" ,default=100,
                      help="number of files in each level [default: %default]")
    parser.add_option("--size", action = "store",type="int",
                      help="size of the files to be used in KB")
    parser.add_option("--random",  action="store_true", default=True,
                      help="random size of the file between --min and --max "
                      "[default: %default]")
    parser.add_option("--max", action = "store",type="int", default=500,
                      help="maximum size(KB) of the files, if random is True "
                      "[default: %default]")
    parser.add_option("--min", action = "store",type="int", default=10,
                      help="minimum size(KB) of the files, if random is True "
                      "[default: %default]" )
    parser.add_option("--text", action="store_true", dest="file_type",default=True,
                      help="create text files [default: %default]" )
    parser.add_option("--sparse", action="store_false",dest="file_type",
                      help="create sparse files ")
    parser.add_option("--single", action="store_true", dest="dir",default=True,
                      help="create files in single directory [default: %default]" )
    parser.add_option("--multi", action="store_false", dest="dir",
                      help="create files in multiple directories")
    (option,args) = parser.parse_args()
    if not args:
        print "usage: <script> [option] <MNT_PT>"
        print ""
        sys.exit(1)
    args[0] = os.path.abspath(args[0])
    if option.dir:
        singledir(args[0], option.files)
    else:
        multipledir(args[0], option.brdth, option.depth, option.files)
