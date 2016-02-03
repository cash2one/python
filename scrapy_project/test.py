#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/29 17:22
# Project:test
# Author:yangmingsong

import scrapy
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        logger.debug(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)
            logger.debug(response.body)
