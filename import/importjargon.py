import os
import HTMLParser

def jargonReadFile(filename):
    inFile = open(filename)
    buffer = ""
    for line in inFile:
        buffer = buffer + line
    parser = HTMLParser.HTMLParser()
    parser.feed(buffer)

def jargonImport(rootDir):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for filename in fileList:
            print('\t%s' % filename)
            jargonReadFile(dirName + '/' + filename)

if __name__ == "__main__":
    jargonImport('original')
