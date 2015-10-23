# -*- coding: utf-8 -*-
import sys, os, glob
import shutil
import pickle
import re
import pandas as pd


#讀入檔案(一次可讀多個csv)
fileList=glob.glob('*.csv')
data=pd.read_csv(fileList[0], names=['Filename', 'CotentType', 'inCache', 'url', 'Title', 'Browser', 'cacheType', 'lastAccessed', 'lastModified', 'fileSize', 'copyName', 'path', 'splitCount', 'ip'])
if len(fileList)>1:
    for i in range(1,len(fileList)):
        fileList[i]=pd.read_csv(fileList[i], names=['Filename', 'CotentType', 'inCache', 'url', 'Title', 'Browser', 'cacheType', 'lastAccessed', 'lastModified', 'fileSize', 'copyName', 'path', 'splitCount', 'ip'])
    data=data.append(fileList[1:])

#讀入檔名字典
with open('courseIDDict','r') as input:
    courseIDDict=pickle.load(input)

#清除檔名字典之特殊字元
symbolDict={u'\\':u'＼',u'/':u'／',u':':u'：',u'*':u'＊',u'?':u'？',u'<':u'〈',u'>':u'〉'}
def replaceSymbol(matchObj):
    if matchObj!=None:
        return symbolDict[matchObj.group(0)]            
for key in courseIDDict:
    courseIDDict[key]=re.sub(u'[\\/:*?<>]',replaceSymbol,courseIDDict[key])

#創建資料夾    
if os.path.exists('videos')!=True:
    os.mkdir('videos')

#抓取、重新命名影片    
for index,row in data.iterrows():
    if row['url'].count('/')>4:
        urlMatch=re.match('(https://taiwan.s3.hicloud.net.tw)/(\d+)/(\d+)/(\d+)/.+',row.url)        
        if urlMatch!=None:
            courseID=urlMatch.group(4)                
        else:
            continue
    else:
        urlMatch=re.match('(https://taiwan.s3.hicloud.net.tw/)(\d+)/.+',row.url)
        if urlMatch!=None:
            courseID=urlMatch.group(2)                
        else:
            continue            
    try:
        name=courseIDDict[courseID]
    except:
        print 'you probably have downloaded a video not recored in the courseList'
        print 'the video will not be rename. info: CourseID='+courseID+';fileName='+row['url'].split('/')[-1]
        
    shutil.copyfile(row.path, u'{}\\videos\\{}.mp4'.format(os.getcwd(),name))
    