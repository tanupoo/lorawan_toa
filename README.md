LoRa Time on Air calculator
===========================

A calculator of the time on air of LoRa PHY frame in Python.

This script refers to the section 4.1.1.6. LoRa Packet Structure,
[SX1276/77/78/79 Datasheet rev.5][http://www.semtech.com/images/datasheet/sx1276.pdf].

The default parameters of the equation is based on LoRaWAN AS923
in the LoRaWAN regional parameters v1.1.

## Note

The default value of Explicit Header is enable.
It is guessed from the PHY frame format
though there is no explit text in the LoRaWAN specification.

The value of LowDataRateOptimization is set automatically
when the symbol duration exceeds 16ms.
Because the datasheet requires that it must be used
when the symbol duration exceeds 16ms.
This is the case below:

- SF=12 and 11 in 125 kHz.
- SF=12 in 250 kHz.

You can disable this feature by the --disable-auto-ldro option.
The LDRO is disabled by default if you disable the auto LDRO.
If you want to enable the LDRO, you can specify the --enable-ldro option.

In the downlink stream, the CRC at the tail of the PHY frame is not used.
To calculate the ToA for the downlink stream,
the --downlink option should be specified.

## Usage

    lorawan_toa.py [-h] [--band-width N_BW] [--disable-auto-ldro]
                        [--enable-ldro] [--disable-eh] [--downlink]
                        [--disable-crc] [--cr N_CR] [--preamble N_PREAMBLE] [-v]
                        [-d]
                        SF SIZE
    
    positional arguments:
      SF                    Spreading Factor. It should be from 7 to 12.
      SIZE                  PHY payload size in byte. It's equal to the MAC
                            payload + 5.
    
    optional arguments:
      -h, --help            show this help message and exit
      --band-width N_BW     bandwidth in kHz. default is 125 kHz.
      --disable-auto-ldro   disable the auto LDRO and disable LDRO.
      --enable-ldro         This option is available when the auto LDRO is
                            disabled.
      --disable-eh          disable the explicit header.
      --downlink            disable the CRC field, which is for the LoRaWAN
                            downlink stream.
      --disable-crc         same effect as the --downlink option.
      --cr N_CR             specify the CR value. default is 1 as LoRaWAN does.
      --preamble N_PREAMBLE
                            specify the preamble. default is 8 for AS923.
      -v                    enable verbose mode.
      -d                    increase debug mode.

## Examples

with the -v option, it shows the ToA as well as the related information.
below example, it show detail information in SF 12, 64 bytes of PHY payload,
125 kHz bandwidth, preamble 8.

    % python lorawan_toa.py 12 64 -v
    PHY payload size    : 64 Bytes
    MAC payload size    : 59 Bytes
    Spreading Factor    : 12
    Band width          : 125 kHz
    Low data rate opt.  : enable
    Explicit header     : enable
    CR (coding rate)    : 1 (4/5)
    Symbol Rate         : 30.518 symbol/s
    Symbol Time         : 32.768 msec/symbol
    Preamble size       : 8 symbols
    Packet symbol size  : 73 symbols
    Preamble ToA        : 401.408 msec
    Payload ToA         : 2392.064 msec
    Time on Air         : 2793.472 msec

without the -v option, it simply shows the ToA.

    % python lorawan_toa.py 12 64
    2793.472

## graph_as923.py

    It makes a set of figures about Time on Air and PHYPayload size,
    especially LoRaWAN AS923 using matlib like below.

![LoRa ToA](image/as923-toa.png)

##
