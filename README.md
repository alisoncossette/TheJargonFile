The Jargon File
===============

Originally created by [Raphael Finkel](http://www.cs.uky.edu/~raphael/), _The Jargon File_ is a list of slang terms used by computer programmers. In recent years the file has fallen into disrepair and much of the language has become dated or irrelevant as fashions, technologies and memes have changed.

I encourage readers to reclaim _The Jargon File_ and make changes, additions or deletions as they see fit.  All vaguely sensible pull requests will be considered.

For readability within a Git repository all entries should be plain ASCII text with a maximum of 78 characters across.

This version of _The Jargon File_ was based upon [version 4.4.7 maintained by Eric S. Raymond](http://www.catb.org/jargon/). It was originally imported from HTML via the _importJargon.py_ script within the _import_ subdirectory.

Converting to other formats
---------------------------

As a Git repository the file isn't all that useful.  You can export it in other formats as follows:

```bash
python makeJargon.py
```
To install the manpage:

```bash
sudo install -m 644 docs/jargon.1.gz /usr/local/share/man/man1
```

The org-mode formatted docuemnt can be found in _docs/jargon-org.txt_
