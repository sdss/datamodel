# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Remote(object):
    """Class to run the remote command-line inteface.

    Parameters
    ----------
    hostname : str, default=wiki.sdss.org
        Set the wiki hostname
    space : str, optional
        Set the wiki space
    """
    
    def __init__(self, hostname="wiki.sdss.org", space = None, verbose = None):
        self.hostname = hostname
        self.space = space
        self.verbose = verbose
        self.set_netrc()
        self.set_credential()
        self.set_jsessionid()

    def set_netrc(self):
        logger.warn("REMOTE> .netrc file=%r" % getenv('NETRCFILE'))
        try: self.netrc = netrc(file = getenv('NETRCFILE'))
        except Exception as e:
            if self.verbose: logger.warn("REMOTE> netrc %r" % e)
            self.netrc = None

    def set_credential(self):
        self.credential = {'hostname': self.hostname, 'username': None, 'password': None}
        if self.hostname and self.netrc:
            authenticators = self.netrc.authenticators(self.hostname)
            if authenticators and len(authenticators) == 3:
                self.credential['username'] = authenticators[0]
                self.credential['password'] = authenticators[2]
                self.credential['***'] = "*" * len(self.credential['password'])
                if self.verbose:
                    logger.warn("REMOTE> authentication for hostname=%(hostname)r set for username=%(username)r password=%(***)r " % self.credential)
            else:
                if self.verbose: logger.warn("REMOTE> cannot find %r in ~/.netrc" % self.hostname)
                self.password = None
        else: self.password = None

    def set_jsessionid(self): pass
