#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Week 5 - Assignment 5 - Data Structures 2
"""

import argparse
import csv
import os

from adts import Queue
from urlfetch import fetch_url


class Server(object):
    """
    Generic request processor.
    """

    def __init__(self, rps=1):
        """
        Server object
        :param rps: (Int) Optional - Requests per second
        :return: None
        """
        self.req_rate = rps
        self.current_req = None
        self.time_remaining = 0

    def tick(self):
        """
        Request execution countdown ticker
        :return: None
        """
        if self.current_req is not None:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_req = None

    def busy(self):
        """
        Server busy state
        :return: Bool
        """
        if self.current_req is not None:
            return True
        else:
            return False

    def start_next(self, new_req):
        """
        Process a new request
        :param new_req: (Request) Request object
        :return: None
        """
        self.current_req = new_req
        self.time_remaining = new_req.get_exec_time() / self.req_rate


class Request(object):
    """
    Request object
    """

    def __init__(self, req_item):
        """
        Request object constructor
        :param req_item: (Request) - Request object
        :return: None
        """
        try:
            self.timestamp = int(req_item[0])
            self.req_uri = req_item[1]
            self.exec_time = int(req_item[2])
        except IndexError:
            print 'Malformed request record: ', req_item

    def get_stamp(self):
        """
        Return request timestamp
        :return: (Int)
        """
        return self.timestamp

    def get_uri(self):
        """
        Returns request URI
        :return: (String)
        """
        return self.req_uri

    def get_exec_time(self):
        """
        Returns request execution time
        :return: (Int)
        """
        return self.exec_time

    def wait_time(self, current_time):
        """
        Returns request wait time from current time
        :param current_time: (Int) Reference time
        :return: (Int)
        """
        return current_time - self.exec_time


def simulate_one_server(input_file):
    """
    Server simulator
    :param input_file: (File) - Request inputs file.
    :return: (Float) - Average wait time for a request
    """
    www = Server()
    req_queue = Queue()
    try:
        with open(input_file, 'rb') as infile:
            req_data = csv.reader(infile)
            w_times = []
            for row in req_data:
                req_queue.enqueue(Request(row))
                if not www.busy() and not req_queue.is_empty():
                    curr = req_queue.dequeue()
                    www.start_next(curr)
                    curr_time = curr.get_stamp()
                    w_times.append(curr.wait_time(curr_time))
                    www.tick()
            avg_wait = float(sum(w_times)) / len(w_times)
            return 'Average wait: {:.2f} seconds\n' \
                   '\t Tasks remaining {}' \
                .format(avg_wait, req_queue.size())
    except IOError:
        print 'Could not open {}'.format(input_file)


def simulate_many_servers(input_file, num_servers):
    rr_items = {}
    averages = []
    out = ''
    try:
        for count in range(num_servers):
            rr_items[count] = {}
            rr_items[count]['server'] = Server()
            rr_items[count]['queue'] = Queue()
            rr_items[count]['times'] = [0.0]

        with open(input_file, 'rb') as infile:
            req_data = csv.reader(infile)
            eof = False
            try:
                while not eof:
                    for key, item in rr_items.iteritems():
                        row = req_data.next()
                        item['queue'].enqueue(Request(row))
                        if not item['server'].busy() and not item['queue'].is_empty():
                            curr = item['queue'].dequeue()
                            item['server'].start_next(curr)
                            curr_time = curr.get_stamp()
                            item['times'].append(curr.wait_time(curr_time))
                            item['server'].tick()
            except StopIteration:
                eof = True

        for key, item in rr_items.iteritems():
            avg_wait = float(sum(item['times'])) / len(item['times'])

            out += 'Server {}:\n' \
                   '\tAverage wait: {:.2f} seconds.\n' \
                   '\tTasks remaining: {}.\n' \
                .format(key, avg_wait, item['queue'].size())

    except IOError:
        print 'Could not open file ', input_file

    return out


if __name__ == '__main__':
    URL = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--file', required=False, type=str, default=URL)
    PARSER.add_argument('--servers', required=False, type=int, default=20)
    ARGS = PARSER.parse_args()
    FILE = ''
    if ARGS.file:
        URL = ARGS.file
        FILE = os.path.basename(URL)
        with open(FILE, 'wb') as OUTFILE:
            READER = csv.reader(fetch_url(URL), dialect='excel')
            WRITER = csv.writer(OUTFILE)
            for line in READER:
                WRITER.writerow(line)
    if ARGS.servers:
        print simulate_many_servers(FILE, ARGS.servers)
    else:
        print simulate_one_server(FILE)
