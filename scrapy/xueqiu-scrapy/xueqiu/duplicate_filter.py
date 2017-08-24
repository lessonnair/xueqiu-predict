#!/usr/bin/python 
#encoding: utf-8

import os

from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from weiboCrawler.parsetool import ParseTool

class CustomFilter(RFPDupeFilter):
    def __getid(self, url):
        tool = ParseTool()
        mm = tool.parse_uid(url)
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)