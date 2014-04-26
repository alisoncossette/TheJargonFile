import os
import string
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
            self.title = data.strip()
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

# Further sanitise the returned text
def jargonSaneText(title, text):
    if len(text) < 2:
        return ''

    # usually in the format (title : text)
    initsplit = text.split(' : ')
    if len(initsplit) < 2:
       # sometimes in the format (title[blurb] text)
       initsplit = text.split('] ')
       if len(initsplit) < 2:
          # sometimes in the format (title adj. text)
          initsplit = text.split(' adj. ')

    # is all else fails look for the second instance of the title text
    if len(initsplit) < 2:
       testsplit = text.split(title)
       if len(testsplit) >= 3:
          initsplit = testsplit
          initsplit[1] = ''
          testsplitctr = 0
          for txt in testsplit:
             if txt == ' ':
                txt = title
             if testsplitctr >= 2:
                if testsplitctr >= 3:
                   initsplit[1] = initsplit[1] + ' '
                initsplit[1] = initsplit[1] + txt
             testsplitctr = testsplitctr + 1

    if len(initsplit) < 2:
       return ''

    # get the second part of the split array (i.e. the description text)
    text = initsplit[1]

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
    text = filter(lambda x: x in string.printable, text)

    return text.strip()

def validTitle(title):
   if title is '':
      return False

   if '\xc2' in title:
      return False

   if title.startswith("Letters"):
      return False

   if title.startswith("Comments"):
      return False

   if title.startswith("Glossary"):
      return False

   return True

# remove any invalid characters from an entry title
# so thst it can be saved in a filename
def jargonSaneTitle(title):
   if '/' in title:
      title = title.replace('/','-')
   return title

def jargonCreateEntry(title, text, outputDir):
   # create the filename for the entry
   filename = outputDir
   if not outputDir.endswith('/'):
      filename = filename + '/'
   filename = filename + jargonSaneTitle(title) + '.txt'

   # don't overwrite existing files
   if os.path.isfile(filename):
      return ''

   fp = open(filename, 'w')
   fp.write(title + '\n\n' + text + '\n')
   fp.close
   return filename

def jargonReadFile(filename, exclusions, outputDir):
    inFile = open(filename)
    buffer = ""
    for line in inFile:
        buffer = buffer + line
    parser = JargonParser()
    parser.feed(buffer)
    if validTitle(parser.title) and \
       parser.bodyText is not '' and \
       len(parser.title) > 1:
       saneBodyText = jargonSaneText(parser.title, parser.bodyText)
       if not ((jargonSaneTitle(parser.title) in exclusions) or \
               (parser.title in exclusions)):
          entryFilename = jargonCreateEntry(parser.title, saneBodyText, outputDir)
          if entryFilename is not '':
             print entryFilename

# read original jargon file entries to be excluded
def jargonReadExclusions(filename):
   if len(filename) == 0:
      return []

   if not os.path.isfile(filename):
      return []

   exclusions = []
   with open(filename) as fp:
      exclusions = fp.readlines()
   fp.close()

   tempExclusions = []
   for i in range(len(exclusions)):
      tempExclusions.append(exclusions[i].strip('\n'))
   exclusions = tempExclusions

   return exclusions

def jargonImport(rootDir, excludeEntriesFilename, outputDir):
   exclusions = jargonReadExclusions(excludeEntriesFilename)

   print exclusions

   for dirName, subdirList, fileList in os.walk(rootDir):
      for filename in fileList:
         jargonReadFile(dirName + '/' + filename, exclusions, outputDir)

if __name__ == "__main__":
   jargonImport('../original','exclusions.txt','../entries')
