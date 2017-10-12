
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import matplotlib.pyplot as plt
import numpy as np
from lorawan_toa import *

####

def get_y_toa(data_size, n_sf, n_bw=125):
    if type(data_size) == list:
        return [ get_y_toa(i, n_sf, n_bw=n_bw) for i in data_size ]
    else:
        return get_toa(data_size, n_sf, n_bw=n_bw)["t_packet"]

def get_y_br(data_size, n_sf, n_bw=125):
    return [ (i*8)/(get_toa(i, n_sf, n_bw=n_bw)["t_packet"]/1000.)
            for i in data_size ]

def get_y_br1(data_size, n_sf, n_bw=125):
    if type(data_size) == list:
        ret = []
        for i in data_size:
            ret.append(get_y_br1(i, n_sf, n_bw=n_bw))
        return ret
    else:
        toa0 = get_toa(0, n_sf, n_bw=n_bw)["t_packet"]
        toa = get_toa(data_size, n_sf, n_bw=n_bw)["t_packet"]
        if toa == toa0:
            return 0
        else:
            return (data_size*8)/((toa - toa0)/1000.)

########
#
x_nb_bytes = range(0, 40)

fig = plt.figure(facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("LoRa Data Rate (BW=125kHz, AS923)")
ax.set_xlabel("PHY payload size (B)")
ax.set_ylabel("Bitrate (bps)")
ax.set_xlim(0, 40)
#ax.set_ylim(0, 700)
#ax2.set_ylim(0, 7000)

lines = []

lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes, 12), "b-", label="SF12 DE=1")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes, 11), "g-", label="SF11 DE=1")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes, 10), "k-", label="SF10 DE=0")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes,  9), "c-", label="SF 9 DE=0")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes,  8), "m-", label="SF 8 DE=0")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes,  7), "y-", label="SF 7 DE=0")

#ax.plot(x_nb_bytes, [  292.97 for i in x_nb_bytes ], "b--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [  250.00 for i in x_nb_bytes ], "b--", lw=2, alpha=0.5)
#ax.plot(x_nb_bytes, [  537.11 for i in x_nb_bytes ], "g--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [  440.00 for i in x_nb_bytes ], "g--", lw=2, alpha=0.5)

ax.plot(x_nb_bytes, [  976.56 for i in x_nb_bytes ], "k--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [ 1757.81 for i in x_nb_bytes ], "c--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [ 3125.00 for i in x_nb_bytes ], "m--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [ 5468.75 for i in x_nb_bytes ], "y--", lw=2, alpha=0.5)

ax.axvline(12, color='k', linestyle='--', alpha=0.7)
ax.scatter(16, get_y_br1(16, 7), s=80, facecolors='none', edgecolors='r')
ax.scatter(19, get_y_br1(19, 7), s=80, facecolors='none', edgecolors='r')
ax.scatter(26, get_y_br1(26, 7), s=80, facecolors='none', edgecolors='r')

ax.grid(which="both")

ax.legend(lines, [i.get_label() for i in lines],
          loc="upper right", prop={'size': 10})

fig.tight_layout()
plt.show()
fig.savefig("image/lorawan-dr-all-50b.png")

########
#
x_nb_bytes = range(0, 255)

fig = plt.figure(facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("LoRa Data Rate (BW=125kHz, AS923)")
ax.set_xlabel("PHY payload size (B)")
ax.set_ylabel("Bitrate (bps)")
ax.set_xlim(0, 260)
#ax.set_ylim(0, 700)
#ax2.set_ylim(0, 7000)

lines = []

lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes, 12), "b-", label="SF12 DE=1")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes, 11), "g-", label="SF11 DE=1")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes, 10), "k-", label="SF10 DE=0")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes,  9), "c-", label="SF 9 DE=0")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes,  8), "m-", label="SF 8 DE=0")
lines += ax.plot(x_nb_bytes, get_y_br1(x_nb_bytes,  7), "y-", label="SF 7 DE=0")

#ax.plot(x_nb_bytes, [  292.97 for i in x_nb_bytes ], "b--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [  250.00 for i in x_nb_bytes ], "b--", lw=2, alpha=0.5)
#ax.plot(x_nb_bytes, [  537.11 for i in x_nb_bytes ], "g--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [  440.00 for i in x_nb_bytes ], "g--", lw=2, alpha=0.5)

ax.plot(x_nb_bytes, [  976.56 for i in x_nb_bytes ], "k--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [ 1757.81 for i in x_nb_bytes ], "c--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [ 3125.00 for i in x_nb_bytes ], "m--", lw=2, alpha=0.5)
ax.plot(x_nb_bytes, [ 5468.75 for i in x_nb_bytes ], "y--", lw=2, alpha=0.5)

ax.axvline(12, color='k', linestyle='--', alpha=0.7)

ax.grid(which="both")

ax.legend(lines, [i.get_label() for i in lines],
          loc="upper right", prop={'size': 10})

fig.tight_layout()
plt.show()
fig.savefig("image/lorawan-dr-all.png")

########
#
x_nb_bytes = range(0, 255)

fig = plt.figure(facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)
ax.set_title("LoRa Data Rate (SF7, BW=125kHz [AS923 DR5])")
ax.set_xlabel("PHY payload size (B)")
ax.set_ylabel("Time on Air (ms)")
ax2 = ax.twinx()
ax2.set_ylabel("Bitrate (bps)")
ax.set_xlim(0, 260)
ax.set_ylim(0, 800)
ax2.set_ylim(0, 8000)

lines = []

n_sf = 7
lines += ax.plot(x_nb_bytes, get_y_toa(x_nb_bytes, n_sf), "k-", label="ToA")

lines += ax2.plot(x_nb_bytes, [ 5468.75 for i in x_nb_bytes ],
                  "r-", label="Equivalent BR.")

lines += ax2.plot(x_nb_bytes, get_y_br(x_nb_bytes, n_sf),
                  "b-", label="Simple BR of PHY_PL/ToA")
lines += ax2.plot(x_nb_bytes, get_y_br1(x_nb_bytes, n_sf),
                  "y-", label="Cal. BR. PHY_PL/ToA DE=0")

ax2.axvline(12, color='k', linestyle='--', alpha=0.7)

ax.grid(which="both")

ax.legend(lines, [i.get_label() for i in lines],
          loc="lower right", prop={'size': 10})

fig.tight_layout()
plt.show()
fig.savefig("image/lorawan-dr-sf7-base.png")

