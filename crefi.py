#!/usr/bin/python

from __future__ import with_statement
import sys
import os
import re
import random
from optparse import OptionParser
import time
import string
import errno
import logging
import tarfile
datsiz = 0
timr = 0

def setLogger(filename):
    global logger
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    return

def setupLogger(filename):
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def os_rd(src, size):
    global datsiz
    fd = os.open(src,os.O_RDONLY)
    data = os.read(fd, size)
    os.close(fd)
    datsiz = datsiz + size
    return data

def os_wr(dest, data):
    global timr
    st = time.time()
    fd = os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0644)
    os.write(fd, data)
    os.close(fd)
    ed = time.time()
    timr = timr+(ed-st)
    return

def create_sparse_file(fil,size,mins,maxs,rand):
    if rand:
        size = random.randint(mins, maxs)
    else:
        size = size
    data = os_rd("/dev/zero", size)
    os_wr(fil, data)
    return

def create_binary_file(fil,size,mins,maxs,rand):
    if rand:
        size = random.randint(mins, maxs)
    else:
        size = size
    data = os_rd("/dev/urandom", size)
    os_wr(fil, data)
    return

def create_txt_file(fil,size,mins,maxs,rand):
    if rand:
        size = random.randint(mins, maxs)
    if size < 500*1024:
        data = os_rd("/etc/services", size)
        os_wr(fil, data)
    else:
        data = os_rd("/etc/services", 512*1024)
        file_size = 0
        fd = os.open(fil,os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0644)
        while file_size < size:
            os.write(fd, data)
            file_size += 500*1024
        os.close(fd)
    return

def create_tar_file(fil,size,mins,maxs,rand):
    if rand:
        size = random.randint(mins, maxs)
    else:
        size = size
    data = os_rd("/dev/urandom", size)
    os_wr(fil, data)
    tar = tarfile.open(fil+".tar.gz","w:gz")
    tar.add(fil)
    tar.close()
    os.unlink(fil)
    return

def get_filename(flen):
    size = flen
    char = string.uppercase+string.digits
    st = ''.join(random.choice(char) for i in range(size))
    ti = str((hex(int(str(time.time()).split('.')[0])))[2:])
    return ti+"~~"+st

def text_files(files, file_count,inter,size,mins,maxs,rand,flen,randname):
    global datsiz,timr
    for k in range(files):
        if not file_count%inter:
            logger.info("Total files created -- "+str(file_count))
        if not randname:
            fil = "file"+str(k)
        else:
            fil = get_filename(flen)
        create_txt_file(fil,size,mins,maxs,rand)
        file_count += 1
    return file_count

def sparse_files(files, file_count,inter,size,mins,maxs,rand,flen,randname):
    for k in range(files):
        if not file_count%inter:
            logger.info("Total files created -- "+str(file_count))
        if not randname:
            fil = "file"+str(k)
        else:
            fil = get_filename(flen)
        create_sparse_file(fil,size,mins,maxs,rand)
        file_count += 1
    return file_count

def binary_files(files, file_count,inter,size,mins,maxs,rand,flen,randname):
    for k in range(files):
        if not file_count%inter:
            logger.info("Total files created -- "+str(file_count))
        if not randname:
            fil = "file"+str(k)
        else:
            fil = get_filename(flen)
        create_binary_file(fil,size,mins,maxs,rand)
        file_count += 1
    return file_count

def tar_files(files, file_count,inter,size,mins,maxs,rand,flen,randname):
    for k in range(files):
        if not file_count%inter:
            logger.info("Total files created -- "+str(file_count))
        if not randname:
            fil = "file"+str(k)
        else:
            fil = get_filename(flen)
        create_tar_file(fil,size,mins,maxs,rand)
        file_count += 1
    return file_count

def rename_files(files,flen,randname):
    if not randname:
        for k in range(files):
            os.rename("file"+str(k),"file"+str(files+k))
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            if not os.path.isdir(fil):
                newfil=get_filename(flen)
                os.rename(fil,newfil)
    return


def truncate_files(files,mins,maxs,randname):
    if not randname:
        for k in range(files):
            byts = random.randint(mins,maxs)
            fd = os.open("file"+str(k), os.O_WRONLY)
            os.ftruncate(fd,byts)
            os.close(fd)
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            if not os.path.isdir(fil):
                byts = random.randint(mins,maxs)
                fd = os.open(fil, os.O_WRONLY)
                os.ftruncate(fd,byts)
                os.close(fd)
    return


def chmod_files(files,flen,randname):
    if not randname:
        for k in range(files):
            mod=random.randint(0,511)
            os.chmod("file"+str(k),mod)
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            mod=random.randint(0,511)
            os.chmod(fil,mod)
    return


def chown_files(files,flen,randname):
    if not randname:
        for k in range(files):
            u = random.randint(1025,65536)
            g = -1
            os.chown("file"+str(k),u,g)
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            u = random.randint(1025,65536)
            g = -1
            os.chown(fil,u,g)
    return


