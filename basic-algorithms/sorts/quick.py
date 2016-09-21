#!/usr/bin/env python
import sys

def partition(new_list, lo, hi):
    pivot = new_list[hi]
    #print 'pivot: ', pivot
    i = lo - 1
    for j in range(lo, hi):
        if new_list[j] <= pivot:
            i += 1
            #print 'i=%d, j=%d' % (i, j)
            new_list[i], new_list[j] = new_list[j], new_list[i]
            #print 'new list: ', new_list
    new_list[i + 1], new_list[hi] = new_list[hi], new_list[i + 1]
    #print new_list 
    #i += 1 
    return i + 1

def quicksort(new_list, lo, hi):
    if lo < hi:
        part = partition(new_list, lo, hi)
        quicksort(new_list, lo, part - 1)
        quicksort(new_list, part + 1, hi)


def main():
    new_list = []
    try:
        newfile = open('array.txt', 'r')
    except IOError as ioe:
        print "%d, %s" % (ioe.errno, ioe.strerror)
        sys.exit(1)
    try:
        new_list = map(int, newfile.readline().split())
    except ValueError as ve:
        print 'File contain incorrect values'
        sys.exit(1)
    print 'original list: ', new_list
    quicksort(new_list, 0, len(new_list) - 1)
    print 'final: ', new_list



if __name__ == '__main__':
    main()
