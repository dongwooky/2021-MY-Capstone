# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 02:23:25 2021

@author: dongwooky
"""
lists = ['nice to', 'hi hello']
food_label = open('./food_label.txt', 'r')
lines = food_label.readlines()
        
for l in lists:
    for line in lines:
        line = line.rstrip('\n')
        if l.find(line) > -1:
            print(line)
food_label.close()