lorawan_toa
===========

A calculator of the time on air of LoRa PHY frame in Python.
This script refers to the section 4.1.1.6. LoRa Packet Structure,
[SX1276/77/78/79 Datasheet][http://www.semtech.com/images/datasheet/sx1276_77_78_79.pdf].

## Usage

    Usage: lorawan_toa.py (sf) (size) [bw] [de]
        size: PHY Payload siz (= MAC Payload + 5)
        bw: bandwidth. default is 125 kHz.
        de: low data optimization. default is 0.

    % python lorawan_toa.py 12 64 500
    616.448 (ms)

## graph_as923.py

    It makes a set of figures about Time on Air and PHYPayload size,
    especially LoRaWAN AS923 using matlib like below.

![LoRa ToA](lora_toa.png)

