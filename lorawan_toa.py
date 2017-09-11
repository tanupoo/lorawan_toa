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

def get_toa(n_size, n_sf, bw=125, de=0):
    '''
    n_size: PHY Payload size (MAC Payload)
    n_sf: SF (12 to 7)
    bw: Bandwidth.  default is 125 KHz.
    '''
    t_sym = math.pow(2, n_sf) / (bw*1000.) * 1000.
    n_preamble = 8    # AS923
    t_preamble = (n_preamble + 4.25) * t_sym
    v_h = 0    # LoRaWAN: No explicit header
    v_de = de  # LoRaWAN: low data optimization
    v_cr = 1   # LoRaWAN: 4/5
    a = 8.*n_size - 4.*n_sf + 28 + 16 - 20.*v_h
    b = 4.*(n_sf-2.*v_de)
    nb_sym_payload = 8 + max(math.ceil(a/b)*(v_cr+4), 0)
    t_payload = nb_sym_payload * t_sym
    t_frame = t_preamble+ t_payload

    return round(t_frame, 3)

if __name__ == "__main__" :
    import sys
    if len(sys.argv) < 3:
        print("Usage: %s (sf) (size) [bw] [de]" % (sys.argv[0]))
        print("    size: PHY Payload siz (= MAC Payload + 5)")
        print("    bw: bandwidth. default is 125 kHz.")
        print("    de: low data optimization. default is 0.")
        exit(1)
    n_sf = int(sys.argv[1])
    n_size = int(sys.argv[2])
    n_bw = 125
    n_de = 0
    if len(sys.argv) == 4:
        n_bw = int(sys.argv[3])
    elif len(sys.argv) == 5:
        n_bw = int(sys.argv[3])
        n_de = int(sys.argv[4])
    t_frame = get_toa(n_size, n_sf, bw=n_bw, de=n_de)
    print "%.3f (ms)" % t_frame
