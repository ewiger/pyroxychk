#!/usr/bin/env python
'''

 PyProxyChecker v 0.1.0

 - reads any text file (first argument) and parses all found ip:port patterns
 - pure python implementation
 - can ping host before checking the port

Copyright (c) 2011, Yauhen Yakimovich <http://yauhen.yakimovich.info>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY YAUHEN YAKIMOVICH ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL YAUHEN YAKIMOVICH OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of YAUHEN YAKIMOVICH.
'''
import re
import sys
import ping
from socket import *


class IpAddress(object):

    def __init__(self, addr, port=8080):
        self.addr = addr
        if type(port) is str:
            port = int(port)
        self.port = port

    def __repr__(self):
        return '%s:%s' % (self.addr, self.port)


def parse_list(filename):    
    ips = list()
    for line in open(filename):
        ip_pat = re.compile(
            r"([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})(\:[\d]{1,5})?")
        ips += ip_pat.findall(line)
    result = list()
    for ip in ips:
        addr = ip[0]
        port = ip[1].lstrip(':') if len(ip) > 1 else None
        if port:
            result.append(IpAddress(addr, port))
        else:
            result.append(IpAddress(addr))
    return result


def portcheck(ipaddress, port, proto=SOCK_STREAM):
    # Test to see if a connection can be made
    # Create new socket to attempt connection on TCP
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(1.0)
        sock.connect((ipaddress, port))
        sock.close()
        return True
    except:
        # Try to create new socket to attempt connection on UDP.
        if proto != SOCK_DGRAM:
            return portcheck(ipaddress, port, SOCK_DGRAM)
        return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '''Python Proxy Checker

Usage: pyroxychk.py <ips.txt>

 where <ips.txt> is a text filename including ip:port patterns.
'''
        exit()
    proxies = parse_list(sys.argv[1])
    for proxy in proxies:
        pong = bool(ping.do_one(proxy.addr, 1) < 1)
        if pong:
            port_available = portcheck(proxy.addr, proxy.port)
        print '[%s:%s] is alive? [ping %s] [port %s] ' % \
            (proxy.addr, proxy.port, pong, port_available)

