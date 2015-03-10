__author__ = 'z9764'
import threading
from pathlib import Path
import codecs
import json
import todoku
import sys
import time
import re

word_list=[]

logff=None
q_status=False

class Myworker(threading.Thread):
    def __init__(self,dstPath,OutPath):
        threading.Thread.__init__(self)
        self.dstpath = Path(dstPath)
        self.outpath =Path(OutPath)
        pass
    def run(self):
        global logff
        global word_list
        xxit = self.dstpath.iterdir()
        cd =todoku.cDokuConvert()
        logff=open("tolog.txt","a")
        log_bad=open("badlog.txt","a")
        errname=""
        for xfile in xxit:
            try:
                infile = str(xfile.resolve())
                fio = codecs.open(infile,"r",'utf-8')
                jdata = json.load(fio)
                myd = re.findall(r"\w+",str(xfile))
                mlen=myd.__len__()
                name=myd[mlen-2]
                print(name)
                errname=name
                logff.writelines(name)
                txt = cd.build_all(jdata,name)
                outp = self.outpath.resolve()
                outfile = str(outp.joinpath(name+".txt"))
                outf=codecs.open(outfile,"w","utf-8")
                outf.write(txt)
                outf.close()
                if q_status==True:
                    break
            except Exception as err:
                print(err)
                log_bad.writelines(errname)
            finally:
                pass
        log_bad.close()
        logff.close()


def mainloop(inpath,outpath):
    global worker_list
    global q_status
    mk=Myworker(inpath,outpath)
    ct=0
    while True:
        keyin =input()
        if keyin =="q":
            q_status=True
            keyin=None
            print("begin to quit all worker ...")
            time.sleep(3)
            print("finish!can relanch workers again!")
            q_status=False
        if keyin =="ex":
            q_status=True
            time.sleep(2)
            keyin=None
            break
        if keyin =="s":

            keyin=None
        if keyin!=None:
            if ct==0:
                mk.start()
                ct=1

# 1 = in path 2=otpath
if __name__ == '__main__':
    mainloop(sys.argv[1],sys.argv[2])
