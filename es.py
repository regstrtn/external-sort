from __future__ import print_function
import os

QSIZE = 25
def main():
				sortlargefile("words1.txt");

def sortlargefile(filename):
				fp = open(filename, "r+")
				offsets = getlineoffsets(fp)
				numlines = getlines(fp)
				sortrecursively(fp, offsets, 0, 0, numlines-1, numlines-1)
				fp.close()

def writesorted(fp, offsets, depq, start, pos1, pos2, end):
				fw = open("newfile", "w")
				fp.seek(offsets[start])
				linesread = 0
				while (linesread<pos1):
								linestr = fp.readline()
								fw.write(linestr)
								linesread+=1
				for linestr in depq:
								fw.write(linestr)
				fp.seek(offsets[pos2])
				for linestr in fp:
								fw.write(linestr)
				fw.close()
				os.rename("newfile", "oldfile")
				fp = open("oldfile", "r")
				return fp
				#write from start to pos1, then depq, then pos2 to end

def writetemp(fp, left, right, depq, offsets, start, pos1, pos2, end):
				for line in right:
								print(line)
				fw = open("newfile", "w")
				fp.seek(offsets[start])
				linesread = 0
				while (linesread<pos1):
								linestr = fp.readline()
								fw.write(linestr)
								linesread+=1
				for linestr in left:
								fw.write(linestr)
				for linestr in depq:
								fw.write(linestr)
				for linestr in right:
								fw.write(linestr)
				fp.seek(offsets[pos2])
				for linestr in fp:
								fw.write(linestr)
				fw.close()
				os.rename("newfile", "oldfile")
				fp = open("oldfile", "r")
				return fp




def sortrecursively(fp,offsets,start, pos1, pos2, end):
				depq = []
				linesread = 0
				fp.seek(offsets[pos1])
				if(pos2-pos1<=QSIZE):
								while (linesread < (pos2-pos1)):
												linestr = fp.readline()
												depq.append(linestr)
												linesread+=1
								#just store sort and return
								depq.sort()
								fp = writesorted(fp, offsets, depq, start, pos1, pos2, end)
								pass
				else:
								print("is greater than QSIZE")
								while (linesread<QSIZE):
												linestr = fp.readline()
												depq.append(linestr)
												linesread += 1
								depq.sort()
								left = open("left", "r+")
								right = open("right", "r+")
								leftlines = 0
								rightlines = 0
								while (linesread<(pos2-pos1)):
												print("hello word")
												right.write("hello world")
												linestr = fp.readline()
												linesread +=1
												if linestr<depq[0]:
																left.write(linestr)
																leftlines+=1
												if linestr>depq[-1]:
																right.write(linestr)
																rightlines+=1
												else:
																right.write(depq[-1])
																depq[-1] = linestr
																depq.sort()
																#print(depq[-1], end = "")
																rightlines+=1
								fp = writetemp(fp, left, right, depq, offsets, start, pos1, pos2, end)
								#sortrecursively(fp, offsets, start, pos1, pos1+leftlines, end)
								#sortrecursively(fp, offsets, start, pos1+leftlines+QSIZE, pos2, end)
								#store. make left. make right.
								#call sort on left. call sort on right.
				fp.seek(offsets[pos2])
				fp.close()


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
				fp.seek(0)
				return lineoffset

if __name__=="__main__":
				main()

