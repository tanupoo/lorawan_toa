#!/usr/bin/env python

from lorawan_toa_cal import get_toa, parse_args

if __name__ == "__main__" :
    opt = parse_args()
    if opt.sf != "FSK":
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
        ret["raw_datarate"] = opt.n_sf * 4/(4+opt.n_cr) * ret["r_sym"]
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
            print("RAW data rate       : %.3f bps" % ret["raw_datarate"])
            #print("MAC data rate       : %.3f bps" % ret["mac_datarate"])
            print("Duty Cycle          : %d %%" % ret["duty_cycle"])
            print("Min span of a cycle : %.3f sec" % ret["t_cycle"])
            print("Max Frames per day  : %d frames" % ret["max_packets_day"])
            if opt.debug_level:
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
        else:
            print("%.3f" % ret["t_packet"])
    else: # FSK
        raise NotImplementedError
        pass
