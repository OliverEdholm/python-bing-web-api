#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Bing web search

This module searches Bing web and returns results with the attributes...
* url  -The URL to access the result.
* title  -The results title.
* description  -The description of the result.

You need a Bing search API key to be able to search with Bing.

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
WEB_QUERY = WEB_BASE + QUERY_TEMPLATE

RESULT_LIMIT = 50


# Classes
class WebResult(object):
    ''''Result object class that takes converts *results* from JSON to it's
    own object.
    '''
    def __init__(self, result):
        self.url = result['Url']
        self.title = result['Title']
        self.description = result['Description']


class BingWebSearch():
    '''Bing Web Search class for searching Bing web with *api_key* and the
    country *market*.
    '''
    def __init__(self, api_key, market='en-US', sleep_interval=1):
        self.api_key = api_key
        self.market = market
        self.sleep_interval = sleep_interval

    def _quote(self, text):
        '''Returns quoted *text*.'''
        return requests.utils.quote("'{}'".format(text))

    def _get_url(self, query, market, top=RESULT_LIMIT, skip=0):
        '''Returns the URL to receive data from with the search query of *query*
        and the country as *market* in the page of *skip* / *RESULT_LIMIT* + 1.
        '''
        return WEB_QUERY.format(self._quote(query), self._quote(market), top, skip)

    def _get_objects(self, url, api_key):
        '''Returns a list of WebResult objects from *url* with the
        authentication of *self.api_key*.
        '''
        json_response = requests.get(url, auth=('', api_key)).json()

        return [WebResult(result) for result in json_response['d']['results']]

    def search(self, query, result_amount):
        '''Returns a list of maximum *result_amount* of objects with the search term of *query*.
        If there are no more results than *result_amount* it returns only the amount of availible
        results.
        '''
        search_results = []

        wanted_result_amount = min(RESULT_LIMIT, result_amount)
        search_url = self._get_url(query, self.market, top=wanted_result_amount)
        search_results.extend(self._get_objects(search_url, self.api_key)
                              [: wanted_result_amount])

        for iteration in range(floor((result_amount - 1) / RESULT_LIMIT)):
            skip = RESULT_LIMIT * (iteration + 1)
            top = min(RESULT_LIMIT, result_amount - len(search_results))
            search_url = self._get_url(query, self.market, top=top, skip=skip)

            search_objects = self._get_objects(search_url, self.api_key)
            search_results.extend(search_objects)

            if len(search_objects) < RESULT_LIMIT:  # If no more availible results
                break
            time.sleep(self.sleep_interval)

        return search_results
