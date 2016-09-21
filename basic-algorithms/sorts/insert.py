#!/usr/bin/env python

import time

def insert_sort(array):
    for i in range(len(array) - 1):
        #print 'i is '+ str(i)
        if array[i] > array[i+1]:
            cur = i + 1
            #print '-------------'
            #print array
            #print '%d is bigger then %d' % (array[i], array[i+1])
            found = False
            for j in range(i, -1, -1):
                #print 'j is %d' % j
                if array[cur] > array[j]:
                    #print '%d is bigger then %d' % (array[cur], array[j])
                    val = array[cur]
                    #print '%d inserted to position %d' % (array[cur], j+1)
                    array.insert(j + 1, array.pop(cur))
                    found = True
                    break
                else: None #print '%d not bigger then %d' % (array[cur], array[j])
            
            if found == False:
                #print '%d inserted to the beggining' % array[cur]
                array.insert(0, array.pop(cur))
                



def main():
    arr_file = open('array.txt')
    array = map(int, arr_file.read().split())
    
    start_time = time.time()
    
    print array
    insert_sort(array)
    print '------ %s seconds --------' % (time.time() - start_time)
    print array

if __name__ == '__main__':
    main()


