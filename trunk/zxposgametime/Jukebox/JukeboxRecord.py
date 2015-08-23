'''
JukeboxRecord is a data supplier, the data contain all the records of user book music information

Members of JukeboxRecord:
RecordList: 
    Save all the Jukebox songs which is booked by user
    It saved into a file formatted as following:
        [20080724AM] 
        F:\Music\Song1.mp3
        F:\Music\Song2.mp3

        [20080724PM]
        F:\Music\Song5.mp3
        F:\Music\Song6.mp3

        [20080725AM]
        F:\Music\Song8.mp3
        F:\Music\Song9.mp3
    When this data loaded into RecordList, it saved as following:
        {'20080724PM': ['F:\\Music\\Song5.mp3', 'F:\\Music\\Song6.mp3'],
        '20080724AM': ['F:\\Music\\Song1.mp3', 'F:\\Music\\Song2.mp3'],
        '20080725AM': ['F:\\Music\\Song8.mp3', 'F:\\Music\\Song9.mp3']}

LastUpdateTime:
    The last update time
'''

import os
import datetime
import PubFun

class JukeboxRecord(object):

    def __init__(self, filePath):
        self._recordList = {}
        self.lastUpdateTime = datetime.datetime.now()
        self.filePath = filePath
        self.__loadrecord__()
        pass

    def __loadrecord__(self):
        '''
        Load song booked records from file
        It is indexed by date+[PM|AM]
        and the content is song list
        '''
        self.lastUpdateTime = datetime.datetime.now()
        self._recordList.clear()

        if False == os.path.exists(self.filePath):
            return False;
            pass

        file = open(self.filePath)

        curSector = ""
        for line in file:
            line = line.strip()
            if len(line) > 2 and line[0] == "[" and line[-1] == "]":
                curSector = line[1:-1]
                self._recordList[curSector] = []
                pass
            else:
                if line != "" and curSector != "":
                    self._recordList[curSector].append(line)
                    pass
                pass
            pass

        file.close()
        pass

    def __saverecord__(self):
        '''
        Save the records into a file
        '''
        self.lastUpdateTime = datetime.datetime.now()

        file = open(self.filePath, 'w')
        
        keys = self._recordList.keys()
        keys.sort()

        #for sector, songList in self._recordList.iteritems():
        for sector in keys:
            songList = self._recordList[sector]
            print >> file, "[" + sector + "]"
            for song in songList:
                print >> file, song
                pass
            print >> file, ""
            pass

        file.close()
        pass
    
    def _getRecords(self):
        today = datetime.datetime.today()
        ret = {}
        for i in range(7):
            sector = today.strftime("%Y%m%dAM")
            if self._recordList.has_key(sector):
                ret[sector] = self._recordList[sector]
            else:
                ret[sector] = []
            sector = today.strftime("%Y%m%dPM")
            if self._recordList.has_key(sector):
                ret[sector] = self._recordList[sector]
            else:
                ret[sector] = []
            
            oneDay = datetime.timedelta(days=1) 
            today += oneDay
            pass
        return ret;
        pass
    
    def _setRecords(self, value):
        for sector, songList in value.iteritems():
            self._recordList[sector] = songList
            pass
        #print self._recordList
        self.__saverecord__()
        return True
        pass
    
    # has issues of property set, does not fixed so far
    # ==> fixed, class must inhanced from object can make fset work, i do not know why
    self.records = property(fget = _getRecords, fset = _setRecords, doc = '')
        
    pass

'''
record = JukeboxRecord("E:\\Projects\\Jukebox\\JukeboxRecord.dat")
recordList = record.records;
#print recordList
recordList["20080724PM"] = ["test1", "test2"]
record.records = recordList
#print recordList
'''