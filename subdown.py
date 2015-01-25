from requests import get
import os
from shutil import move
import hashlib
from re import sub

def get_hash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            #size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def getSub(filename):    
    filename = sub(r'"', "", filename)
    subname = sub(r"\..{1,3}$", ".srt", filename)

    if not(os.path.exists(subname)):
        url = 'http://api.thesubdb.com'
        payload = {'action': 'download',
                   'hash': get_hash(filename),
                   'language': 'en'}
        myHeader = {'User-Agent': 'SubDB/1.0 (SubDown/0.1; http://github.com/Shanks512/sub-down'}

        r = get(url, params=payload, headers=myHeader)      
        
        if(r.status_code == 200):        
            with open(subname, 'wb') as subtitle:
                subtitle.write(r.content)
            print "Subtitle Ready!!"    
        else:
            print "Status Code:", r.status_code
            print "No sub available. Sorry.\n"

def folderize(filename):
    filename = sub(r'"', "", filename)    
    subname = sub(r"\..{1,3}$", ".srt", filename)
    foldername = sub(r"\..{1,3}$", "", filename)    

    if(os.path.exists(subname) and os.path.exists(filename)):
        os.mkdir(foldername)        
        move(filename, foldername)       
        move(subname, foldername)
        print "Folderized!!\n"

while(True):
    moviepath = raw_input("Path: ")
    #print filename
    getSub(moviepath)
    folderize(moviepath)
