LoRa Time on Air calculator
===========================

A calculator of the time on air of LoRa PHY frame in Python.
This script refers to the section 4.1.1.6. LoRa Packet Structure,
[SX1276/77/78/79 Datasheet][http://www.semtech.com/images/datasheet/sx1276_77_78_79.pdf].

The default value is aligned to LoRaWAN AS923.

## Usage

    lorawan_toa.py [-h] [--band-width N_BW] [--disable-dro] [--disable-eh]
                          [--cr N_CR] [--preamble N_PREAMBLE] [-v] [-d]
                          SF SIZE
    
    positional arguments:
      SF                    Spreading Factor. It should be from 7 to 12.
      SIZE                  PHY payload size in byte. It's equal to the MAC
                            payload + 5.
    
    optional arguments:
      -h, --help            show this help message and exit
      --band-width N_BW     bandwidth in kHz. default is 125 kHz.
      --disable-dro         disable the low data rate optimization. default is
                            enable as LoRaWAN does.
      --disable-eh          disable the explicit header. default is enable as
                            LoRaWAN does.
      --cr N_CR             specify the CR value. default is 1 as LoRaWAN does.
      --preamble N_PREAMBLE
                            specify the preamble. default is 8 for AS923.
      -v                    enable verbose mode.
      -d                    increase debug mode.

## Examples

with the -v option, it shows the ToA as well as the related information.

    % python lorawan_toa.py 12 64 -v
    PHY payload size    : 64 Bytes
    MAC payload size    : 59 Bytes
    Spreading Factor    : 12
    Band width          : 125 kHz
    Low data rate opt.  : enable
    Explicit header     : enable
    CR (coding rate)    : 1 (4/5)
    Preamble size       : 8 symbols
    Time on Air         : 2793.472 msec
    MAC frame data rate : 63.998 bps

without the -v option, it simply shows the ToA.

    % python lorawan_toa.py --band-width=500 7 128    
    71.744

## graph_as923.py

    It makes a set of figures about Time on Air and PHYPayload size,
    especially LoRaWAN AS923 using matlib like below.

![LoRa ToA](lora_toa.png)

