#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 2014 year

__author__ = 'suxoza'


import sys,os,time,paramiko,time,stat

class MainError(Exception):
    pass

class ftp:
    def __init__(self):
        self.replace_ = False
        self.replace_from = "eruditor/"
        self.replace_to = "eruditor/"

        self.input_()

    def default(self):
        self.host  = "lilu.ge"
        self.port  = 22
        self.user  = "suxoza"
        self.passw = "burdga"
        self.file_name  = "/var/www/lilu/admin"#"/home/suxoza/1"
        self.get_put  = "p"
        self.replace_ = False
        self.file_or_dir = 'd'

        if self.get_put == 'g':
            type = input("config file or directioin? [f,d] ").strip()
            if type in ['f','d']:
                self.file_or_dir = type
            else: raise TypeError
        return (self.connect_ftp() if self.file_or_dir == 'f' else self.connect_tcp())

    def input_(self):
        try:
            if input("default? [y,n] ") in ("\n".strip(),"yes","y"):raise MainError
            (self.host,self.port,self.user,self.passw,self.file_name) = (
                str(input("enter host: ")),
                int(input("enter port: ")),
                input("enter userName: "),
                input("enter userPass: "),
                input("enter config file / or directory location: ")
            )
            if input("replace? [y,n] ") in ("\n".strip(),"yes","y"):
                self.replace_ = True
                self.replace_from = input("replace: ")
                self.replace_to = input("replace to: ")

            self.get_put = input("get or put? [g,p] ").strip()

            if self.get_put == 'p':
               if not os.path.exists(self.file_name):raise FileNotFoundError("config file / dir not found")
               if os.path.isfile(self.file_name):return self.connect_ftp()
               elif os.path.isdir(self.file_name):return self.connect_tcp()



        except MainError as e:
                self.default()
        except ValueError as e:
                sys.exit(e)
        except FileNotFoundError as e:
                sys.exit(e)

    def connect_ftp(self):




        self.ssh_ftp_()

        try:
            tm = time.time()
            with open(self.file_name) as read_:
                rea = [(x.strip(),x.strip().replace(self.replace_from,self.replace_to) if self.replace_ else x.strip()) for x in read_.readlines() if x.strip()]
                for a,b in rea:
                   if self.get_put == 'p':
                      if not os.path.isfile(a):
                          continue
                      self.ssh_ftp.put(a, b)
                   if self.get_put == 'g':
                      print(self.replace_from,self.replace_to)
                      self.ssh_ftp.get(b, a)
                   print(a,b,sep=" | ")
                print("count: "+str(len(rea)),"time: "+str(round(time.time() - tm,2)),sep=" | ")
        except FileNotFoundError as e:
            sys.exit("config file not found! {}".format(e))

    def connect_tcp(self):

        self.ssh_tcp_()
        self.ssh_ftp_()
        if self.get_put == 'g':
            self.replace_from,self.replace_to = self.replace_to,self.replace_from


        try:
            tm = time.time()
            server_dir = self.file_name.replace(self.replace_from,self.replace_to) if self.replace_ else self.file_name
            stdin,stdout,stderr = self.ssh_tcp('[ ! -d "{}" ] || echo "yes"'.format(server_dir))
            if stdout.read().decode().strip():
                self.ssh_tcp('rm -R {}'.format(server_dir))
                print("delete old files...")
                time.sleep(2)


            iterator_file = 0
            iterator_dir = 0
            for(a,b,c) in os.walk(self.file_name):
                iterator_dir += 1
                server_dir = a.replace(self.replace_from,self.replace_to) if self.replace_ else a
                st = oct(os.stat(a)[stat.ST_MODE])[-3:]
                #self.ssh_tcp('mkdir {0} && chmod {1} {0}'.format(server_dir,st))
                self.ssh_tcp('mkdir {0}'.format(server_dir))
                #print('mkdir {0} && chmod {1} {0}'.format(server_dir,st))
                print('mkdir {0}'.format(server_dir))

                time.sleep(10)
                for file in c:
                    iterator_file += 1
                    current_file_name = os.path.join(a,file)
                    server_file_name = os.path.join(server_dir,file)
                    self.ssh_ftp.get(current_file_name, server_file_name)
                    print(current_file_name, server_file_name)
            print("count: file-"+str(iterator_file)+" , dir-"+str(iterator_dir),"time: "+str(round(time.time() - tm,4)),sep=" | ")


        except Exception as e:
            sys.exit(e)
            return

    def ssh_ftp_(self):
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.user, password=self.passw)
            self.ssh_ftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            sys.exit(e)

    def ssh_tcp_(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.host, username=self.user, password=self.passw, port=self.port)
            self.ssh_tcp = client.exec_command
        except Exception as e:
            sys.exit(e)


if __name__ == "__main__":
   ftp()

