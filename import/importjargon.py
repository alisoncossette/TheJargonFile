import os
import HTMLParser, urllib, urlparse

class JargonFile(dict):
   def __init__(self,*arg,**kw):
      super(CustomDictOne, self).__init__(*arg, **kw)

   def __getitem__(self, key):
       val = dict.__getitem__(self, key)
       print 'GET', key
       return val

   def __setitem__(self, key, val):
       print 'SET', key, val
       dict.__setitem__(self, key, val)

   def __repr__(self):
       dictrepr = dict.__repr__(self)
       return '%s(%s)' % (type(self).__name__, dictrepr)

   def update(self, *args, **kwargs):
       print 'update', args, kwargs
       for k, v in dict(*args, **kwargs).iteritems():
           self[k] = v

class JargonParser(HTMLParser.HTMLParser):
    def __init__ (self):
        HTMLParser.HTMLParser.__init__ (self)
        self.seen = {}
        self.currentSection=''
        self.title = ''
        self.bodyText = ''
    def handle_data(self, data):
        if "head" in self.currentSection:
            # store the title
            self.title = data
            self.bodyText = '';
        elif "body" in self.currentSection:
            replacements = ['    ','   ','  ','\t','\r','\n']
            for rep in replacements:
                data = data.replace(rep,' ')
            data = data.strip()
            self.bodyText = self.bodyText + data + ' '
    def handle_starttag(self, tag, attributes):
        if "head" in tag or "body" in tag:
            self.currentSection = tag;

def jargonSaneText(text):
    if len(text) < 2:
        return ''

    initsplit = text.split(' : ')
    if len(initsplit) < 2:
        return ''

    initial = True
    newtext = ''
    for txt in initsplit:
        if not initial:
            newtext = newtext + txt
        initial = False
    text = newtext

    sentsplit = text.split('.')
    if len(sentsplit) > 1:
        ctr = 0
        newtext = ''
        for sent in sentsplit:
            if ctr < len(sentsplit)-1:
                newtext = newtext + sent + '.'
            ctr = ctr + 1
        text = newtext

    text = text.replace(' . ','. ')
    text = text.replace(' .','. ')
    text = text.replace('  ',' ')

    return text.strip()

def jargonReadFile(filename):
    inFile = open(filename)
    buffer = ""
    for line in inFile:
        buffer = buffer + line
    parser = JargonParser()
    parser.feed(buffer)
    if parser.title is not '' and \
       parser.bodyText is not '' and \
       len(parser.title) > 1:
        parser.bodyText = jargonSaneText(parser.bodyText)
        print "Title: " + parser.title
        print "Text: " + parser.bodyText + "\n"

def jargonImport(rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        for filename in fileList:
            jargonReadFile(dirName + '/' + filename)

if __name__ == "__main__":
    jargonImport('../original')
