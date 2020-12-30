# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from os import getenv
from netrc import netrc


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Remote(object):
    """Class to run the remote command-line inteface.

    Parameters
    ----------
    hostname : str, default=wiki.sdss.org
        Set the wiki hostname
    """
    
    def __init__(self, hostname = None, verbose = None):
        self.hostname = hostname if hostname else "wiki.sdss.org"
        self.verbose = verbose
        self.set_netrc()
        self.set_credential()
        self.set_jsessionid()

    def set_netrc(self):
        if self.verbose: print("REMOTE> .netrc file=%r" % getenv('NETRCFILE'))
        try: self.netrc = netrc(file = getenv('NETRCFILE'))
        except Exception as e:
            if self.verbose: print("REMOTE> netrc %r" % e)
            self.netrc = None

    def set_credential(self):
        self.credential = {'username': None, 'password': None}
        if self.hostname and self.netrc:
            authenticators = self.netrc.authenticators(self.hostname)
            if authenticators and len(authenticators) == 3:
                self.credential['username'] = authenticators[0]
                self.credential['password'] = authenticators[2]
                self.credential['***'] = "*" * len(self.credential['password'])
                if self.verbose:
                    if self.verbose: print("REMOTE> credential set for username=%(username)r password=%(***)r " % self.credential)
            else:
                if self.verbose: print("REMOTE> cannot find %r in ~/.netrc" % self.hostname)
                self.password = None
        else: self.password = None

    def set_jsessionid(self): pass
