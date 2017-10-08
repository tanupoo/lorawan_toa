#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import matplotlib.pyplot as plt
from lorawan_toa import *

def get_line(list_size, n_sf, bw=125):
    return [ get_toa(i, n_sf, n_bw=bw)["t_packet"] for i in list_size ]

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("SF and ToA (BW=125 kHz)")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", label="SF12", linewidth=3, alpha=1)
ax.plot(x, get_line(x, 11), "g-", label="SF11", linewidth=3, alpha=1)
ax.plot(x, get_line(x, 10), "k-", label="SF10", linewidth=3, alpha=1)
ax.plot(x, get_line(x, 9), "c-", label="SF9", linewidth=3, alpha=1)
ax.plot(x, get_line(x, 8), "m-", label="SF8", linewidth=3, alpha=1)
ax.plot(x, get_line(x, 7), "y-", label="SF7", linewidth=3, alpha=1)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="upper left", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/lora-toa-125.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("AS923 No DwellTime")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 11), "g-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 10), "k-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 9), "c-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 8), "m-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 7), "y-", linewidth=3, alpha=0.05)

# no dwellTime consideration
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 12), "b-", label="SF12",
         linewidth=3, alpha=1)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 11), "g-", label="SF11",
         linewidth=3, alpha=1)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 10), "k-", label="SF10",
         linewidth=3, alpha=1)
ax.plot(mpsrange(8, 123), get_line(mpsrange(8, 123), 9), "c-", label="SF9",
         linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 8), "m-", label="SF8",
         linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-", label="SF7",
         linewidth=3, alpha=1)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="upper left", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/as923-without-dwelltime.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("AS923 DwellTime 400ms")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 11), "g-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 10), "k-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 9), "c-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 8), "m-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 7), "y-", linewidth=3, alpha=0.05)

# required dwellTime consideration
ax.plot([0], [0], "b-", label="SF12", linewidth=3, alpha=1)
ax.plot([0], [0], "c-", label="SF11", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 19), get_line(mpsrange(8, 19), 10), "k-", label="SF10", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 61), get_line(mpsrange(8, 61), 9), "c-", label="SF9", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 133), get_line(mpsrange(8, 133), 8), "m-", label="SF8", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-", label="SF7", linewidth=3, alpha=1)

ax.plot(x, [400 for i in range(0, 255)], "r,", linewidth=1, alpha=0.7)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="upper left", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/as923-with-dwelltime.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("AS923")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 11), "g-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 10), "k-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 9), "c-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 8), "m-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 7), "y-", linewidth=3, alpha=0.05)

# no dwellTime consideration
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 12), "b-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 11), "g-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 10), "k-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 123), get_line(mpsrange(8, 123), 9), "c-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 8), "m-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-", linewidth=1.2, alpha=0.7)

# required dwellTime consideration
ax.plot([0], [0], "b-", label="SF12/125kHz", linewidth=3, alpha=1)
ax.plot([0], [0], "g-", label="SF11/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 19), get_line(mpsrange(8, 19), 10), "k-",
         label="SF10/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 61), get_line(mpsrange(8, 61), 9), "c-",
         label="SF9/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 133), get_line(mpsrange(8, 133), 8), "m-",
         label="SF8/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-",
         label="SF7/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7, bw=250), "b--",
         label="SF7/250kHz", linewidth=3, alpha=0.5)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="upper left", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/as923-toa.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("AS923 and ARIB STD-T108")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 11), "g-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 10), "k-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 9), "c-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 8), "m-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 7), "y-", linewidth=3, alpha=0.05)

# no dwellTime consideration
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 12), "b-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 11), "g-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 10), "k-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 123), get_line(mpsrange(8, 123), 9), "c-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 8), "m-", linewidth=1.2, alpha=0.7)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-", linewidth=1.2, alpha=0.7)

# required dwellTime consideration
ax.plot([0], [0], "b-", label="SF12/125kHz", linewidth=3, alpha=1)
ax.plot([0], [0], "g-", label="SF11/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 19), get_line(mpsrange(8, 19), 10), "k-",
         label="SF10/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 61), get_line(mpsrange(8, 61), 9), "c-",
         label="SF9/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 133), get_line(mpsrange(8, 133), 8), "m-",
         label="SF8/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-",
         label="SF7/125kHz", linewidth=3, alpha=1)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7, bw=250), "b--",
         label="SF7/250kHz", linewidth=3, alpha=0.5)

