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

