#!/usr/bin/env python

from parser import DmozParser

# This is a really simple python implementation of the Dmoz RDF parser. 
# This parser makes the assumption is the last entity in each dmoz page is topic:
# <ExternalPage about="http://www.awn.com/">
#   <d:Title>Animation World Network</d:Title>
#   <d:Description>Provides information resources to the international animation community. Features include searchable database archives, monthly magazine, web animation guide, the Animation Village, discussion forums and other useful resources.</d:Description>
#   <priority>1</priority>
#   <topic>Top/Arts/Animation</topic>
# </ExternalPage>
# This assumption is strictly checked, and processing will abort if it is violated.
# To use this parser, one should unpack the content.rdf.u8.gz first

class Filter:
  def __init__(self):
    self._file = open("seeds.txt", 'w')

  def page(self, page, content):
      if page != None and page != "":
          topic = content['topic']
          with open("category.txt") as f:
                ctg = f.readline().strip()
          if topic.find(ctg) > 0 :
              self._file.write(page + "\n")
              print "found page %s in topic %s" % (page , topic)

  def finish(self):
    self._file.close()


parser = DmozParser()
parser.add_handler(
    Filter()
)
parser.run()