def chgrp_files(files,flen,randname):
    if not randname:
        for k in range(files):
            g = random.randint(1025,65536)
            u = -1
            os.chown("file"+str(k),u,g)
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            g = random.randint(1025,65536)
            u = -1
            os.chown(fil,u,g)
    return


def symlink_files(files,flen,randname):
    try:
        os.makedirs("symlink_to_files")
    except OSError as ex:
        if not ex.errno is errno.EEXIST:
            raise
    if not randname:
        for k in range(files):
            src_file = os.path.abspath("file"+str(k))
            os.symlink(src_file,"symlink_to_files/file"+str(k)+"_sym")
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            newfil = get_filename(flen)
            src_file = os.path.abspath(fil)
            os.symlink(src_file,"symlink_to_files/"+newfil)
    return

def hardlink_files(files,flen,randname):
    try:
        os.makedirs("hardlink_to_files")
    except OSError as ex:
        if not ex.errno is errno.EEXIST:
            raise
    if not randname:
        for k in range(files):
            src_file = os.path.abspath("file"+str(k))
            os.link(src_file,"hardlink_to_files/file"+str(k)+"_hard")
    else:
        dirs = os.listdir('.')
        for fil in dirs:
            if not os.path.isdir(fil):
                newfil = get_filename(flen)
                src_file = os.path.abspath(fil)
                os.link(src_file,"hardlink_to_files/"+newfil)
    return

def human2bytes(size):
    size_short = {
        1024 : ['K','KB','KiB','k','kB','kiB'],
        1024*1024 : ['M','MB','MiB'],
        1024*1024*1024 : ['G','GB','GiB']
}
    num = re.search('(\d+)',size).group()
    ext = size[len(num):]
    num = int(num)
    if ext == '':
        return num
    for value, keys in size_short.items():
        if ext in keys:
            size = num*value
            return size

def bytes2human(byts):
    abbr={
        1<<30L : "GB",
        1<<20L : "MB",
        1<<10L : "KB",
        1 : "bytes"
        }
    if byts == 1:
        return '1 bytes'
    for factor, suffix in abbr.items():
        if byts >= factor:
            break
    return "%.3f %s" % (byts / factor,suffix)


