from __future__ import print_function
from minmax import MinMaxHeap
import os
import sys

QSIZE = 3 
def main(argv):
				sortlargefile(argv[1]);

def sortlargefile(filename):
				fp = open(filename, "r+")
				offsets = getlineoffsets(fp)
				numlines = getlines(fp)
				fp.close()
				sortrecursively(filename, offsets, 0, 0, numlines, numlines)

def writesorted(filename, offsets, depq, start, pos1, pos2, end):
				if(pos2- pos1<=1): return 
				#print("Writesort called with parameters ",start, pos1, pos2, end)
				fw = open("newfile", "w+")
				fp = open(filename, "r+")
				fp.seek(0)
				linesread = 0
				while (linesread<pos1):
								linestr = fp.readline()
								fw.write(linestr)
								linesread+=1
				while not depq.isEmpty():
								#print("Depq: "+linestr)
								linestr = depq.PopMin()
								fw.write(linestr)
								#print("Pos2: ", pos2)
				while (linesread<pos2):
								fp.readline()
								linesread+=1
				while (linesread<end):
								linestr = fp.readline()
								linesread+=1
								fw.write(linestr)
				fw.close()
				os.remove(filename)
				os.rename("newfile", filename)
				#write from start to pos1, then depq, then pos2 to end

def writetemp(filename, depq, offsets, start, pos1, pos2, end):
				if(pos2- pos1<=1): return 
				#print("Writetemp called with parameters ",start, pos1, pos2, end)
				fp = open(filename, "r+")
				fw = open("newfile", "w+")
				left = open("left", "r")
				right = open("right", "r")
				fp.seek(0)
				linesread = 0
				while (linesread<pos1):
								linestr = fp.readline()
								fw.write(linestr)
								linesread+=1
				for linestr in left:
								fw.write(linestr)
				while not depq.isEmpty():
								linestr = depq.PopMin()
								fw.write(linestr)
				for linestr in right:
								fw.write(linestr)
				while (linesread<pos2):
								fp.readline()
								linesread+=1
				while (linesread<end):
								#print("Pos2, linesread", pos2, linesread)
								linestr = fp.readline()
								linesread+=1
								fw.write(linestr)

				fw.close()
				os.remove(filename)
				os.rename("newfile", filename)

def sortrecursively(filename, offsets, start, pos1, pos2, end):
				fp = open(filename, "r+")
				offsets = getlineoffsets(fp)
				if(pos2-pos1<=1):
								fp.close()
								return
				arr = []
				depq = MinMaxHeap(arr)
				linesread = 0
				#print("After pos1: "+fp.readline())
				while (linesread<pos1):
								fp.readline()
								linesread+=1
				linesread = 0
				if(pos2-pos1<=QSIZE):
								while (linesread < (pos2-pos1)):
												linestr = fp.readline()
												depq.Insert(linestr)
												linesread+=1
								#just store sort and return
								#depq.sort()
								writesorted(filename, offsets, depq, start, pos1, pos2, end)
				else:
								while (linesread<QSIZE):
												linestr = fp.readline()
												depq.Insert(linestr)
												linesread += 1
								#depq.sort()
								left = open("left", "w+")
								right = open("right", "w+")
								leftlines = 0
								rightlines = 0
								while (linesread<(pos2-pos1)):
												linestr = fp.readline()
												linesread +=1
												if (linestr<depq.PeekMin()):
																left.write(linestr)
																leftlines+=1
												elif linestr>=depq.PeekMax():
																right.write(linestr)
																rightlines+=1
												else:
																#print("utely: "+linestr, end = "")
																right.write(depq.PopMax())
																depq.Insert(linestr)
																#depq.sort()
																rightlines+=1
								left.close()
								right.close()
								writetemp(filename, depq, offsets, start, pos1, pos2, end)
								del depq
								sortrecursively(filename, offsets, start, pos1, pos1+leftlines+1, end)
								sortrecursively(filename, offsets, start, pos1+leftlines+QSIZE, pos2, end)
								#store. make left. make right.
								#call sort on left. call sort on right.
				#fp.seek(offsets[pos2])
				fp.close()

sortrecursively.counter = 0
def getlines(fp):
				fp.seek(0);
				lines = 0
				for line in fp:
								lines += 1
				return lines

def getlineoffsets(fp):
				lineoffset = []
				offset = 0
				fp.seek(0)
				for line in fp:
								lineoffset.append(offset)
								offset += len(line)
				lineoffset.append(offset)
				fp.seek(0)
				return lineoffset

if __name__=="__main__":
				main(sys.argv)
