#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 4.1.1.6. LoRaTM Packet Structure, SX1276/77/78/79 Datasheet
# http://www.semtech.com/images/datasheet/sx1276_77_78_79.pdf

import math

def mpsrange(a, b):
    '''
    Mac Payload Size range.
    return a list of [a, b], a <= arange(a,b) <= b
    '''
    a += 5  # MHDR + MIC
    b += 6  # MHDR + MIC + 1
    return range(a, b)

def get_toa(n_size, n_sf, n_bw=125, enable_dro=1, disable_h=0, n_cr=1,
            n_preamble=8):
    '''
    return the time on air in milisecond.
    n_size:
        PL in the fomula.  PHY Payload size in byte (= MAC Payload + 5)
    n_sf: SF (12 to 7)
    n_bw: Bandwidth in kHz.  default is 125 kHz for AS923.
    enable_dro:
        DE in the fomula.
        1 when the low data rate optimization is enabled.
        0 for disabled.
        LoRaWAN always use the low data optimization.
    disable_eh:
        H in the fomula.
        0 when the explicit header is enabled.
        1 when no header is present.
        LoRaWAN always use the header.
    n_cr:
        CR in the fomula, should be from 1 to 4.
        Coding Rate = (n_cr/(n_cr+1)).
        LoRaWAN takes alway 1.
    n_preamble:
        The preamble length in bit.
        default is 8 in AS923.
    '''
    t_sym = math.pow(2, n_sf) / (n_bw*1000.) * 1000.
    t_preamble = (n_preamble + 4.25) * t_sym
    a = 8.*n_size - 4.*n_sf + 28 + 16 - 20.*disable_h
    b = 4.*(n_sf-2.*enable_dro)
    v_ceil = a/b
    nb_sym_payload = 8 + max(math.ceil(a/b)*(n_cr+4), 0)
    t_payload = nb_sym_payload * t_sym
    t_frame = t_preamble+ t_payload

    ret = {}
    ret["t_sym"] = t_sym
    ret["t_preamble"] = t_preamble
    ret["v_ceil"] = v_ceil
    ret["nb_sym_payload"] = nb_sym_payload
    ret["t_payload"] = t_payload
    ret["t_frame"] = round(t_frame, 3)

    return ret

if __name__ == "__main__" :
    import sys
    import argparse

    def parse_args():
        p = argparse.ArgumentParser(
                description="LoRa Time on Air calculator.",
                epilog="")
        p.add_argument("n_sf", metavar="SF", type=int,
            help="Spreading Factor. It should be from 7 to 12.")
        p.add_argument("n_size", metavar="SIZE", type=int,
            help="PHY payload size in byte. It's equal to the MAC payload + 5.")
        p.add_argument("--band-width", action="store", dest="n_bw", type=int,
            default=125,
            help="bandwidth in kHz. default is 125 kHz.")
        p.add_argument("--disable-dro", action="store_const", dest="v_de",
            const=0, default=1,
            help="disable the low data rate optimization. default is enable as LoRaWAN does.")
        p.add_argument("--disable-eh", action="store_const", dest="v_h",
            const=1, default=0,
            help="disable the explicit header.  default is enable as LoRaWAN does.")
        p.add_argument("--cr", action="store", dest="n_cr", type=int, default=1,
            help="specify the CR value. default is 1 as LoRaWAN does.")
        p.add_argument("--preamble", action="store", dest="n_preamble",
            type=int, default=8,
            help="specify the preamble. default is 8 for AS923.")
        p.add_argument("-v", action="store_true", dest="f_verbose",
            default=False,
            help="enable verbose mode.")
        p.add_argument("-d", action="append_const", dest="_f_debug", default=[],
            const=1, help="increase debug mode.")
    
        args = p.parse_args()
        args.debug_level = len(args._f_debug)
        return args

    #
    # main
    #
    opt = parse_args()
    ret = get_toa(opt.n_size, opt.n_sf, n_bw=opt.n_bw, enable_dro=opt.v_de,
                  disable_h=opt.v_h, n_cr=opt.n_cr, n_preamble=opt.n_preamble)
    ret0 = get_toa(0, opt.n_sf, n_bw=opt.n_bw, enable_dro=opt.v_de,
                   disable_h=opt.v_h, n_cr=opt.n_cr, n_preamble=opt.n_preamble)
    if opt.f_verbose:
        print "PHY payload size    : %d Bytes" % opt.n_size
        print "MAC payload size    : %d Bytes" % (opt.n_size-5)
        print "Spreading Factor    : %d" % opt.n_sf
        print "Band width          : %d kHz" % opt.n_bw
        print "Low data rate opt.  : %s" % ("enable" if opt.v_de else "disable")
        print "Explicit header     : %s" % ("disable" if opt.v_h else "enable")
        print "CR (coding rate)    : %d (4/%d)" % (opt.n_cr, 4+opt.n_cr)
        print "Preamble size       : %d symbols" % opt.n_preamble
        print "Other symbol size   : %d symbols" % ret["nb_sym_payload"]
        print "Symbol Time         : %.3f msec" % ret["t_sym"]
        print "Preamble ToA        : %.3f msec" % ret["t_preamble"]
        print "Payload ToA         : %.3f msec" % ret["t_payload"]
        print "Time on Air         : %.3f msec" % ret["t_frame"]
        if opt.debug_level:
            print "MAC frame data rate : %.3f bps" % ((8.*(opt.n_size-5)) /
                                    ((ret["t_frame"]-ret0["t_frame"])/1000.))
            print "Ceil(x)             : %.3f" % ret["v_ceil"]
    else:
        print "%.3f" % ret["t_frame"]
