#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Week 5 - Assignment 5 - Data Structures 2
"""


class Stack(object):
    """
    Stack data structure
    """

    def __init__(self):
        """
        Stack object constructor
        :return: None
        """
        self.items = []

    def is_empty(self):
        """
        Checks if stack is empty
        :return: (Bool)- True of False
        """
        return self.items == []

    def push(self, item):
        """
        Add item to stack
        :param item: (Mixed)
        :return: None
        """
        self.items.insert(0, item)

    def pop(self):
        """
        Remove last item in stack
        :return: (Mixed)
        """
        return self.items.pop(0)

    def peek(self):
        """
        Returns last stack entry
        :return: (Mixed)
        """
        return self.items[0]

    def size(self):
        """
        Returns number of items in stack
        :return: (Int)
        """
        return len(self.items)


class Queue(object):
    """
    Queue object implementation
    """

    def __init__(self):
        """
        Queue object constructor
        :return: None
        """
        self.items = []

    def is_empty(self):
        """
        Checks if queue is empty
        :return: (Bool) - True or False
        """
        return self.items == []

    def enqueue(self, item):
        """
        Append item to queue
        :param item: (Mixed)
        :return: None
        """
        self.items.insert(0, item)

    def dequeue(self):
        """
        Returns first entry in queue
        :return: (Mixed)
        """
        return self.items.pop()

    def size(self):
        """
        Returns number of items in queue
        :return: (Int)
        """
        return len(self.items)
