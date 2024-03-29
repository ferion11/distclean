#!/usr/bin/env python
## distclean.py version 0.4 (16 Jan 2012)
##
## Removes source files for Gentoo
## packages that are no longer installed
## Use with '-p' (pretend) flag to just get a list of files
## that would be removed
##
## 0.1: Aug 20, 2003 - first version with version number
## 0.2: Jan 11, 2005 - fixes by Emil Beinroth
## 0.3: Jan 04, 2009 - portage API changed, fixed by Jan Narovec
## 0.4: Feb 16, 2012 - change for python3 work, fixed by Daniel Ribeiro (aka danielbr OR ferion11)
##
## Copyright (c) 2003, Fredrik Arnerup (e97_far@e.kth.se)
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##
##   * Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in the
##     documentation and/or other materials provided with the distribution.
##
## THIS SOFTWARE IS PROVIDED BY FREDRIK ARNERUP "AS IS" AND ANY
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
## FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
## DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
## CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
## LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
## OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
## DAMAGE.

import sys, os, os.path, getopt, portage

opt_p = 0
try:
    if len(sys.argv) > 1:
        opt_p = getopt.getopt(sys.argv[1:], 'p')[0][0][0] == '-p'
except getopt.GetoptError:
    pass

distdir = portage.settings['DISTDIR']
print ('DISTDIR =', distdir)
    
vartree = portage.db['/']['vartree']
packages = []
for name in vartree.getallnodes():
    packages.extend(vartree.dep_match(name))

files = {}
for package in packages:
    try:
        package_files = portage.portdb.getFetchMap(package).keys()
        for filename in package_files:
            files[filename] = 1
    except:
        print ('Failed to get file list for', package)

if not files:
    sys.exit("No package files found.  This can't be right.\n")

try:
    list = portage.listdir(distdir)
except os.OSError:
    sys.exit('Failed to read ' + distdir)

size = 0; count = 0
for file in list:
    abs_file = distdir + '/' + file
    if (os.path.isfile(abs_file) and (not os.path.islink(abs_file)) 
        and (not file in files)):
        size += os.stat(abs_file).st_size
        count += 1
        if opt_p:
            print ('Would remove', abs_file)
        else:
            try:
                os.remove(abs_file)
                print ('Removed', abs_file)
            except OSError:
                print ('Failed to remove', abs_file)


size /= 1048576  ## MB
print ( '%i files, total size: %i MB' % (count, size) )
