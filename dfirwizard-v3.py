#!/usr/bin/env python3

# Sample program or step 3 in becoming a DFIR Wizard!
# No license as this code is simple and free!

import sys
import pytsk3
import datetime

imagefile = "\\\\.\\PhysicalDrive0"
imagehandle = pytsk3.Img_Info(imagefile)
partitionTable = pytsk3.Volume_Info(imagehandle)
for partition in partitionTable:
  print(f"{partition.addr}, {partition.desc}, {partition.start}({partition.start * 512}), {partition.len}")
  if 'NTFS' in partition.desc:
    filesystemObject = pytsk3.FS_Info(imagehandle, offset=(partition.start*512))
    fileobject = filesystemObject.open("/$MFT")
    print("File Inode: {fileobject.info.meta.addr}")
    print("File Name: {fileobject.info.name.name}")
    print("File Creation Time: {datetime.datetime.fromtimestamp(fileobject.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')}")
    
    outFileName = str(partition.addr)+fileobject.info.name.name
    print(outFileName)
    
    outfile = open(outFileName, 'w')
    filedata = fileobject.read_random(0,fileobject.info.meta.size)
    outfile.write(filedata)
    outfile.close
