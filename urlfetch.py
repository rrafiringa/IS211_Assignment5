#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reusable url fetching module
"""

import urllib2


def fetch_url(url):
    """
    URL fetcher
    :param url: (String) URL to fetch
    :return: (string) URL data
    """
    try:
        return urllib2.urlopen(urllib2.Request(url))
    except urllib2.URLError as error:
        if hasattr(error, 'reason'):
            print r"Could not connect to server."
            print r'Reason: ', error.reason
        elif hasattr(error, 'code'):
            print r"The server couldn't fulfill the request."
            print r"Error code: ", error.code
