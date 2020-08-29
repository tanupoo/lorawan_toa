#!/usr/bin/env python

from lorawan_toa_cal import get_toa
import argparse

def parse_args():
    p = argparse.ArgumentParser(
            description="LoRa Time on Air calculator.")
    p.add_argument("n_sf", metavar="SF", type=int,
        help="Spreading Factor. It should be from 7 to 12.")
    p.add_argument("n_size", metavar="SIZE", type=int,
        help="""PHY payload size in byte.
                    Remember that PHY payload (i.e. MAC frame) consists of 
                    MHDR(1) + MAC payload + MIC(4), or
                    MHDR(1) + FHDR(7) + FPort(1) + APP + MIC(4).
                    For example, SIZE for Join Request is going to be 23.
                    If the size of an application message (APP) is
                    12, SIZE is going to be 25. """)
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

if __name__ == "__main__" :
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
    ret["t_cycle_jp1"] = ret["t_packet"] + 50   # waiting time = 50 ms
    ret["t_cycle_jp2"] = ret["t_packet"] + ret["t_packet"]*10   # duty = 10%
    ret["datarate_jp1"] = (8*ret["mac_pl_size"])/(ret["t_cycle_jp1"]/1000.)
    ret["datarate_jp2"] = (8*ret["mac_pl_size"])/(ret["t_cycle_jp2"]/1000.)
    if opt.f_verbose:
        print("PHY payload size    : %d Bytes" % ret["phy_pl_size"])
        print("MAC payload size    : %d Bytes" % ret["mac_pl_size"])
        print("Spreading Factor    : %d" % ret["sf"])
        print("Band width          : %d kHz" % ret["bw"])
        print("Low data rate opt.  : %s" % ret["ldro"])
        print("Explicit header     : %s" % ret["eh"])
        print("CR (coding rate)    : %d (4/%d)" % (ret["cr"], 4+ret["cr"]))
        print("Symbol Rate         : %.3f symbol/s" % ret["r_sym"])
        print("Symbol Time         : %.3f msec/symbol" % ret["t_sym"])
        print("Preamble size       : %d symbols" % ret["preamble"])
        print("Packet symbol size  : %d symbols" % ret["n_sym_payload"])
        print("Preamble ToA        : %.3f msec" % ret["t_preamble"])
        print("Payload ToA         : %.3f msec" % ret["t_payload"])
        print("Time on Air         : %.3f msec" % ret["t_packet"])
        print("Duty Cycle          : %d %%" % ret["duty_cycle"])
        print("Min span of a cycle : %.3f sec" % ret["t_cycle"])
        print("Max Frames per day  : %d frames" % ret["max_packets_day"])
        if opt.debug_level:
            print("Data rate (*1)      : %.3f bps" % ret["datarate_jp1"])
            print("Data rate (*2)      : %.3f bps" % ret["datarate_jp2"])
            ret0 = get_toa(0, opt.n_sf, n_bw=opt.n_bw,
                           enable_auto_ldro=opt.enable_auto_ldro,
                           enable_ldro=opt.enable_ldro,
                           enable_eh=opt.enable_eh, enable_crc=opt.enable_crc,
                           n_cr=opt.n_cr, n_preamble=opt.n_preamble)
            print("PHY PL=0 ToA        : %.3f msec" % (ret0["t_packet"]))
            # preamble=8 cr=1? payload-len=7? crc=16 (payload) payload-crc=16
            # =? 48 ==> 6 bytes ?
            t0 = (ret["t_packet"]-ret0["t_packet"])/1000.
            print("PHY fr.dr.(48b) 7:15: %.3f bps" % ((8.*opt.n_size+48)/t0))
            print("MAC frame DR        : %.3f bps" % ((8.*(opt.n_size))/t0))
            print("before ceil(x)      : %.3f" % ret["v_ceil"])
            print("    (*1) data rate of MAC Payload in JP Ch 24-38 20mW.")
            print("    (*2) data rate of MAC Payload in JP Ch 33-61 20mW.")
    else:
        print("%.3f" % ret["t_packet"])
