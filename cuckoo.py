from collections.abc import Collection
from math import e, modf, floor, sqrt
from itertools import filterfalse, chain
from copy import copy
import unittest


# DO NOT CHANGE ANY CODE BETWEEN LINE X AND LINE Y
# ******* THIS IS LINE X ******************

GOLDEN = (1.0 + 5.0 * 0.5) / 2.0


def swap(a, b):
    return b, a


# ***************************************************
# why do we inherit from Collection rather than Set?
# because Set requires too many methods to be defined


class CuckooSet(Collection):

    # *** course helper routines *******
    def _hash2_(self, obj, table_size):
        try:
            h = hash(obj)  # may raise exception
        except Exception:
            raise TypeError("unhashable key")

        h %= table_size

        f1, _ = modf(h * e)
        f2, _ = modf(h * GOLDEN)
        h1 = floor(table_size * f1)
        h2 = floor(table_size * f2)
        if h1 == h2:
            h2 = (h2 + 7) % table_size
        return h1, h2

    def _members_(self, tab):  # returns iterator
        return filterfalse((lambda x: x is None), tab)

    def _allmembers_(self):
        return chain(self._members_(self.htab1), self._members_(self.htab2))

    # ** course methods ****

    def __init__(self, iter=[], *, s=128):
        if s < 4:
            raise ValueError("set size too small")
        self._size_ = s
        self._MAXSWAPS_ = floor(s * 0.6)
        self.htab1 = [None] * s
        self.htab2 = [None] * s
        for i in iter:
            self.add(i)

    def __len__(self):
        count1 = len(list(self._members_(self.htab1)))
        count2 = len(list(self._members_(self.htab2)))
        return count1 + count2

    def _resize_(self):
        oldself = copy(self)
        self.__init__(oldself, s=oldself._size_ * 2)

    def __str__(self):
        fstr = ""
        for v in self._allmembers_():
            if len(fstr):
                fstr += ", "
            fstr += str(v)
        return fstr

    def __iter__(self):
        return self._allmembers_()
# ******* THIS IS LINE Y ******************

# returns true if x is in htab1 or htab2, false otherwise.
# raises ValueError if x is None
    def __contains__(self, x):
        # raise error if x is None
        if x is None:
            raise ValueError("key may not be None")

        h1, h2 = self._hash2_(x, self._size_)  # get hash indices
        if (self.htab1[h1] == x):  # check if in table 1
            return True
        if (self.htab2[h2] == x):  # check if in table 2
            return True
        return False


# removes x from the table if it is present
# throws ValueError if x is not present
    def remove(self, x):
        if x not in self:
            raise ValueError()
        else:
            h1, h2 = self._hash2_(x, self._size_)  # get hash indices
            if (self.htab1[h1] == x):  # check if in table 1
                self.htab1[h1] = None
            if (self.htab2[h2] == x):  # check if in table 2
                self.htab2[h2] = None
        return


# removes x from the table if it is present
# quietly returns if x is not present
    def discard(self, x):
        if x not in self:
            return
        else:
            h1, h2 = self._hash2_(x, self._size_)  # get hash indices
            if (self.htab1[h1] == x):  # check if in table 1
                self.htab1[h1] = None
            if (self.htab2[h2] == x):  # check if in table 2
                self.htab2[h2] = None
        return


# adds x to htab1 or htab2, if x is hashable
# will resize the hash table if necessary
    def add(self, x):
        # check if x is already in table
        if x in self:
            return

        # set counter to 0
        counter = 0

        # start
        while (True):

            # compute h1 for x
            h1, h2 = self._hash2_(x, self._size_)

            # check if htab1[h1] is empty
            if (self.htab1[h1] == None):
                # if yes, place x here and return
                self.htab1[h1] = x
                return
            else:
                # if no, swap x and the element at htab1[h1]
                temp = self.htab1[h1]
                self.htab1[h1] = x
                x = temp

            # compute h2 for new x
            h1, h2 = self._hash2_(x, self._size_)

            # check if htab2[h2] is empty
            if (self.htab2[h2] == None):
                # if yes, place x here and return
                self.htab2[h2] = x
                return
            else:
                # if no, swap x and htab2[h2]
                temp = self.htab2[h2]
                self.htab2[h2] = x
                x = temp
                # increment counter by 1
                counter += 1

            # if counter is greater than or equal to MAXSWAPS
            if (counter >= self._MAXSWAPS_):
                # resize table
                self._resize_()
                # set counter to zero
                counter = 0
                # go to start

cs = CuckooSet([])
