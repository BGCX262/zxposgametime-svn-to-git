'''

This module is specialized on Extracting music information from a dirctionary.

Giving it a directionary, and it gonna return all the music file information in this directionary.

This module pick up music file by its extension name. 
And the following extension name is recognized as music file:
    mp3
    ape
    rm
    wma

The following information of music file is collected:
    FileName
    CreateTime
    ModifyTime
    FileSize


Author: xiaopai
DateTime: 2008-7-17

'''

import os, sys
from stat import *
import id3

class MusicInfoReader(object):

    def __init__(self):
        self.musicInfoList = []
        pass

    def __walkdir__(self, top, callback):
        '''recursively descend the directory tree rooted at top,
            calling the callback function for each regular file'''

        for f in os.listdir(top):
            pathname = os.path.join(top, f)
            mode = os.stat(pathname)[ST_MODE]
            if S_ISDIR(mode):
                # It's a directory, recurse into it
                self.__walkdir__(pathname, callback)
            elif S_ISREG(mode):
                # It's a file, call the callback function
                callback(pathname)
            else:
                # Unknown file type,
                pass
        pass

    def __visitfile__(self, fileName):
        '''
        Visiting a file and get file information if it is a music file
        '''
        extendName = fileName.split('.')[-1]
        extendName = extendName.lower()
        if extendName == "mp3" \
            or extendName == "ape"\
            or extendName == "rm"\
            or extendName == "wma" :
            info = {}
            
            # file information
            info["FileName"] = fileName.split('\\')[-1]
            info["CreateTime"] = os.path.getctime(fileName)
            info["ModifyTime"] = os.path.getmtime(fileName)
            info["Size"] = os.path.getsize(fileName)
            
            #mp3 information
            if (extendName == "mp3"):
                try:
                    mp3Header = id3.load(fileName)
                    info["Album"] = mp3Header["album"]
                    info["Artist"] = mp3Header["artist"]
                    info["Title"] = mp3Header["title"]
                    info["Track"] = mp3Header["track"]
                    info["Year"] = mp3Header["year"]
                    pass
                except:
                    info["Album"] = ""
                    info["Artist"] = ""
                    info["Title"] = ""
                    info["Track"] = ""
                    info["Year"] = ""
                    pass
                pass
            
            self.musicInfoList.append(info)
        pass

    def LoadMusicInfo(self, path):
        '''
        Load music information from given path
        '''
        # clear list
        del self.musicInfoList[:]

        # walk direction and get music information
        self.__walkdir__(path, self.__visitfile__)
        return self.musicInfoList
        pass

'''
reader = MusicInfoReader()
print reader.LoadMusicInfo("F:\\Music\\")
'''
