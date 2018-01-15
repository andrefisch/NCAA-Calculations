from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

from lxml import html
from flask import Flask, render_template
from io import BytesIO
import requests
import pandas
import operator
import random

import scraping_service as ScrapingService


ESCRIME_RESULTS_2017_URL = "https://escrimeresults.com/NCAA/ncaa2017.html"


def get_current_results():
    school_map = _get_school_mappings()
    school_fencers_map = _get_school_fencers_map()

    content = _get_page_content(url=ESCRIME_RESULTS_2017_URL)

    remaining_bout_data = ScrapingService.scrape_site_content_for_bout_data(
        content=content,
        school_map=school_map,
        school_fencers_map=school_fencers_map)

    return remaining_bout_data


def _get_school_mappings():
    school_map = {}

    with open("./static/text/schoolDict.txt") as f:
        for line in f:
            (key, val) = line.strip('\n').split(";")
            school_map[key] = val

    return school_map


def _get_school_fencers_map():
    school_fencers_map = {}

    with open("./static/text/totalFencers.txt") as f:
        for line in f:
            (key, val) = line.strip('\n').split(";")
            school_fencers_map[key] = val

    return school_fencers_map


def _get_page_content(url):
    s = requests.Session()
    s.mount('https://', MyAdapter())
    page = s.get(url)

    return pandas.read_html(page.content)
