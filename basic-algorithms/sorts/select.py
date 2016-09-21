#!/usr/bin/env python


import time

def select_sort(array):
    for i in range(len(array)):
        is_min = False
        min = i
        for j in range(i, len(array)):
            if array[min] > array[j]:
                min = j
                is_min = True
        if is_min == True:
            array[min], array[i] = array[i], array[min]


def main():
    array_file = open('array.txt')
    array = map(int, array_file.read().split())
    start_time = time.time()
    print array
    select_sort(array)
    print array
    print '-------- %s seconds ----' % (time.time() - start_time)


if __name__ == '__main__':
    main()
