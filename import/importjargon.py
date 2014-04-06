import os
import HTMLParser, urllib, urlparse

class JargonParser(HTMLParser.HTMLParser):
    def __init__ (self):
        HTMLParser.HTMLParser.__init__ (self)
        self.seen = {}
        self.currentSection=''
        self.title = ''
    def handle_data(self, data):
        if self.currentSection is not '':
            if "head" in self.currentSection:
                # store the title
                self.title = data
                print "Title: " + self.title
            else:
                print self.currentSection + ": " + data
    def handle_endtag(self, tag):
        if "head" in self.currentSection or "body" in self.currentSection:
            currentSection = '';
    def handle_starttag(self, tag, attributes):
        if "head" in tag or "body" in tag:
            self.currentSection = tag;
        #print "Tag: " + tag

def jargonReadFile(filename):
    inFile = open(filename)
    buffer = ""
    for line in inFile:
        buffer = buffer + line
    parser = JargonParser()
    parser.feed(buffer)

def jargonImport(rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        for filename in fileList:
            jargonReadFile(dirName + '/' + filename)

if __name__ == "__main__":
    jargonImport('../original')
