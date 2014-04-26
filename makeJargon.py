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

def jargonGetEntries(entriesDir):
    entries = []
    for dirName, subdirList, fileList in os.walk(entriesDir):
        for filename in fileList:
            entry = jargonParseEntry(entriesDir + '/' + filename)
            if entry:
                entries.append(entry)
    entries.sort(key=operator.itemgetter(0))
    return entries

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
