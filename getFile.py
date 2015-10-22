# -*- coding: utf-8 -*-
import sys, os, glob
import shutil
import pickle
import re
import pandas as pd

fileList=glob.glob('*.csv')
data=pd.read_csv(fileList[0], names=['Filename', 'CotentType', 'inCache', 'url', 'Title', 'Browser', 'cacheType', 'lastAccessed', 'lastModified', 'fileSize', 'copyName', 'path', 'splitCount', 'ip'])
if len(fileList)>1:
    for i in range(1,len(fileList)):
        fileList[i]=pd.read_csv(fileList[i], names=['Filename', 'CotentType', 'inCache', 'url', 'Title', 'Browser', 'cacheType', 'lastAccessed', 'lastModified', 'fileSize', 'copyName', 'path', 'splitCount', 'ip'])
    data=data.append(fileList[1:])

with open('courseIDDict','r') as input:
    courseIDDict=pickle.load(input)    

os.mkdir('videos')    
for index,row in data.iterrows():
    urlMatch=re.match('(https://taiwan.s3.hicloud.net.tw/)(\d+)/.+',row.url)
    if urlMatch!=None:
        name=courseIDDict[urlMatch.group(2)]
        shutil.copyfile(row.path, '{}/videos/{}.mp4'.format(os.getcwd(),name))