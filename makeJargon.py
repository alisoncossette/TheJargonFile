import os
import string
import operator
import time

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

    # remove any gaps
    pos = text.find('  ')
    while pos != -1:
        text = text.replace('  ',' ')
        pos = text.find('  ')

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

# saves the license details
def saveLicense(fp, year, publishername):
    fp.write("Copyright (c)  " + str(year) + "  " + publishername + "\n")
    fp.write("Permission is granted to copy, distribute and/or modify this document\n")
    fp.write("under the terms of the GNU Free Documentation License, Version 1.3\n")
    fp.write("or any later version published by the Free Software Foundation;\n")
    fp.write("with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.\n")
    fp.write("A copy of the license is included in the section entitled \"GNU\n")
    fp.write("Free Documentation License\".\n\n")

def jargonWithDefinitions(text, definitions):
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

def jargonToManpage(manpageFilename, entries, version, publishername):
    year = int(time.strftime("%Y"))

    if not os.path.isdir("docs"):
        os.system("mkdir docs")

    if os.path.isfile(manpageFilename + ".gz"):
        os.system("rm " + manpageFilename + ".gz")

    fp = open(manpageFilename,'w')

    fp.write(".TH \"The Jargon File\" 1 \"" + time.strftime("%x") + \
             "\" \"\" \"" + version + "\"\n\n")

    fp.write(".SH LICENSE\n\n")
    saveLicense(fp, year, publishername)

    for entry in entries:
        title = entry[0]
        text = entry[1]
        definitions = jargonSubdefinitions(entry[1])
        if definitions > 1:
            text = jargonWithDefinitions(text, definitions)

        fp.write(".SH " + title + "\n")
        fp.write(text + "\n\n")

    fp.close()

    os.system("gzip " + manpageFilename)
    print "manpage can be installed with the command:"
    print "sudo install -m 644 " + manpageFilename + ".gz /usr/local/share/man/man1"

def jargonToOrgMode(orgFilename, entries, version, publishername):
    year = int(time.strftime("%Y"))

    if not os.path.isdir("docs"):
        os.system("mkdir docs")

    if os.path.isfile(orgFilename):
        os.system("rm " + orgFilename)

    fp = open(orgFilename,'w')

    fp.write("#+TITLE: The Jaqrgon File\n")
    fp.write("#+VERSION " + version + "\n")
    fp.write("#+OPTIONS: ^:nil\n")
    fp.write("#+STYLE: <link rel=\"stylesheet\" type=\"text/css\" href=\"index.css\" />\n\n")

    fp.write("#+BEGIN_CENTER\n")
    fp.write("*Yet more Jargon*\n")
    fp.write("#+END_CENTER\n\n")

    fp.write("* License\n\n")
    saveLicense(fp, year, publishername)

    fp.write("* Glossary\n")

    for entry in entries:
        title = entry[0]
        text = entry[1]
        definitions = jargonSubdefinitions(entry[1])
        if definitions > 1:
            text = jargonWithDefinitions(text, definitions)

        fp.write("** " + title + "\n")
        fp.write(text + "\n\n")
    fp.close()


if __name__ == "__main__":
    version = "x.xx"
    publishername = "My Name"
    entries = jargonGetEntries('entries')
    jargonToManpage("docs/jargon.1", entries, version, publishername)
    jargonToOrgMode("docs/jargon-org.txt", entries, version, publishername)
