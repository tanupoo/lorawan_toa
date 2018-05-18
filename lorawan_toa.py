#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 4.1.1.6. LoRaTM Packet Structure, SX1276/77/78/79 Datasheet Rev.5 Aug 2016
# http://www.semtech.com/images/datasheet/sx1276.pdf

import math

def mpsrange(a, b):
    '''
    Mac Payload Size range.
    return a list of [a, b], a <= arange(a,b) <= b
    '''
    a += 5  # MHDR + MIC
    b += 6  # MHDR + MIC + 1
    return range(a, b)

def get_toa(n_size, n_sf, n_bw=125, enable_auto_ldro=True, enable_ldro=False,
            enable_eh=True, enable_crc=True, n_cr=1, n_preamble=8):
    '''
    Parameters:
        n_size:
            PL in the fomula.  PHY Payload size in byte (= MAC Payload + 5)
        n_sf: SF (12 to 7)
        n_bw: Bandwidth in kHz.  default is 125 kHz for AS923.
        enable_auto_ldro
            flag whether the auto Low Data Rate Optimization is enabled or not.
            default is True.
        enable_ldro:
            if enable_auto_ldro is disabled, LDRO is disable by default,
            which means that DE in the fomula is going to be 0.
            When enable_ldro is set to True, DE is going to be 1.
            LoRaWAN specification does not specify the usage.
            SX1276 datasheet reuiqres to enable LDRO
            when the symbol duration exceeds 16ms.
        enable_eh:
            when enable_eh is set to False, IH in the fomula is going to be 1.
            default is True, which means IH is 0.
            LoRaWAN always enables the explicit header.
        enable_crc:
            when enable_crc is set to False, CRC in the fomula is going to be 0.
            The downlink stream doesn't use the CRC in the LoRaWAN spec.
            default is True to calculate ToA for the uplink stream.
        n_cr:
            CR in the fomula, should be from 1 to 4.
            Coding Rate = (n_cr/(n_cr+1)).
            LoRaWAN takes alway 1.
        n_preamble:
            The preamble length in bit.
            default is 8 in AS923.
    Return:
        dict type contains below:
        r_sym: symbol rate in *second*
        t_sym: the time on air in millisecond*.
        t_preamble:
        v_ceil:
        symbol_size_payload:
        t_payload:
        t_packet: the time on air in *milisecond*.
    '''
    r_sym = (n_bw*1000.) / math.pow(2,n_sf)
    t_sym = 1000. / r_sym
    t_preamble = (n_preamble + 4.25) * t_sym
    # LDRO
    v_DE = 0
    if enable_auto_ldro:
        if t_sym > 16:
            v_DE = 1
    elif enable_ldro:
        v_DE = 1
    # IH
    v_IH = 0
    if not enable_eh:
        v_IH = 1
    # CRC
    v_CRC = 1
    if enable_crc == False:
        v_CRC = 0
    #
    a = 8.*n_size - 4.*n_sf + 28 + 16*v_CRC - 20.*v_IH
    b = 4.*(n_sf-2.*v_DE)
    v_ceil = a/b
    n_payload = 8 + max(math.ceil(a/b)*(n_cr+4), 0)
    t_payload = n_payload * t_sym
    t_packet = t_preamble+ t_payload

    ret = {}
    ret["r_sym"] = r_sym
    ret["t_sym"] = t_sym
    ret["n_preamble"] = n_preamble
    ret["t_preamble"] = t_preamble
    ret["v_DE"] = v_DE
    ret["v_ceil"] = v_ceil
    ret["n_sym_payload"] = n_payload
    ret["t_payload"] = t_payload
    ret["t_packet"] = round(t_packet, 3)

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
            default=125, metavar="NUMBER",
            help="bandwidth in kHz. default is 125 kHz.")
        p.add_argument("--disable-auto-ldro", action="store_false",
            dest="enable_auto_ldro",
            help="disable the auto LDRO and disable LDRO.")
        p.add_argument("--enable-ldro", action="store_true", dest="enable_ldro",
            help="This option is available when the auto LDRO is disabled.")
        p.add_argument("--disable-eh", action="store_false", dest="enable_eh",
            help="disable the explicit header.")
        p.add_argument("--downlink", action="store_false", dest="enable_crc",
            help="disable the CRC field, which is for the LoRaWAN downlink stream.")
        p.add_argument("--disable-crc", action="store_false", dest="enable_crc",
            help="same effect as the --downlink option.")
        p.add_argument("--cr", action="store", dest="n_cr",
            type=int, default=1, metavar="NUMBER",
            help="specify the CR value. default is 1 as LoRaWAN does.")
        p.add_argument("--preamble", action="store", dest="n_preamble",
            type=int, default=8, metavar="NUMBER",
            help="specify the preamble. default is 8 for AS923.")
        p.add_argument("--duty-cycle", action="store", dest="n_duty_cycle",
            type=int, default=1, metavar="NUMBER",
            help="specify the duty cycle in percentage. default is 1 %%.")
        p.add_argument("-v", action="store_true", dest="f_verbose",
            default=False,
            help="enable verbose mode.")
        p.add_argument("-d", action="append_const", dest="_f_debug", default=[],
            const=1, help="increase debug mode.")
    
        args = p.parse_args()

        args.v_de = False
        args.debug_level = len(args._f_debug)
        return args

    #
    # main
    #
    opt = parse_args()
    ret = get_toa(opt.n_size, opt.n_sf, n_bw=opt.n_bw,
                  enable_auto_ldro=opt.enable_auto_ldro,
                  enable_ldro=opt.enable_ldro,
                  enable_eh=opt.enable_eh, enable_crc=opt.enable_crc,
                  n_cr=opt.n_cr, n_preamble=opt.n_preamble)
    ret["phy_pl_size"] = opt.n_size
    ret["mac_pl_size"] = opt.n_size - 5
    ret["sf"] = opt.n_sf
    ret["bw"] = opt.n_bw
    ret["ldro"] = "enable" if ret["v_DE"] else "disable"
    ret["eh"] = "enable" if opt.enable_eh else "disable"
    ret["cr"] = opt.n_cr
    ret["preamble"] = opt.n_preamble
    ret["duty_cycle"] = opt.n_duty_cycle
    ret["t_cycle"] = (ret["t_packet"]/1000.)*(100./ret["duty_cycle"])
    ret["max_packets_day"] = 86400./ret["t_cycle"]
    if opt.f_verbose:
        print "PHY payload size    : %d Bytes" % ret["phy_pl_size"]
        print "MAC payload size    : %d Bytes" % ret["mac_pl_size"]
        print "Spreading Factor    : %d" % ret["sf"]
        print "Band width          : %d kHz" % ret["bw"]
        print "Low data rate opt.  : %s" % ret["ldro"]
        print "Explicit header     : %s" % ret["eh"]
        print "CR (coding rate)    : %d (4/%d)" % (ret["cr"], 4+ret["cr"])
        print "Symbol Rate         : %.3f symbol/s" % ret["r_sym"]
        print "Symbol Time         : %.3f msec/symbol" % ret["t_sym"]
        print "Preamble size       : %d symbols" % ret["preamble"]
        print "Packet symbol size  : %d symbols" % ret["n_sym_payload"]
        print "Preamble ToA        : %.3f msec" % ret["t_preamble"]
        print "Payload ToA         : %.3f msec" % ret["t_payload"]
        print "Time on Air         : %.3f msec" % ret["t_packet"]
        print "Duty Cycle          : %d %%" % ret["duty_cycle"]
        print "Min span of a cycle : %.3f sec" % ret["t_cycle"]
        print "Max Frames per day  : %d frames" % ret["max_packets_day"]
        if opt.debug_level:
            ret0 = get_toa(0, opt.n_sf, n_bw=opt.n_bw,
                           enable_auto_ldro=opt.enable_auto_ldro,
                           enable_ldro=opt.enable_ldro,
                           enable_eh=opt.enable_eh, enable_crc=opt.enable_crc,
                           n_cr=opt.n_cr, n_preamble=opt.n_preamble)
            print "PHY PL=0 ToA        : %.3f msec" % (ret0["t_packet"])
            # preamble=8 cr=1? payload-len=7? crc=16 (payload) payload-crc=16
            # =? 48 ==> 6 bytes ?
            t0 = (ret["t_packet"]-ret0["t_packet"])/1000.
            print "PHY fr.dr.(48b) 7:15: %.3f bps" % ((8.*opt.n_size+48)/t0)
            print "MAC frame DR        : %.3f bps" % ((8.*(opt.n_size))/t0)
            print "before ceil(x)      : %.3f" % ret["v_ceil"]
    else:
        print "%.3f" % ret["t_packet"]
