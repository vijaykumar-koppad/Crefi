#Crefi

###what is it?
Crefi is a Python command-line tool to create multi threaded workload on a filesystem and do file operations on created data.
It provides basic operations to create files of different sizes, different types, in different directory structures, along with creating symlinks, hardlinks to files, and also rename, truncate, chmod, chown, chgrp and setxattr on the created files.

Typical use involves creating large number of files of different sizes,
over different layout, and do different operations on the created files.


###Examples


```$ crefi <MNT_PT>```

 Creates 100 text files in the directory MNT_PT of random size
 between 10K and 500K [Filename length will be 20 bytes
 first 10 bytes will be current time, next 10 bytes will be
 combination of letters(A-Z) and numbers(1-9)]

```$ crefi --multi -b 10 -d 10 -n 1000 --type=sparse --size=100 <MNT_PT>```

Creates files in the directory layout of 10 directories in each level, and 10 directories
depth and in each directory, create 1000 sparse files of size 100K on mount point.

```$ crefi --multi -b 10 -d 10 -n 10 --type=binary --random --min=1K --max=10K <MNT_PNT> ```

Creates files in the directory layout of 10 directories in each level, and 10 directories
depth and in each directory, create 1000 sparse files of random size between 10K and 1K on mount point.

There are other option. Check it using help    ```crefi -h```


###Latest version

Latest version can be found at [Github](https://github.com/vijaykumar-koppad/Crefi)

### Installation

```$  pip install crefi```

It requires "pyxattr" module to use setxattr option.

To install pyxattr 

```$  pip install pyxattr ```

### Licensing

  Please see the file called LICENSE.

### Contact

Found any issues or have any suggestions to improve the tool, drop a mail at vijaykumar.koppad@gmail.com
