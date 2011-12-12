#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing
from CrawlerWorker import CrawlerWorker


class WebCrawler(object):
  
  def __init__(self, base_url):
    #multiprocessing.Process.__init__(self)
    self.base_url = base_url
    
  def run(self):

    urls_in = multiprocessing.JoinableQueue()
    mgr = multiprocessing.Manager()
    processed = mgr.list()
  
    try:
      urls_in.put(self.base_url)
      self.crawlers = []
      for i in xrange(4):
        c = CrawlerWorker(self.base_url, urls_in, processed)
        c.start()
        self.crawlers.append(c)
      urls_in.join()
      for u in sorted(processed):
        print u

    except KeyboardInterrupt:
      for c in self.crawlers:
        c.terminate()

"""def summarize(urllist, fn):
  print "%d total URLs." % len(urllist)
  x = codecs.open("%s.txt" % fn, "w", "utf-8")
  x.write("\n".join(sorted(urllist)))
  x.close()"""
  
def crawl_url(url):
  wc = WebCrawler(url)
  wc.run()
  #wc.join()


