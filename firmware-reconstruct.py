#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#############################################################################
##                                                                         ##
## This file is proposed as is                                             ##
##                                                                         ##
##                                                                         ##
## Copyright (C) 2010, 2011 Cassidian SAS. All rights reserved.            ##
## This document is the property of Cassidian SAS, it may not be copied or ##
## circulated without prior licence                                        ##
##                                                                         ##
##  Author: Jean-Michel Picod <jean-michel.picod@cassidian.com>            ##
##                                                                         ##
## This program is distributed under GPLv3 licence                         ##
##                                                                         ##
#############################################################################


import argparse
import sys
from collections import Counter


def rebuild_file(out_file, in_files, chunk_size=1024):
    while True:
        in_data = [x.read(chunk_size) for x in in_files]
        if all([len(x) == 0 for x in in_data]):
            break
        out_data = []
        for byte_offset in xrange(len(in_data[0])):
            c = Counter([x[byte_offset] for x in in_data])
            elected = c.most_common(2)
            if len(elected) == 2 and elected[0][1] == elected[1][1]:
                print "Warning: ex-aequo candidates detected '0x%02x' (%d) and '0x%02x' (%d)" % (ord(elected[0][0]),
                                                                                                 elected[0][1],
                                                                                                 ord(elected[1][0]),
                                                                                                 elected[1][1])
                print "\tArbitrary choosing '0x%02x'" % ord(elected[0][0])
            out_data.append(c.most_common(1)[0][0])
        out_file.write("".join(out_data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('infiles', metavar="INFILE", nargs='+', help="Input files", type=argparse.FileType('rb'))
    parser.add_argument('-o', '--output', dest='outfile', metavar='OUTFILE', help='Destination of the rebuilt image',
                        required=True, type=argparse.FileType('wb'))

    args = parser.parse_args(sys.argv[1:])
    rebuild_file(args.outfile, args.infiles)
    [x.close() for x in args.infiles]
    args.outfile.close()

# vim:ts=4:expandtab:sw=4

