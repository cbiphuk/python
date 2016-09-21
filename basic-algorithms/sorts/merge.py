#!/usr/bin/env python

import time

def merge(array_a, begin, middle, end, array_b):
    k = 0 
    i = begin
    j = middle
    print 'initial array_b', array_b
    while k < end - begin:
        
        if i < middle and (j >= end or array_a[i] < array_a[j]):
            array_b[k] = array_a[i]
            i += 1
        else:
            array_b[k] = array_a[j]
            j += 1
        k += 1
    print 'array_b', array_b
    
def copy_array(array_a, begin, end, array_b):
    k = 0
    print 'len a: ', end - begin, 'start from: ',begin, 'end: ', end
    print 'len b: ', len(array_b), 'array_b: ', array_b
    for i in range(begin, end):
        print 'array_b', array_b
        array_a[i] = array_b[k]
        print 'add value %d to position %d' % (array_b[k], i)
        k += 1
        print 'k =', k
    print 'sort array_a :', array_a
    

def split_merge(array_a, begin, end, array_b):
    if end - begin < 2:
        print array_a[begin:end]
        return

    middle = (begin + end) / 2
    split_merge(array_a, begin, middle, array_b)
    split_merge(array_a, middle, end, array_b)
    merge(array_a, begin, middle, end, array_b)
    copy_array(array_a, begin, end, array_b) 

def merge_sort(array_a):
    array_b = [None] * len(array_a)
    #for i in range(len(array_a)):
    #    array_b.append(array_a[i])

    split_merge(array_a, 0, len(array_a), array_b)

def main():
    
    array_file = open('array.txt')
    array = map(int, array_file.read().split())
    start_time = time.time()
    print array
    merge_sort(array)
    print '-----%s take seconds------' % (time.time() - start_time)



if __name__ == '__main__':
    main()
