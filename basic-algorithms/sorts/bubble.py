#!/usr/bin/env python

import time

def bubble_sort(array):
    is_sorted = False
    while is_sorted == False:
        is_sorted = True
        #print array
        for i in range(len(array) - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                is_sorted = False
                #print array
    return array

if __name__ == '__main__':

    arr_file = open('array.txt')

    array = arr_file.read()
    array = array.split()
    array = map(int, array)
    start_time = time.time()
    array = bubble_sort(array)
    print array
    print("--- %s seconds ---" % (time.time() - start_time))


