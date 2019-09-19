#!/usr/bin/python3
# -*- coding:utf-8 -*-

# 2014 year

import sys, os

try:
  #from dict_dir import A
  from optparse import OptionParser
except ImportError:
    sys.exit("no optparse module found")


class MyError(Exception):

	def __init__(self, message, errors):
		super().__init__(message)

		#pass #sys.exit("please type with --help first")

#-i /var/www/eruditor/view -e .html -t b -s paliko
#-i /var/www/eruditor/view -e .html -t b -s paliko -r "saxli pali"

#-i /var/www/eruditor/view -e .html -t b -s "\"http://www.onlineolimpiada/\""
#-i /var/www/eruditor/view -e .html -t b -s "\"http://www.onlineolimpiada/\"" -r  "\"http://www.onlineolimpiada/new/\""

class Repl:
	def __init__(self,kwargs):
	    try:
	        self.input       = kwargs['path']
	        self.search      = kwargs['search']
	        self.replace     = kwargs['replace']
	        self.type        = kwargs['type']
	        self.end         = kwargs['end']

	        self.iterator    = 0

	        self.action = 'search_' if not self.replace else 'replace_'
	    except KeyError:
	        print("parameters error")

	def find(self):

		if not (self.input and os.path.exists(self.input)):
			raise Exception("input path not found!!!")

		self.ret_array = []
		self.iterator = 0
		for (a,b,c) in os.walk(self.input):
			for file in c:
				if not os.path.isfile(os.path.join(a,file)):continue
				if self.end:
				  if not file.endswith(self.end):continue
				file_name = os.path.join(a,file)

				getattr(self,self.action)(file_name)


		for x in self.ret_array:
		    print(x)
		print('sum:',self.iterator)


	def replace_(self,file):
	    iter,line = 0,0
	    mode = 'r' if self.type == 's' else 'rb'
	    mode_w = 'w' if self.type == 's' else 'wb'
	    count_ = 0
	    line_ = []
	    ret = "".encode()
	    with open(file,mode) as op:
	      for x in op:
	          line += 1
	          if self.search.encode() in x:
	              ret += x.replace(self.search.encode(),self.replace.encode())
	              line_.append(line)
	              len_ = len(x.split(self.search.encode())) - 1
	              count_ += len_
	              self.iterator += len_
	          else:
	              ret += x
	    if count_:
	       self.ret_array.append(dict(count = count_,file = file,line = line_))
	       with open(file,mode_w) as w:
	          w.write(ret)


	def search_(self,file):
		if not (self.search):raise Exception("please specify search string!")
		iter,line = 0,0
		mode = 'r' if self.type == 's' else 'rb'
		count_ = 0
		line_ = []
		with open(file, mode) as op:
		  for x in op:
		      line += 1
		      if self.search.encode() in x:
		          line_.append(line)
		          len_ = len(x.split(self.search.encode())) - 1
		          count_ += len_
		          self.iterator += len_
		if count_:self.ret_array.append(dict(count = count_,file = file,line = line_))





if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-p", "--pathToSearch", dest="path",help="destination path")#myfindfile
    parser.add_option("-s", "--search", dest="search", help="string what need to found") # -s paliko
    parser.add_option("-r", "--replace", dest="replace",help="if parameter is present then replacing string") # -r pali
    parser.add_option("-t", "--type", dest="type",help="binary or string; if string then don`t works with binnary files!") # -t s || b
    parser.add_option("-e", "--end", dest="end",help="endswith; if need only specific files example: .py will find only python files. same as *.py in linux!") # -e .py

    (options, args) = parser.parse_args()



    a = Repl(vars(options))
    try:
    	a.find()
    except Exception as e:
    	print(str(e))

