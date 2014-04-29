
#Crefi 
Crefi is a Python command-line tool to create files and do file operations on created data.
It provides basic operations to create files of differrent
sizes, in different layout, along with other options.

Typical use involves creating large number of files of different sizes,
over different layout.


####EXAMPLES:
####
  ```python crefi.py MNT_PT```

       Creates 100 text files in the directory MNT_PT of random size
       between 10K and 500K [Filename length will be 20 bytes
       first 10 bytes will be current time, next 10 bytes will be
       combination of letters(A-Z) and numbers(1-9)]
####
  ```python crefi.py --multi -b 10 -d 10 -n 1000 --type=sparse --size=100 MNT_PT```

       Create files in directory MNT_PT in the directory
       layout of 10 directories in each level, and 10 directories
       depth and in each directory, create 1000 sparse files of size 100K.
