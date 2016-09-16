from __future__ import print_function
from minmax import MinMaxHeap
import os
import sys

def buildheap(args):
   ar = []
   f = open(args, "r")
   for line in f:
      ar.append(line)
   hp = MinMaxHeap(ar)
   #hp.printheap()
   print("Sorted Heap")
   hp.sortheap()
   
buildheap(sys.argv[1])


