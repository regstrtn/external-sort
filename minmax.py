from math import log, floor, pow


class MinMaxHeap(object):

    def __init__(self, array=[]):
        super(MinMaxHeap, self).__init__()
        self.heap = [0]
        for i in array:
            self.Insert(i)

    def Insert(self, value):
        self.heap = self.heap + [value]
        self.BubbleUp(len(self.heap) - 1)

    def DeleteAt(self, position):
        self.heap[position] = self.heap[-1]
        del(self.heap[-1])
        self.TrickleDown(position)

    def Index(self, value):
        return self.heap.index(value)

    def PeekMax(self):
        if len(self.heap) > 1:
            return self.heap[1]
        else:
            raise Exception

    def PeekMin(self):
        size = len(self.heap)
        if size > 1:
            c = [self.heap[1]]
            if size > 2:
                c = c + [self.heap[2]]
            if size > 3:
                c = c + [self.heap[3]]
            return min(c)
        else:
            raise Exception

    def PopMax(self):
        m = self.PeekMax()
        mi = self.Index(m)
        self.DeleteAt(mi)
        return m

    def PopMin(self):
        m = self.PeekMin()
        mi = self.Index(m)
        self.DeleteAt(mi)
        return m

    def TrickleDown(self, position):
        if self.OnMinLevel(position):
            self.TrickleDownMin(position)
        else:
            self.TrickleDownMax(position)

    def TrickleDownMin(self, position):
        if self.HasChildren(position):
            min_pair = self.SortPairs(self.ChildrenAndGrandChildren(position))[0]
            m = min_pair[0]  # index of smallest kid
            if self.IsGrandChild(position, m):
                if self.heap[m] < self.heap[position]:
                    self.Swap(m, position)
                    if self.heap[m] > self.heap[self.Parent(m)]:
                        self.Swap(m, self.Parent(m))
                    self.TrickleDownMin(m)
            # if not grandchild, m must be a child
            else:
                if self.heap[m] < self.heap[position]:
                    self.Swap(m, position)
        else:
            pass

    def TrickleDownMax(self, position):
        if self.HasChildren(position):
            max_pair = self.SortPairs(self.ChildrenAndGrandChildren(position))[-1]
            m = max_pair[0]  # index of smallest kid
            if self.IsGrandChild(position, m):
                if self.heap[m] > self.heap[position]:
                    self.Swap(m, position)
                    if self.heap[m] < self.heap[self.Parent(m)]:
                        self.Swap(m, self.Parent(m))
                    self.TrickleDownMax(m)
            # if not grandchild, m must be a child
            else:
                if self.heap[m] > self.heap[position]:
                    self.Swap(m, position)
        else:
            pass

    def BubbleUp(self, position):
        if self.OnMinLevel(position):
            if self.HasParent(position):
                if self.heap[position] > self.heap[self.Parent(position)]:
                    self.Swap(position, self.Parent(position))
                    self.BubbleUpMax(self.Parent(position))
                else:
                    self.BubbleUpMin(position)
        else:
            if self.HasParent(position):
                if self.heap[position] < self.heap[self.Parent(position)]:
                    self.Swap(position, self.Parent(position))
                    self.BubbleUpMin(self.Parent(position))
                else:
                    self.BubbleUpMax(position)

    def BubbleUpMin(self, position):
        grandparent = self.Parent(self.Parent(position))
        if self.HasGrandParent(position):
            if self.heap[position] < self.heap[grandparent]:
                self.Swap(position, grandparent)
                self.BubbleUpMin(grandparent)

    def BubbleUpMax(self, position):
        if self.HasGrandParent(position):
            grandparent = self.Parent(self.Parent(position))
            if self.heap[position] > self.heap[grandparent]:
                self.Swap(position, grandparent)
                self.BubbleUpMax(grandparent)

    def Swap(self, a, b):
        """swap values between a and b"""
        a_val = self.heap[a]
        b_val = self.heap[b]
        self.heap[a] = b_val
        self.heap[b] = a_val

    def Parent(self, child):
        """return child's parent"""
        return int(child) / 2

    def IsGrandChild(self, parent, grand_child):
        """tell whether grand_child is parent's grandchild or not"""
        if self.HasGrandChildren(parent):
            size = len(self.heap)
            if grand_child < size:
                return True
            else:
                return False
        else:
            return False

    def SortPairs(self, list_of_pairs):
        """return 2-tuple representing smallest, sorted by value in second"""
        return sorted(list_of_pairs, key=lambda tup: tup[1])

    def ChildrenAndGrandChildren(self, position):
        """
        return list of children's and grandchildren's indices
        """
        if self.HasChildren(position):
            c = self.countChildren(position)
            a = []
            for i in range(0, c):
		            a = a + [(int(pow(2, position)) + i, self.heap[int(pow(2, position)) + i])]
            if self.HasChildren(int(pow(2, position))):
                cpos = int(pow(2, position))
                c = self.countChildren(cpos)
                for i in range(0, c):
                  a = a + [(int(pow(2, cpos)) + i, self.heap[int(pow(2, cpos)) + i])]
            if self.HasChildren(int(pow(2, position)) + 1):
                cpos = int(pow(2, position)) + 1
                c = self.countChildren(cpos)
                for i in range(0, c):
                	a = a + [(int(pow(2, cpos)) + i, self.heap[int(pow(2, cpos)) + i])]
            return a
        else:
            raise Exception

    def HasParent(self, position):
        p = self.Parent(position)
        if p is not 0:
            return True
        else:
            return False

    def HasGrandParent(self, position):
        gp = self.Parent(self.Parent(position))
        if gp is not 0:
            return True
        else:
            return False
    def countChildren(self, position):
						"""return number of children of a node, 0, 1 or 2"""
						size = len(self.heap)
						if(pow(2, position)<size):
										if((pow(2, position)+1)<size):
														return 2
										else: return 1
						else: return 0

    def HasChildren(self, position):
        """check if 2^position and 2^(position)+1 exist"""
        size = len(self.heap)
        if (pow(2, position) < size) or ((pow(2, position) + 1) < size):
            return True
        else:
            return False

    def HasGrandChildren(self, position):
        """check if either of position's children have children of their own"""
        if self.HasChildren(int(pow(2, position))) or \
           self.HasChildren(int(pow(2, position)) + 1):
            return True
        else:
            return False

    def OnMinLevel(self, position):
        test = self.OnLevel(position) % 2
        if test == 0:
            return False
        else:
            return True

    def OnMaxLevel(self, position):
        test = self.OnLevel(position) % 2
        if test == 0:
            return True
        else:
            return False

    def OnLevel(self, position):
        """returns what level the key at position is on"""
        return floor(log(int(position), 2))
       
    def printheap(self):
						for i in range(0, len(self.heap)):
										print(self.heap[i])

    def Size(self):
       return(len(self.heap)-1)

    def isEmpty(self):
       size = len(self.heap)
       if(size<=1): return True
       else: return False
    
    def isContain(self, x):
       heapset = set(self.heap)
       return x in heapset
       
    def sortheap(self):
         """Print out elements in a sorted order"""
         size = len(self.heap)
         while (size > 1):
										a = self.PopMin()
										print(a) 
										size = len(self.heap)
