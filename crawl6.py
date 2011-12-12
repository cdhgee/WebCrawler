#!/usr/bin/python
# -*- coding: utf-8 -*-

#from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse
import codecs
import sys
import multiprocessing
import Queue
import logging
import lxml.html

class Crawler(multiprocessing.Process):

  def __init__(self, base_url, urls_in, processed, logger):
    multiprocessing.Process.__init__(self)
    self.base_url = urlparse.urlsplit(base_url)
    self.urls_in = urls_in
    self.processed = processed
    self.logger = logger

  def run(self):
    while True:
      try:
        u = self.urls_in.get(True, 5)
        try:
          uo = urllib2.urlopen(u)
          if uo.info().gettype() == "text/html":
            self.logger.debug("processing %s", u)
            tree = lxml.html.parse(uo)
            tags = tree.xpath("//a")
            #soup = BeautifulSoup(uo.read())
            #tags = soup.findAll("a")

            for t in tags:
              tval = t.get("href")
              #for (tname, tval) in t.attrs:
              #  if tname == "href":
              new_url = urlparse.urldefrag(urlparse.urljoin(u, tval).lower())[0]
              if new_url not in self.processed and self.validate(new_url):
                self.logger.debug("validated ok: %s", new_url)
                self.urls_in.put(new_url)
                self.processed.append(new_url)

          self.urls_in.task_done()
        except urllib2.HTTPError:
          pass
        except UnicodeEncodeError:
          pass
        except urllib2.URLError:
          pass
      except Queue.Empty:
        break

  def validate(self, url):
    v = urlparse.urlsplit(url)
    return self.base_url.scheme == v.scheme and self.base_url.netloc == v.netloc and v.path[-3:].lower() != 'jpg'

def main():
  logger = multiprocessing.log_to_stderr()
  base_url = sys.argv[1]
  logger.debug("base_url is %s", base_url)

  urls_in = multiprocessing.JoinableQueue()
  mgr = multiprocessing.Manager()
  processed = mgr.list()
  #all_urls = mgr.list()

  try:
    urls_in.put(base_url)
    crawlers = []
    for i in xrange(4):
      c = Crawler(base_url, urls_in, processed, logger)
      c.start()
      crawlers.append(c)
    urls_in.join()
    for u in sorted(processed):
      print u


  except KeyboardInterrupt:
    pass

  #summarize(processed, "smiths-medical-urls")
  #summarize(all_urls, "smiths-medical-all_urls")

def summarize(urllist, fn):
  print "%d total URLs." % len(urllist)
  x = codecs.open("%s.txt" % fn, "w", "utf-8")
  x.write("\n".join(sorted(urllist)))
  x.close()


if __name__ == "__main__":
  main()
