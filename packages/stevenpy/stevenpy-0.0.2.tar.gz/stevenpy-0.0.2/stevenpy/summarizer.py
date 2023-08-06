# -*- coding: utf-8 -*-
"""
Created on Wed May 19 15:12:10 2021

@author: Steven Verwer
"""
#from pathlib import Path

import csv

import stevenpy

class summarizer:
    def __init__(self, **kwargs):
        self.search_object = kwargs.get('searcher')
    
    def run(self):
        processed_files = stevenpy.listdir_dirs_only(self.search_object.processed_loc)
        for task_obj in self.search_object.tasks:
            data = []
            header = ['filename']
            resultfile = ''.join( [task_obj.title, '_summary', '.csv'] )
            resultfilepath = self.search_object.res_loc / resultfile
            first_file = True
            for directory in processed_files:
                row_counter = 1
                file = ''.join( [task_obj.title, '.csv'] )
                filepath = self.search_object.processed_loc / directory / file
                with open(filepath, mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        #condition1 = ( not row[0] )
                        #if condition1:
                        #    continue
                        
                        condition2 = ( first_file == True )
                        if condition2:
                            header += row
                            data += [', '.join( header ) + '\n']
                            first_file = False
                            
                        condition3 = ( row_counter != 1 )
                        if condition3:
                            dataline = [directory] + row
                            data += [', '.join( dataline ) + '\n']
                        
                        row_counter +=1
            data = ''.join(data)
            with open(resultfilepath, mode='w') as f:
                f.write(data)
                
                
                
                
                
                
                
                
                
                
                
                
                
                