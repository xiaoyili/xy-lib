'''
based on Turian's
'''

import os
import datetime

import memory


__initrealtime = os.times()[4]


def stats():
    """
    Return a string of statistics:
    nodename time: user+sys elapsed, realtime elapsed, CPU usage, memory usage
    """
    nodename = os.uname()[1]
    t = os.times()
    usersystime = t[0] + t[1]
    realtime = t[4] - __initrealtime

    usage = 100. * usersystime / (realtime + 0.00001)
    usersystime = datetime.timedelta(seconds=usersystime)
    realtime = datetime.timedelta(seconds=realtime)
    return "%s %s: %s user+sys, %s real, %.2f%% usage, %.2f MB" % (
    nodename, datetime.datetime.now(), usersystime, realtime, usage, memory.memory() / 1024. / 1024.)
