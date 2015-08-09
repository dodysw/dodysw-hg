# Introduction #

A set of small utilities wrote mainly in Python to maintain my file systems.

# File System Utilities #

  * [filesplitterbyline](http://code.google.com/p/dodysw-hg/source/browse/ShellUtilities/filesplitbyline.py): python script to split a file into max n KB chunks, while preserving the line (split at eol), optionally bzipped the chunks. 2011.
  * [Find shuttercount](http://code.google.com/p/dodysw/source/browse/trunk/find_shuttercount/find_shuttercount.py): output photo's date and shutter count register (Canon camera only) to give early hint on how close your camera to reaching manufacturer's claimed shutter life, and timeline on how you spend those precious shutters. 2008.
  * [photo group](http://code.google.com/p/dodysw/source/browse/trunk/photogroup/photogroup.py): move your photos into yearly folders based on exif date of taken but preserve their parent folder structure. E.g. I have photos in Newyear/`*`.jpg, Birthday/`*`.jpg, they will be moved to 2008/Newyear/`*`.jpg, 2009/Newyear/`*`.jpg, 2009/Birthday/`*`.jpg, etc. 2008.
  * [filesplitter](http://code.google.com/p/dodysw/source/browse/trunk/filesplitter/filesplitter.py): efficiently split  arbitrarily large file into x number of smaller files. 2007.
  * [WinRipAttachment](http://code.google.com/p/dodysw/source/browse/trunk/ripattachment/pyripattachment.py): gui app that parse .msg/.eml email files and extract all multipart mime attachments into another place. 2005.
  * [change indent](http://code.google.com/p/dodysw/source/browse/trunk/changeindent/changeindent.py): fix python file indentation mixed-up, and optionally change to x number of spaces. 2004.
  * [pyDedupe](http://code.google.com/p/dodysw/source/browse/trunk/pydedupe/pydedupe.py): dual mode (console, and gui) script to scan through directories recursively to detect and optionally remove duplicate files. 2004.
  * [pyFileSearchReplace](http://code.google.com/p/dodysw/source/browse/trunk/pyfilesearchreplace/pyFileSearchReplace.py): recursively search and optionally replace a string inside files in specified directories. 2004.
  * [pytreesize](http://code.google.com/p/dodysw/source/browse/trunk/pytreesize/pytreesize.py): recursively iterate all files and directory's size, in similar way to linux du (disk usage), but run everywhere python run. 2004.
  * [getyahoogroups](http://code.google.com/p/dodysw/source/browse/trunk/web_utils/getyahoogroups/getyahoogroups.py): output what yahoogroups mailing list each mailbox files contain for [The Bat!](http://www.ritlabs.com/en/products/thebat/) (background: I used to subscribed to a lot of mailing list, and storage restriction forces me to frequently archive old mailing lists to CD. 2003.
  * [mailclientparser](http://code.google.com/p/dodysw/source/browse/trunk/web_utils/mailclient_parser/mailclientparser.py): analyze mailbox file for statistics on email client user agents. 2003.