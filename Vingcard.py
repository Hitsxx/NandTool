#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
##                                                                         ##
## This file is proposed as is                                             ##
##                                                                         ##
##  Author: Jean-Michel Picod                                              ##
##                                                                         ##
## This program is distributed under GPLv3 licence                         ##
##                                                                         ##
#############################################################################

from scapy.all import *


class MifareSerial(Packet):
    fields_desc=[
        ByteEnumField("manufacturer", 4, {0x04: "NXP"}),
        XShortField("serial1", 0),
        XByteField("check0", 0),
        XIntField("serial2", 0),
        XByteField("check1", 0)
    ]

    def i2repr(self, pkt):
        return pkt.manufacturer + pkt.serial1 + pkt.serial2
        

class MifareUltralight(Packet):
    fields_desc=[
        MifareSerial,
        ByteField("internal", 0),
        XShortField("lockbytes", 0),
        XIntField("otp_bytes", 0)
    ]


class VingcardProtected(Packet):
    fields_desc=[
        XByteField("xor_key", 0),
        XByteField("magic", 0x90),
        X3BytesField("hotel_id", 0),
        XByteField("key_type", 0x82),
        XIntField("key_id", 0),
        XIntField("duration", 0),
        X3BytesField("room_id", 0),
        XByteField("unk1", 0),
        XShortField("const1", 0xFF00),
        XIntField("unk2", 0)
    ]

    def pre_dissect(self, s):
        k = ord(s[0])
        return s[0] + "".join([chr(k ^ ord(x)) for x in s[1:]])

    def post_build(self, p, pay):
        k = ord(p[0])
        return p[0] + "".join([chr(k ^ ord(x)) for x in p[1:]]) + "".join([chr(k ^ ord(x)) for x in pay])


class Vingcard(Packet):
    fields_desc=[
        MifareUltralight,
        ByteField("magic", 6),
        FieldLenField("header_length", None, length_of="unknown", fmt="B"),
        FieldLenField("payload_length", None, length_of="protected_data", fmt="H"),
        StrLenField("unknown", "", length_from=lambda pkt: pkt.header_length - 4),
        PacketLenField("protected_data", None, VingcardProtected, length_from=lambda pkt: pkt.payload_length),
        ByteField("unk", 0),
        XIntField("checksum", None)
    ]


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument('dump', metavar="FILE", nargs=1, type=argparse.FileType('rb'))
    args = parser.parse_args(sys.argv[1:])
    try:
        Vingcard(args.dump[0].read()).show2()
    except:
        print >> sys.stderr, "Input file does not seem to be a valid Vingcard dump"
    finally:
        args.dump[0].close()
    sys.exit(0)

# vim:ts=4:expandtab:sw=4

