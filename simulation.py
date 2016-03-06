#!/usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Week 5 - Assignment 5 - Data Structures 2
"""

import argparse
import urlfetch
import adts

class Server(object):
    """
    Generic request processing.
    """
    def __init__(self): pass


class Request(object):
    def __init__(self, req_item):
        self.timestamp = req_item[0]
        self.req_uri = req_item[1]
        self.exec_time = self.timestamp + req_item[2]

    def get_stamp(self):
        return self.timestamp

    def get_uri(self):
        return self.req_uri

    def get_exec_time(self):
        return self.exec_time

    def wait_time(self, current_time):
        return current_time - self.exec_time

