# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:45:19 2021

@author: Steven Verwer
"""

from pathlib import Path

import os

from tqdm import tqdm

from math import floor

from multiprocessing import Pool, cpu_count

import stevenpy

class searcher (object):
    '''
        the searcher object is a simple handler that combines pdf scraping,
        paralel processing and tekst analysing tasks given by the search_task
        class.
        
        To run the searcher after initialisation call: 
            *.run()
        '''
    def __init__(self, **kwargs):
        
        '''
        Initialisation requires:
            - dat_loc: string that contains the directory of the data.
            - res_loc: string that contains the directory of the results.
            - result_filename: string which is used to name the final result
            file.
            - (not recommended) maxpages: integer value, changes how many pages
            per pdf are analysed.
            - cpuload: decimal between 0 and 1, used to set the wanted cpuload.
            - tasks: list of search_task classes, [task1,taskt2,taskN].
        '''
        #load settings
        self.check_progression = kwargs.get('check_progression', True)
        stevenpy.__check_instance__(self.check_progression, bool)
        
        
        
        
        # data and result paths
        stevenpy.__check_instance__( kwargs.get('dat_loc', 'data'), str )
        self.dat_loc = Path( kwargs.get('dat_loc', 'data') )
        

        stevenpy.__check_instance__( kwargs.get('res_loc', 'result'), str )
        self.res_loc = Path( kwargs.get('res_loc', 'result') )
        
        
        # result filename (without extension)
        self.result_filename = kwargs.get('result_filename', 'result')
        stevenpy.__check_instance__(self.result_filename, str)
        
        # max pages: 0 (default) => infinite
        self.maxpages = kwargs.get('maxpages', 0)
        stevenpy.__check_instance__(self.maxpages, int)
        
        # number of cores to use based on cpuload %
        stevenpy.__check_instance__( kwargs.get('cpuload',0.5) , int)
        self.num_cpu = max(1, floor((2 + cpu_count()) * min(kwargs.get('cpuload',0.5),1)) )
        
        # load tasks in searcher class and check if correct
        self.tasks = kwargs.get('tasks')
        if isinstance(self.tasks, stevenpy.task):
            self.tasks = [self.tasks]
        stevenpy.__check_instance__( self.tasks , list )
        for each in self.tasks:
            stevenpy.__check_instance__( each , stevenpy.task)

        # processed location
        self.processed_loc = self.res_loc / kwargs.get('processed_foldername', 'processed_files')
        
        # create directories if not existing
        Path(self.res_loc).mkdir(parents=True, exist_ok=True)
        Path(self.processed_loc).mkdir(parents=True, exist_ok=True)
        return
    
    def run(self):
        # create pool
        pool = Pool(self.num_cpu)
        
        # fire workers
        jobs=[]
        for file in os.listdir(self.dat_loc):
            job = pool.apply_async(self.__worker__, (file,))
            jobs.append(job)
        
        # check progress
        if self.check_progression:
            for job in tqdm(jobs):
                job.get()
        elif not self.check_progression:
            for job in jobs:
                job.get()
            
        # close and join pool
        pool.close()
        pool.join()
    
    def __worker__(self, file):
        if not self.tasks:
            return
        
        ''' processes a pdf file given by main() and writes output to q (queue)'''
        filename = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]

        if extension!='.pdf':
            return None
        Path(self.processed_loc / filename).mkdir(parents=True, exist_ok=True)
        
        # init PDF class (this class is used to get pages from the PDF and process pdftext)
        pdf_object = stevenpy.pdf_class(dat_loc=self.dat_loc,maxpages=self.maxpages)
        
        # extract pages
        pdf_pages_generator_object = pdf_object.__get_pages__(file)
        pages = []
        data = ''
        for page in pdf_pages_generator_object:
            pages.append(page)
        
        for each in self.tasks:
            if each.search_type == 'regex':
                data = pdf_object.__inbuild_regex__(pages,each.expression,each.label)
                filenamecsv = each.title + '.csv'
                with open(self.processed_loc / filename / filenamecsv, 'w', newline='') as f:
                    f.write(data)
            
            if each.search_type == 'special':
                data = each.header + '\n'
                pageNum = 1
                for page in pages:
                    if each.tags_mode:
                        layout_textlines = pdf_object.__layout_textlines__(page)
                        data += each.function(layout_textlines,pageNum)
                    else:
                        pagestr = pdf_object.__pagestr__(page)
                        data += each.func(pagestr,pageNum)
                    pageNum +=1
                filenamecsv = each.title + '.csv'
                with open(self.processed_loc / filename / filenamecsv, 'w', newline='') as f:
                    f.write(data)
        pdf_object.__terminate__()
        return data
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    