#-*- coding:utf-8 -*-
def sumfoo(*values):
    s = 0
    for v in values:
        i = int(v)
        s = s + i
    print s
 
def outputfoo():
    print('print something')
