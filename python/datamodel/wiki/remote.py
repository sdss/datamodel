# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from os import getenv
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
    
    def __init__(self, hostname = None, verbose = None):
        self.hostname = hostname if hostname else "wiki.sdss.org"
        self.verbose = verbose
        self.set_netrc()
        self.set_credential()
        self.set_jar()
        self.set_login()

    def set_netrc(self):
        try: self.netrc = netrc(file = getenv('NETRCFILE'))
        except Exception as e:
            print("REMOTE> netrc %r" % e)
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
                    print("REMOTE> credential set for username=%(username)r password=%(***)r " % self.credential)
            else:
                print("REMOTE> cannot find %r in ~/.netrc" % self.hostname)
                self.password = None
        else: self.password = None
        
    def set_jar(self):
        try:
            cli_dir = getenv("CONFLUENCE_CLI_DIR)
            jar = join(cli_dir, 'lib', "confluence-cli-%s.jar" % cli_dir)
            if not exists(jar):
                print("REMOTE> missing Confluence CLI library file")
                jar = None
        except:
            print("REMOTE> please set CONFLUENCE_CLI_DIR ")
            jar = None
        self.jar = ['java', '-jar', jar, '--server', self.hostname] if jar and self.hostname else None

    def submit(self):
        job_dir = self.get_job_dir()
        job_file = self.get_job_file()
        if not exists(job_dir): self.append_error("ERROR: Missing job dir at %s" % job_dir)
        elif not exists(job_file): self.append_error("ERROR: Missing job file at %s" % job_file)
        else:
            if self.job.dir and exists(self.job.dir): chdir(self.job.dir)
            submit_command = [Client.config.submit_command,job_file]
            if vendor=='moab': submit_command += ['-o',job_dir]
            submit_output = check_output(submit_command,universal_newlines=True).rstrip()
            self.job = Job.query.get(self.job.id)
            self.job.identifier = Client.config.identifier_from_submit_output(submit_output)
            self.job.status = 3
            self.job.commit()
            self.submitted = True

    def set_login(self):
        if self.credential and 'username' in self.credential and 'password' in self.credential:
            self.action = ["--action", "login"]
            self.login = ["--username", self.credential['username']]
            self.login += ["--password", self.credential['password']]
            self.set_command()
            self.set_response()
            self.login = ["--login", self.response]
        else:
            self.login = None

    def set_command_output(self):
        self.command = self.jar + self.action + self.login if self.jar and self.action and self.login else None

    def set_response(self):
        self.response = check_output(self.command,universal_newlines=True).rstrip() if self.command else None
