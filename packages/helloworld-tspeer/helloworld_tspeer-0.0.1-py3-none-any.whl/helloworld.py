#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:34:02 2021

@author: newmac
"""

def say_hello(name=None):
    if name is None:
        return 'Hello, World!'
    else:
        return f'Hello, {name}!'
    
    