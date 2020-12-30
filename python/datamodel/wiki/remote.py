# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from os import getenv
from os.path import join, exists, basename
from netrc import netrc
from subprocess import check_output


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Remote(object):
    """Class to run the remote command-line inteface.

    Parameters
    ----------
    hostname : str, default=wiki.sdss.org
        Set the wiki hostname
    """
    
    java = "/usr/bin/java"
    
    def __init__(self, hostname = None, verbose = None):
        self.hostname = hostname if hostname else "https://wiki.sdss.org"
        self.verbose = verbose
        self.set_netrc()
        self.set_credential()
        self.set_jar()

    def set_netrc(self):
        try: self.netrc = netrc(file = getenv('NETRCFILE'))
        except Exception as e:
            print("REMOTE> netrc %r" % e)
            self.netrc = None

    def set_credential(self):
        self.credential = {'user': None, 'password': None}
        if self.hostname:
            host = self.hostname.replace("https://", "") if self.hostname.startswith("https://") else self.hostname.replace("http://", "") if self.hostname.startswith("http://") else self.hostname
        else: host = None
        if host and self.netrc:
            authenticators = self.netrc.authenticators(host)
            if authenticators and len(authenticators) == 3:
                self.credential['user'] = authenticators[0]
                self.credential['password'] = authenticators[2]
                self.credential['***'] = "*" * len(self.credential['password'])
                if self.verbose:
                    print("REMOTE> credential set for user=%(user)r password=%(***)r " % self.credential)
            else:
                print("REMOTE> cannot find %r in .netrc" % host)
                self.credential = None
        else: self.credential = None
        
    def set_jar(self):
        try:
            cli_dir = getenv("CONFLUENCE_CLI_DIR")
            cli_ver = basename(cli_dir) if cli_dir and exists(cli_dir) else None
            jar = join(cli_dir, 'lib', "confluence-cli-%s.jar" % cli_ver)
            if not exists(jar):
                print("REMOTE> missing Confluence CLI library file")
                jar = None
        except:
            print("REMOTE> please set CONFLUENCE_CLI_DIR ")
            jar = None
        self.jar = [self.java, '-jar', jar, '--server', self.hostname] if jar and self.hostname else None


    def set_login(self):
        if self.credential and 'user' in self.credential and 'password' in self.credential:
            self.action = ["--action", "login"]
            self.login = ["--user", self.credential['user']]
            self.login += ["--password", self.credential['password']]
            self.set_command()
            self.set_response()
            self.login = ["--login", self.response]
        else:
            self.login = None

    def set_command(self):
        self.command = self.jar + self.action + self.login if self.jar and self.action and self.login else None

    def set_response(self):
        self.response = check_output(self.command,universal_newlines=True).rstrip() if self.command else None
