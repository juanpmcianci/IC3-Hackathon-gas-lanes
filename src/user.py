#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:48:17 2023

@author: juanpablomadrigalcianci
"""

from typing import List, Dict, Any
from random import randint

# User class to submit messages to the mempool
class User:
    def __init__(self):
        self.mempool = []

    def submit_message(self, message: str):
        self.mempool.append(message)
