#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Bing web search

This module searches Bing web and returns results with the attributes...
* url  -The URL to access the result.
* title  -The results title.
* description  -The description of the result.

You need an Bing search API key to be able to search with Bing.

Oliver Edholm 2016-05-30 20:31
'''
# Imports
from math import floor
import time
import requests
import requests.utils

# Variables
WEB_BASE = 'https://api.datamarket.azure.com/Bing/Search/Web'
QUERY_TEMPLATE = '?Query={}&Market={}&$top={}&$skip={}&$format=json'

DEFAULT_MARKET = 'en-US'
DEFAULT_SKIP = 0
WEB_QUERY = WEB_BASE + QUERY_TEMPLATE
RESULT_LIMIT = 50
SLEEP_INTERVAL = 1


# Classes
class WebResult(object):
    ''''Result object class that takes converts *results* from JSON to it's
    own object.
    '''
    def __init__(self, result):
        self.url = result['Url']
        self.title = result['Title']
        self.description = result['Description']


# Functions
def quote(text):
    '''Returns quoted *text*.'''
    return requests.utils.quote("'{}'".format(text))


def get_url(query, market, top=RESULT_LIMIT, skip=DEFAULT_SKIP):
    '''Returns the URL to receive data from with the search query of *query*
    and the country as *market* in the page of *skip* / *RESULT_LIMIT* + 1.
    '''
    return WEB_QUERY.format(quote(query), quote(market), top, skip)


def get_objects(url, api_key):
    '''Returns a list of WebResult objects from *url* with the
    authentication of *self.api_key*.
    '''
    json_response = requests.get(url, auth=('', api_key)).json()

    return [WebResult(result) for result in json_response['d']['results']]


def search(query, result_amount, api_key, market=DEFAULT_MARKET):
    '''Returns a list of maximum *result_amount* of objects with the search term of *query*.
    If there are no more results than *result_amount* it returns only the amount of availible
    results.
    '''
    search_results = []

    wanted_result_amount = min(RESULT_LIMIT, result_amount)
    search_url = get_url(query, market, top=wanted_result_amount)
    search_results.extend(get_objects(search_url, api_key)
                          [: wanted_result_amount])

    for iteration in range(floor((result_amount - 1) / RESULT_LIMIT)):
        skip = RESULT_LIMIT * (iteration + 1)
        top = min(RESULT_LIMIT, result_amount - len(search_results))
        search_url = get_url(query, market, top=top, skip=skip)
        print(search_url)

        search_objects = get_objects(search_url, api_key)
        search_results.extend(search_objects)

        if len(search_objects) < RESULT_LIMIT:
            break
        time.sleep(SLEEP_INTERVAL)

    return search_results
