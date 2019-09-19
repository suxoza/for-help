#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 2014 year

__author__ = 'suxoza'


import sys,os,time,paramiko,time,subprocess

class MainError(Exception):
    pass

dir_sufix = '/var/www/'
host_files = dict(
    hall    = dict(port = 22, host = 'hall.loc',user = 'tombala', passw = 'tombala'),
    ghall   = dict(port = 22, host = 'ghall.loc',user = 'gtombala', passw = 'gtombala'),
    cegm    = dict(port = 22, host = 'cegm.local',user = 'tombala', passw = 'tombala'),
    cctv    = dict(port = 23, host = 'cctv.local',user = 'cctv', passw = 'cctv'),
)

ends = ['.php','.js','.coffee','.css','.html','.py','.gz','.twig','.xml']

class ftp:
    def __init__(self):

        self.input_()

    def get_from_git(self, choised):
        os.chdir(dir_sufix+choised)
        out_ = subprocess.check_output("git status", shell = True).splitlines()
        self.files_ = []
        for i in out_:
            dec = str(i.decode())
            it = dec
            it = '.'+it.split('.').pop().strip()
            if not it or (dec and 'deleted:' in dec): continue
            if it in ends:
                self.files_.append(os.path.join(dir_sufix,choised,dec.split().pop()))
        
    def input_(self):
        try:
            keys = list(host_files.keys())
            k = " | ".join(keys)
            i = input("choise host ["+k+"]: ")
            if i in keys:raise MainError(str(i.strip()))
            raise FileNotFoundError("config not foud!")
           



        except MainError as e:
                self.default(str(e))
        except ValueError as e:
                sys.exit(e)
        except FileNotFoundError as e:
                sys.exit(e)

    def default(self, choised):
        self.current = host_files[choised]
        self.get_from_git(choised)
        if len(self.files_):
            self.connect_ftp(choised)

       

    def connect_ftp(self, choised): 
        self.ssh_ftp_()

        try:
            tm = time.time()
            rea = [(x.strip(),x.strip().replace(self.current['replace_from'],self.current['replace_to']) if 'replace_from' in self.current else x.strip()) for x in self.files_ if x.strip()]
            for a,b in rea:
                if not os.path.isfile(a):
                  continue
                self.ssh_ftp.put(a, b)
                print(a,b,sep=" | ")
            os.chdir(os.path.join('/home',str(os.getlogin())))
            if os.path.isfile('git_'+choised):
                os.system("./git_"+choised)
            print("count: "+str(len(rea)),"time: "+str(round(time.time() - tm,2)),sep=" | ")
        except FileNotFoundError as e:
            sys.exit("config file not found! {}".format(e))



    def ssh_ftp_(self):
        try:
            transport = paramiko.Transport((self.current['host'], self.current['port']))
            transport.connect(username=self.current['user'], password=self.current['passw'])
            self.ssh_ftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            sys.exit(e)



if __name__ == "__main__":
   ftp()

