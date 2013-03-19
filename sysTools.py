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


def runcmd(args, input=None):
    """
    Split args into a list, run this command, and return its output.
    Raise RuntimeError if the command does not return 0.
    @note: This function will not work if args contains pipes |
    @param input: If this exists, it will be fed as stdin
    """
    import subprocess
    #    print args
    import string

    if input == None:
        stdin = None
    else:
        stdin = subprocess.PIPE
    proc = subprocess.Popen(string.split(args), stdout=subprocess.PIPE, stdin=stdin)
    #    proc = subprocess.Popen(string.split(args), stdout=subprocess.PIPE)
    output = proc.communicate(input=input)[0]
    if proc.returncode != 0:
        import exceptions

        raise exceptions.RuntimeError
    return output


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


class sysArgs:
    '''
    class argument handler
    '''

    def __init__(self, argv=None, description='None'):
        if not len(argv):
            print 'Please check usage by: \'-h\' or \'--help\' '
            return

        import argparse

        self.parser = argparse.ArgumentParser(description=description)

    def add_args(self, label='-a', type=int, desc='sample option', default=[0]):
        self.parser.add_argument(label, type=type, help=desc, nargs='+', default=default)


    def get_args(self):
        return self.parser.parse_args()


if __name__ == '__main__':

    # === test sysArgs ===
    # import sys
    #
    # a = sysArgs(sys.argv[1:], 'this is a sample')
    # a.add_args()
    # args = a.get_args()
    # print args.a[0]

    # === test runcmd() ===
    # print runcmd('ls -al')


    pass