ax.plot(x, [400 for i in range(0, 255)], "r--", linewidth=2, alpha=0.7)
ax.plot(x, [200 for i in range(0, 255)], "r--", linewidth=2, alpha=0.7)
ax.plot(x, [4000 for i in range(0, 255)], "r--", linewidth=2, alpha=0.7)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="upper left", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/as923-with-arib180.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("AS923 vs Others (SF12)")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 12, bw=500), "r-", linewidth=3, alpha=0.05)

# no dwellTime consideration
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 12), "b-",
         label="SF12/125kHz", linewidth=3.0, alpha=1)

# LoRa: SF12 / 500 kHz
ax.plot(mpsrange(8, 61), get_line(mpsrange(8, 61), 12, bw=500), "r-",
         label="SF12/500kHz", linewidth=3, alpha=1)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="best", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/as923-vs-others-sf12.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("AS923 vs Others (SF10)")

x = range(0, 255)
ax.plot(x, get_line(x, 10), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 10, bw=500), "r-", linewidth=3, alpha=0.05)

# no dwellTime consideration
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 10), "b-",
         label="SF10/125kHz", linewidth=3.0, alpha=1)

# LoRa: SF10 / 500 kHz
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 10, bw=500), "r-",
         label="SF10/500kHz", linewidth=3, alpha=1)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="best", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/as923-vs-others-sf10.png")

#########
#
fig = plt.figure(num=None, figsize=(16, 8), facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("LoRaWAN")

x = range(0, 255)
ax.plot(x, get_line(x, 12), "b-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 11), "g-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 10), "k-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 9), "c-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 8), "m-", linewidth=3, alpha=0.05)
ax.plot(x, get_line(x, 7), "y-", linewidth=3, alpha=0.05)

# SF  BW  bit rate    Max. MACPayload
# 12  125 250         59
# 11  125 440         59
# 10  125 980         59
# 9   125 1760        123
# 8   125 3125        250
# 7   125 5470        250
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 12), "b-",
         label="SF12/125kHz", linewidth=2.0)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 11), "g-",
         label="SF11/125kHz", linewidth=2.0)
ax.plot(mpsrange(8, 59), get_line(mpsrange(8, 59), 10), "k-",
         label="SF10/125kHz", linewidth=2.0)
ax.plot(mpsrange(8, 123), get_line(mpsrange(8, 123), 9), "c-",
         label="SF9/125kHz", linewidth=2.0)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 8), "m-",
         label="SF8/125kHz", linewidth=2.0)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7), "y-",
         label="SF7/125kHz", linewidth=2.0)

# SF  BW  bit rate    Max. MACPayload
# 7   250 11000   250
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7, bw=250), "b-.",
         label="SF7/250kHz", linewidth=2.0)

# SF  BW  bit rate    Max. MACPayload
# 12  500 980         61
# 11  500 1760        137
# 10  500 3900        250
# 9   500 7000        250
# 8   500 12500       250
# 7   500 21900       250
ax.plot(mpsrange(8, 61), get_line(mpsrange(8, 61), 12, bw=500), "b--",
         label="SF12/500kHz", linewidth=2.0)
ax.plot(mpsrange(8, 137), get_line(mpsrange(8, 137), 11, bw=500), "g--",
         label="SF11/500kHz", linewidth=2.0)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 10, bw=500), "k--",
         label="SF10/500kHz", linewidth=2.0)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 9, bw=500), "c--",
         label="SF9/500kHz", linewidth=2.0)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 8, bw=500), "m--",
         label="SF8/500kHz", linewidth=2.0)
ax.plot(mpsrange(8, 250), get_line(mpsrange(8, 250), 7, bw=500), "y--",
         label="SF7/500kHz", linewidth=2.0)

ax.set_xlim(0, 260)
ax.set_ylim(0, 5000)
ax.set_xlabel("PHY Payload Size (Byte)")
ax.set_ylabel("Time on Air (ms)")
ax.grid(True)
ax.legend(loc="upper right", fancybox=True, shadow=True)

fig.tight_layout()
plt.show()
fig.savefig("image/lorawan-toa.png")

