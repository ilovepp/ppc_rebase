#!/usr/bin/python

######################################################################

#

# Copyright (C) 2015

# 

# This program is free software: you can redistribute it and/or modify

# it under the terms of the GNU General Public License as published by

# the Free Software Foundation, either version 3 of the License, or

# (at your option) any later version.

#

# This program is distributed in the hope that it will be useful,

# but WITHOUT ANY WARRANTY; without even the implied warranty of

# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

# GNU General Public License for more details.

#

# You should have received a copy of the GNU General Public License

# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#

######################################################################

import sys

import os

import re

from subprocess import *

from collections import Counter

######################################################################Functions Def

def Usage():

	print "###############################################################"

	print "Find powerpc binary-blob firmware's rebase address!"

	# Please don't remove this. At least respect my rights!

	print "Auther: Lambda"

	print "Usage: {} <file>".format(sys.argv[0])

	print "  file: the path of firmware file"

	print "Examples: "

	print "  {} NOE77101.bin".format(sys.argv[0])

	print "Special thanks to: wzjlovecode"

	print "###############################################################"

	sys.exit(0)



def get_arrow_addr_list(filename):

	f = open(filename,"rb")

	filedata = f.read()

	f.close()

	re_str_patt = "[\x3c\x3d].{3}\x38.{3}" # machine code pattern 0x3c/0x3d XX XX XX 0x38 XX XX XX

	bytedata = bytearray(filedata)

	reObj = re.compile(re_str_patt)

	res=reObj.findall(bytedata)

	resSet= set()

	for r in res:   

		temp=(r[2]<<24)+(r[3]<<16)+(r[6]<<8)+r[7]

		if r[6]>=0x80:

			temp=temp-(1<<16)

		resSet.add(temp)

	resList=list(resSet)

	resList.sort()

	#the code below are do the arrow address cluster

	diff_list = [resList[i] - resList[i-1] for i in range(1,len(resList)) ]

	L={}

	i=0

	Record = False

	while i<len(diff_list):

		Valid = diff_list[i] < 4096 # the max num of a string,can choose othe num

		if Record:

			if Valid:

				L[index].append(diff_list[i])

			else:

				Record = False

		else:

			if Valid:

				Record = True

				index = i

				L[index]=[]

				L[index].append(diff_list[i])

			else:

				pass

		i+=1

	tuplelist = sorted(L.iteritems(),key=lambda x:len(x[1]),reverse=True)	

	return resList[tuplelist[0][0]:tuplelist[0][0]+len(tuplelist[0][1])+1]



def get_target_addr_list(filename):

	str_addr_list=[item.strip().split(' ')[0] for item in Popen(["strings", "--radix=d",filename], stdout=PIPE).communicate()[0].split('\n')]

	str_addr_list.remove('')

	return map(int,str_addr_list)



def rebase(arrow_addr_set,target_addr_set,offset_lowbound,offset_upbound):

	result={}

	result["hitnum"]=0

	result["hitlist"]=[]

	offset = offset_lowbound

	while offset <= offset_upbound:

		temp_list = map(lambda x : x+offset,target_addr_set)

		count=len(arrow_addr_set & set(temp_list))

		result["hitlist"].append(count)

		if count > result["hitnum"]:

			result["hitnum"] = count

			result["offset"] = offset

		offset+=step

	return result

###################################################################### Main Start Here

if len(sys.argv) !=2 or sys.argv[1]=="-h":

	Usage()

inputFile=sys.argv[1]

if not os.path.isfile(inputFile):

	print "Error:file not exist!"

	Usage()

step = 0x400 # memory align,can choose other num

target_addr_list = get_target_addr_list(inputFile)

target_addr_set = set(target_addr_list)

arrow_addr_list = get_arrow_addr_list(inputFile)

arrow_addr_set = set(arrow_addr_list)

offset_upbound = ( int(arrow_addr_list[-1]) - int(target_addr_list[0]) + step )/step*step

offset_lowbound = int(arrow_addr_list[0]) - int(target_addr_list[-1])

if offset_lowbound < 0:

	offset_lowbound = 0

result = rebase(arrow_addr_set,target_addr_set,offset_lowbound,offset_upbound)

print "The rebase address of %s is %s" %(inputFile,hex(result["offset"]))

print "-----------------------details----------------------------"

print "Find %d arrow addresss.They are from %s to %s" %(len(arrow_addr_list),hex(arrow_addr_list[0]),hex(arrow_addr_list[-1]))

print "Find %d target addresss.They are from %s to %s" %(len(target_addr_list),hex(target_addr_list[0]),hex(target_addr_list[-1]))

print "Check offset from %s to %s by step=0x%x" %(hex(offset_lowbound),hex(offset_upbound),step)

print "Offset=%s,Hitnum=%d" %(hex(result["offset"]),result["hitnum"])

orded_pairs = sorted(dict(Counter(result["hitlist"])).iteritems(),key=lambda x:x[0],reverse=True)

print "HitNum-AppearNums pairs:%s %s %s %s %s" %(str(orded_pairs[0]),str(orded_pairs[1]),str(orded_pairs[2]),str(orded_pairs[3]),str(orded_pairs[4]))

