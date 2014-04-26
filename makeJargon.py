import os
import string
import operator

def jargonParseEntry(filename):
    if not os.path.isfile(filename):
        return []

    entry = []

    line = []
    with open(filename) as fp:
        line = fp.readlines()
    fp.close()

    text = ''
    if len(line) > 2:
        for i in range(len(line)):
            if i == 0:
                entry.append(line[i].replace('\n','').strip())
            if i >= 2:
                text = text + line[i]
    text = text.replace('\n',' ')
    entry.append(text.strip())

    return entry

# returns the number of sub-definitions within a description
def jargonSubdefinitions(text):
    definitions = 0
    prevpos = 0
    for i in range(10):
        definitionStr = str(i+1) + ". "
        pos = text.find(definitionStr)
        if pos == -1 or pos < prevpos:
            break
        else:
            definitions = definitions + 1
            prevpos = pos

    if definitions == 0:
        definitions = 1

    # too many definitions
    if definitions > 5:
        definitions  = 0

    return definitions

def jargonGetEntries(entriesDir):
    entries = []
    for dirName, subdirList, fileList in os.walk(entriesDir):
        for filename in fileList:
            entry = jargonParseEntry(entriesDir + '/' + filename)
            if entry:
                entries.append(entry)
    entries.sort(key=operator.itemgetter(0))
    return entries

def jargonManpageWithDefinitions(text, definitions):
    result = ''
    prevpos = 0
    for i in range(definitions):
        pos = text.find(str(i+1) + ". ")
        if pos > -1 and i > 0:
            if result != '':
                result = result + "\n\n"
            result = result + text[prevpos:pos]
        prevpos = pos
    return result + "\n\n" + text[prevpos:]

def jargonToManpage(manpageFilename, entries, version):
    if not os.path.isdir("man"):
        os.system("mkdir man")

    if os.path.isfile(manpageFilename + ".gz"):
        os.system("rm " + manpageFilename + ".gz")

    fp = open(manpageFilename,'w')

    fp.write(".TH \"The Jargon File\" 1 \"April 26, 2014\" \"\" \"" + version + "\"\n\n")

    for entry in entries:
        title = entry[0]
        text = entry[1]
        definitions = jargonSubdefinitions(entry[1])
        if definitions > 1:
            text = jargonManpageWithDefinitions(text, definitions)

        fp.write(".SH " + title + "\n")
        fp.write(text + "\n\n")

    fp.close()

    os.system("gzip " + manpageFilename)
    print "manpage can be installed with the command:"
    print "sudo install -m 644 " + manpageFilename + ".gz /usr/local/share/man/man1"

if __name__ == "__main__":
    version = "x.xx"
    entries = jargonGetEntries('entries')
    jargonToManpage("man/jargon.1", entries, version)
