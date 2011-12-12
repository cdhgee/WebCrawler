#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import sys

def main():
  webcrawler.crawl_url("http://www.aerosonics.com")
  
  
if __name__ == "__main__":
  sys.path.append(os.path.abspath(".."))
  print sys.path
  from webcrawler import WebCrawler as webcrawler
  main()
