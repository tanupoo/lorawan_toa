LoRa/LoRaWAN Time on Air calculator
===================================

A calculator of the time on air (ToA) of LoRa/LoRaWAN PHY frame in Python.

(28-Aug-2020) Python2 has sunset already.  For Python3, toa.py has been added.  Don't worry.  lorawan_toa.py is not changed for backward compatibility.

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

```
usage: toa.py [-h] [--band-width NUMBER] [--disable-auto-ldro] [--enable-ldro]
              [--disable-eh] [--downlink] [--disable-crc] [--cr NUMBER]
              [--preamble NUMBER] [--duty-cycle NUMBER] [-v] [-d]
              SF SIZE

LoRa Time on Air calculator.

positional arguments:
  SF                   Spreading Factor. It should be from 7 to 12.
  SIZE                 PHY payload size in byte. Remember that PHY payload
                       (i.e. MAC frame) consists of MHDR(1) + MAC payload +
                       MIC(4), or MHDR(1) + FHDR(7) + FPort(1) + APP + MIC(4).
                       For example, SIZE for Join Request is going to be 23.
                       If the size of an application message (APP) is 12, SIZE
                       is going to be 25.

optional arguments:
  -h, --help           show this help message and exit
  --band-width NUMBER  bandwidth in kHz. default is 125 kHz.
  --disable-auto-ldro  disable the auto LDRO and disable LDRO.
  --enable-ldro        This option is available when the auto LDRO is
                       disabled.
  --disable-eh         disable the explicit header.
  --downlink           disable the CRC field, which is for the LoRaWAN
                       downlink stream.
  --disable-crc        same effect as the --downlink option.
  --cr NUMBER          specify the CR value. default is 1 as LoRaWAN does.
  --preamble NUMBER    specify the preamble. default is 8 for AS923.
  --duty-cycle NUMBER  specify the duty cycle in percentage. default is 1 %.
  -v                   enable verbose mode.
  -d                   increase debug mode.
```

## Examples

with the -v option, it shows the ToA as well as the related information.
below example, it show detail information in SF 12, 64 bytes of PHY payload,
125 kHz bandwidth, preamble 8.

```
% toa.py 12 64 -v
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
Duty Cycle          : 1 %
Min span of a cycle : 279.347 sec
Max Frames per day  : 309 frames
```

without the -v option, it simply shows the ToA.

```
% toa.py 12 64
2793.472
```

There is an example of Semtech LoRa Caluculator Interface in the datasheet.
If the parameters in that picture apply to toa.py, below is the command line.

```
% toa.py 12 8 --band-width 500 --cr 1 --disable-auto-ldro --preamble 6 --disable-eh -v
PHY payload size    : 8 Bytes
MAC payload size    : 3 Bytes
Spreading Factor    : 12
Band width          : 500 kHz
Low data rate opt.  : disable
Explicit header     : disable
CR (coding rate)    : 1 (4/5)
Symbol Rate         : 122.070 symbol/s
Symbol Time         : 8.192 msec/symbol
Preamble size       : 6 symbols
Packet symbol size  : 13 symbols
Preamble ToA        : 83.968 msec
Payload ToA         : 106.496 msec
Time on Air         : 190.464 msec
RAW data rate       : 1171.875 bps
Duty Cycle          : 1 %
Min span of a cycle : 19.046 sec
Max Frames per day  : 4536 frames
```


## graph_as923.py

    It makes a set of figures about Time on Air and PHYPayload size,
    especially LoRaWAN AS923 using matlib like below.

![LoRa ToA](image/as923-toa.png)

