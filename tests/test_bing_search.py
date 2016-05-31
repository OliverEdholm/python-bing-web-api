#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Bing search test

This is the main Bing search module. This file is meant to be run by nose.

Oliver Edholm 2016-05-30 21:11
'''
# Imports
from bing_search.web_search import search


# Functions
def setup():
    '''Runs when tests start.'''
    print("Setup!")


def teardown():
    '''Runs when tests stops.'''
    print("Tear down!")


def test_basic():
    '''Runs the test.'''
    search_term = 'Bill Gates'
    result_amount = 70
    api_key = 'API KEY'

    results = search(search_term, result_amount, api_key)
    titles = [result.url for result in results]
    print('Result length:', len(results))
    print('Results head:', titles[:5])
    print('Results tail:', titles[len(titles) - 5:])
    print('Results 1:', titles[:50])
    print('Results 2:', titles[50:])
