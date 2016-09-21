#!/usr/bin/env python

import random 

array_len = 1000

if __name__ == '__main__':
    array_file = open('array.txt', 'w')
    counter = 0
    #array = []
    while counter < array_len:
        value = random.randint(0, 10)
        counter += 1
        #array.append(value)
        if counter < array_len: 
            array_file.write(str(value) + ' ')
        else:
            array_file.write(str(value))
    #array_file.write(str(array) + '\n')
    array_file.close()