def multipledir(mnt_pnt,brdth,depth,files,fop, file_type="text",inter="1000", size="100K",mins="10K",maxs="500K",rand=False,l=10, randname=False):
    files_count = 1
    size = human2bytes(size)
    maxs = human2bytes(maxs)
    mins = human2bytes(mins)
    for i in range(brdth):
        dir_depth = mnt_pnt
        for j in range(depth):
            dir_depth = dir_depth+"/"+"level"+str(j)+str(i)
            try:
                os.makedirs(dir_depth)
            except OSError as ex:
                if not ex.errno is errno.EEXIST:
                    raise
            os.chdir(dir_depth)
            if fop == "create":
                logger.info("Entering the directory level"+str(j)+str(i))
                if file_type == "text":
                    files_count = text_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
                elif file_type == "sparse":
                    files_count = sparse_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
                elif file_type == "binary":
                    files_count = binary_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
                elif file_type == "tar":
                    files_count = tar_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
                else:
                    logger.error("Not a valid file type")
                    sys.exit(1)

            elif fop == "rename":
                logger.info("Started renaming files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+" ...")
                rename_files(files,l,randname)
                logger.info("Finished renaming files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

            elif fop == "chmod":
                logger.info("Started changing permission of files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+" ...")
                chmod_files(files,l,randname)
                logger.info("Finished changing permission of files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

            elif fop == "chown":
                logger.info("Started changing ownership of files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+" ...")
                chown_files(files,l,randname)
                logger.info("Finished changing ownership of files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

            elif fop == "chgrp":
                logger.info("Started changing group ownership of files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+" ...")
                chgrp_files(files,l,randname)
                logger.info("Finished changing group ownership of files for the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

            elif fop == "symlink":
                logger.info("Started creating symlink to the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+"...")
                symlink_files(files,l,randname)
                logger.info("Finished creating symlink to the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

            elif fop == "hardlink":
                logger.info("Started creating hardlink to the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+"...")
                hardlink_files(files,l,randname)
                logger.info("Finished creating hardlink to the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

            elif fop == "truncate":
                logger.info("Started truncating the files 0 to "+str(files)+" in the directory level"+str(j)+str(i)+"...")
                truncate_files(files,mins,maxs,randname)
                logger.info("Finished truncating the files 0 to "+str(files)+" in the directory level"+str(j)+str(i))

    if fop == "create":
        thrpt = datsiz / timr
        logger.info("finished creating files with throughput ---- "+ bytes2human(thrpt)+"ps")



def singledir(mnt_pnt, files, fop, file_type="text",inter="1000", size="100K",mins="10K",maxs="500K",rand=False,l=10, randname=False):

    files_count = 1
    os.chdir(mnt_pnt)
    size = human2bytes(size)
    maxs = human2bytes(maxs)
    mins = human2bytes(mins)
    if fop == "create":
        if file_type == "text":
            files_count = text_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
        elif file_type == "sparse":
            files_count = sparse_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
        elif file_type == "binary":
            files_count = binary_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
        elif file_type == "tar":
            files_count = tar_files(files, files_count,inter,size,mins,maxs,rand,l,randname)
        else:
            logger.info("Not a valid file type")
            sys.exit(1)
        thrpt = datsiz / timr
        logger.info("finished creating files with avg throughput ---- "+bytes2human(thrpt)+"ps")

    elif fop == "rename":
        logger.info("Started renaming files for the files 0 to "+str(files)+"...")
        rename_files(files,l,randname)
        logger.info("Finished renaming files for the files 0 to "+str(files))

    elif fop == "chmod":
        logger.info("Started changing permission of files for the files 0 to "+str(files)+"...")
        chmod_files(files,l,randname)
        logger.info("Finished changing permission of files for the files 0 to "+str(files))

    elif fop == "chown":
        logger.info("Started changing ownership of files for the files 0 to "+str(files)+"...")
        chown_files(files,l,randname)
        logger.info("Finished changing ownership of files for the files 0 to "+str(files))

    elif fop == "chgrp":
        logger.info("Started changing group ownership of files for the files 0 to "+str(files)+"...")
        chgrp_files(files,l,randname)
        logger.info("Finished changing group ownership of files for the files 0 to "+str(files))

    elif fop == "symlink":
        logger.info("Started creating symlink to the files 0 to "+str(files)+"...")
        symlink_files(files,l,randname)
        logger.info("Finished creating symlink to the files 0 to "+str(files))

    elif fop == "hardlink":
        logger.info("Started creating hardlink to the files 0 to "+str(files)+"...")
        hardlink_files(files,l,randname)
        logger.info("Finished creating hardlink to the files 0 to "+str(files))

    elif fop == "truncate":
        logger.info("Started truncating the files 0 to "+str(files)+"...")
        truncate_files(files,mins,maxs,randname)
        logger.info("Finished truncating the files 0 to "+str(files))


if __name__ == '__main__':
    usage = "usage: %prog [option] <MNT_PT>"
    parser = OptionParser(usage=usage)
    parser.add_option("-n", dest="files",type="int" ,default=100,
                      help="number of files in each level [default: %default]")
    parser.add_option("--size", action = "store",type="string",default="100k",
                      help="size of the files to be used [default: %default]")
    parser.add_option("--random",  action="store_true", default=False,
                      help="random size of the file between --min and --max "
                      "[default: %default]")
    parser.add_option("--max", action = "store",type="string", default="500K",
                      help="maximum size of the files, if random is True "
                      "[default: %default]")
    parser.add_option("--min", action = "store",type="string", default="10K",
                      help="minimum size of the files, if random is True "
                      "[default: %default]" )
    parser.add_option("--single", action="store_true", dest="dir",default=True,
                      help="create files in single directory [default: %default]" )
    parser.add_option("--multi", action="store_false", dest="dir",
                      help="create files in multiple directories")
    parser.add_option("-b", dest="brdth",type="int",default=5,
                      help="number of directories in one level(works with --multi)[default: %default]")
    parser.add_option("-d", dest="depth",type="int",default=5,
                      help="number of levels of directories(works with --multi)[default: %default]")
    parser.add_option("-l", dest="flen",type="int" ,default=10,
                      help="number of bytes for filename ( Used only when randname is enabled) "
                      "[default: %default]")
    parser.add_option("-t","--type", action="store", type="string" , dest="file_type",default="text",
                      help="type of the file to be created (text, sparse, binary, tar) [default: %default]" )
    parser.add_option("-I", dest="inter", type="int", default=100,
                      help="print number files created of interval [defailt: %default]")
    parser.add_option("--fop", action="store", type="string", dest="fop", default="create",
                      help="fop to be performed on the files ( create,rename,chmod,chown,chgrp,symlink,hardlink,truncate) [default: %default]")
    parser.add_option("-R", dest="randname", action="store_false", default=True,
                       help="To disable random file name [default: Enabled]")


    (option,args) = parser.parse_args()
    if not args:
        print "usage: <script> [option] <MNT_PT>"
        print ""
        sys.exit(1)
    logger = setupLogger("testlost")
    args[0] = os.path.abspath(args[0])

    if option.dir:
        singledir(args[0], option.files, option.fop, option.file_type, option.inter, option.size, option.min, option.max, option.random, option.flen, option.randname)
    else:
        multipledir(args[0], option.brdth, option.depth, option.files,option.fop, option.file_type, option.inter, option.size, option.min, option.max, option.random, option.flen, option.randname)
