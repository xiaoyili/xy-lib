'''
expanded based on Turian's
'''

import os
import datetime
import random
import time

# third-party
import memory


__initrealtime = os.times()[4]


def sys_stats():
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


def random_sleep(min, max):
    """ Sleep some random time in [min, max) """
    sleep = random.random() * (max - min) + min
    #sleep = random.random() * 2 + 0
    print "Sleeping %g seconds..." % sleep
    time.sleep(sleep)


#http://www.daniweb.com/code/snippet368.html
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2 - t1) * 1000.0)
        return res

    return wrapper


def gmtimestr():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
