# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:53:58 2021

@author: Steven Verwer
"""

class task (object):
    def __init__(self, search_type='regex', **kwargs):
        '''
        This class is used to talk to the searcher and generate tasks:
        Currently there are two types available (task.search_type):
            - 'special':
                * task.function accepts a function handle as input
                This function will get all pages and must export 'data' which
                should be organised as str: Res1,...,etc\nRes2,...,etc AND
                correspond to task.header: Header1, ... HeaderN
                
            - 'regex':
                * task.expression accepts regex string to search for a
                string in each line in each page.
                For more info see: https://docs.python.org/3/library/re.html
                * further only task.label of type string can be given to
                change the result header name of the found_strings.
            
            Other properties are:
                task.title: Title of the search task.
        '''
        self.search_type = search_type
        self.title = kwargs.get('title', self.search_type)
        
        if search_type == 'regex':
            self.expression = kwargs.get('expression')
            self.label = kwargs.get('label','found_string')
        elif search_type == 'special':
            self.func = kwargs.get('func')
            self.tags_mode = kwargs.get('tags_mode',False)
            self.header = kwargs.get('header')
        else:
            raise Exception('Given search_type: ' + self.search_type +
                            ' could not be identified.\n' + "Use 'special' or 'regex'.")
        return