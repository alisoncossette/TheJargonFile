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
    if definitions > 8:
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

def jargonWithDefinitions(text, definitions, isHtml):
    result = ''
    prevpos = 0
    for i in range(definitions):
        pos = text.find(str(i+1) + ". ")
        if pos > -1 and i > 0:
            if result != '':
                result = result + "\n\n"

            if not isHtml:
                result = result + text[prevpos:pos]
            else:
                result = result + "<p>" + text[prevpos:pos] + "</p>"

        prevpos = pos

    if not isHtml:
        result = result + "\n\n" + text[prevpos:]
    else:
        result = result + "\n\n" + "<p>" + text[prevpos:] + "</p>"
    return result

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
            text = jargonWithDefinitions(text, definitions, False)

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

    fp.write("#+TITLE: The Jargon File\n")
    fp.write("#+VERSION " + version + "\n")
    fp.write("#+OPTIONS: ^:nil\n")
    fp.write("#+STYLE: <link rel=\"stylesheet\" type=\"text/css\" href=\"index.css\" />\n\n")

    fp.write("#+BEGIN_CENTER\n")
    fp.write("*Yet more Jargon*\n")
    fp.write("#+END_CENTER\n\n")

    fp.write("* License\n\n")
    saveLicense(fp, year, publishername)

    fp.write("* Glossary\n")

    subsection = ''
    for entry in entries:
        title = entry[0]
        text = entry[1]
        definitions = jargonSubdefinitions(entry[1])
        if definitions > 1:
            text = jargonWithDefinitions(text, definitions, False)

        if title[0:1] != subsection:
            subsection = title[0:1]
            fp.write("** " + subsection.upper() + "\n")

        fp.write("*** " + title + "\n")
        fp.write(text + "\n\n")
    fp.close()


def jargonToHTML(htmlFilename, entries, version, publishername):
    year = int(time.strftime("%Y"))

    if not os.path.isdir("docs"):
        os.system("mkdir docs")

    if os.path.isfile(htmlFilename):
        os.system("rm " + htmlFilename)

    fp = open(htmlFilename,'w')

    fp.write("<!DOCTYPE html>\n")
    fp.write("<html>\n")
    fp.write("  <head>\n")
    fp.write("    <title>The Jargon File</title>\n")
    fp.write("  </head>\n")
    fp.write("  <body>\n")
    fp.write("    <H1>The Jargon File</H1>\n")
    fp.write("      <H2>License</H2>\n")
    fp.write("      <p>\n")
    saveLicense(fp, year, publishername)
    fp.write("      </p>\n")
    fp.write("      <H2>Glossary</H2>\n")

    subsection = ''
    for entry in entries:
        title = entry[0]
        text = entry[1]

        if title[0:1] != subsection:
            subsection = title[0:1]
            fp.write("        <H3>" + subsection.upper() + "</H3>\n")

        fp.write("        <H4>" + title + "</H4>\n")

        definitions = jargonSubdefinitions(entry[1])
        if definitions > 1:
            text = jargonWithDefinitions(text, definitions, True)
            fp.write("        " + text + "\n")
        else:
            fp.write("        <p>\n")
            fp.write("        " + text + "\n")
            fp.write("        </p>\n")

    fp.write("  </body>\n");
    fp.write("</html>\n")
    fp.close()

if __name__ == "__main__":
    version = "x.xx"
    publishername = "My Name"
    entries = jargonGetEntries('entries')
    jargonToManpage("docs/jargon.1", entries, version, publishername)
    jargonToOrgMode("docs/jargon-org.txt", entries, version, publishername)
    jargonToHTML("docs/jargon.html", entries, version, publishername)
