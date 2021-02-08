# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from netrc import netrc
from os import getenv
from os.path import basename, exists, join
from subprocess import CalledProcessError, check_output


__author__ = "Joel Brownstein <joelbrownstein@sdss.org>"


class Remote(object):
    """Class to run the remote command-line inteface.

    Parameters
    ----------
    hostname : str, default=wiki.sdss.org
        Set the wiki hostname
    space : str, default=DATAMODEL
        Set the wiki space
    """

    java = "/usr/bin/java"
    PAGE_NOT_FOUND = 255

    def __init__(self, hostname=None, space=None, verbose=None):
        self.hostname = hostname if hostname else "https://wiki.sdss.org"
        self.space = space if space else "DATAMODEL"
        self.login = None
        self.command = None
        self.response = None
        self.error = None
        self.verbose = verbose
        self.set_netrc()
        self.set_credential()
        self.set_jar()

    def set_netrc(self):
        try:
            self.netrc = netrc(file=getenv("NETRCFILE"))
        except Exception as e:
            print("REMOTE> netrc %r" % e)
            self.netrc = None

    def set_credential(self):
        self.credential = {"user": None, "password": None}
        if self.hostname:
            host = (
                self.hostname.replace("https://", "")
                if self.hostname.startswith("https://")
                else self.hostname.replace("http://", "")
                if self.hostname.startswith("http://")
                else self.hostname
            )
        else:
            host = None
        if host and self.netrc:
            authenticators = self.netrc.authenticators(host)
            if authenticators and len(authenticators) == 3:
                self.credential["user"] = authenticators[0]
                self.credential["password"] = authenticators[2]
                self.credential["***"] = "*" * len(self.credential["password"])
                if self.verbose:
                    print(
                        "REMOTE> credential set for user=%(user)r password=%(***)r "
                        % self.credential
                    )
            else:
                print("REMOTE> cannot find %r in .netrc" % host)
                self.credential = None
        else:
            self.credential = None

    def set_jar(self):
        try:
            atlassian_dir = getenv("ATLASSIAN_DIR")
            atlassian_ver = (
                basename(atlassian_dir) if atlassian_dir and exists(atlassian_dir) else None
            )
            jar = join(atlassian_dir, "lib", "acli-%s.jar" % atlassian_ver)
            if not exists(jar):
                print("REMOTE> missing Atlassian lib jar file")
                jar = None
        except:
            print("REMOTE> please set ATLASSIAN_DIR ")
            jar = None
        self.jar = (
            [self.java, "-jar", jar, "confluence", "--server", self.hostname]
            if jar and self.hostname
            else None
        )

    def add_page(self, parent=None, title=None, content=None, convert=None):
        if self.space:
            if title and content:
                self.action = ["--action", "addPage", "--space", self.space]
                self.action += ["--title", title, "--content", content]
                self.action += ["--parent", parent] if parent else ["--parent", "@home"]
                if not convert:
                    self.action += ["--noConvert"]
                self.set_command()
                self.set_response()
                self.print_response_or_error()
                if self.error:
                    pass
                elif self.verbose:
                    print("PAGE> CREATED %s with parent=%r" % (title, parent))

    def set_pagelist(self, parent=None, title=None):
        if self.space:
            self.action = ["--action", "getPageList"]
            self.action += ["--space", self.space]
            if parent:
                self.action += ["--parent", parent]
            if title:
                self.action += ["--title", title]
            self.action += ["--outputFormat", "2"]
            self.set_command()
            self.set_response()
            if self.error:
                self.pagelist = None
            else:
                self.pagelist = self.get_data_from_response()
                if self.pagelist:
                    self.pagelist["parent"] = parent
                    if self.verbose:
                        print("REMOTE> %(summary)s for parent=%(parent)r" % self.pagelist)
        else:
            self.pagelist = None

    def get_data_from_response(self):
        keys = summary = None
        data = []
        if self.response:
            lines = self.response.split("\n")
            for index, line in enumerate(lines):
                if index > 1:
                    values = line.replace('"', "").split(",")
                    data.append(dict(zip(keys, values)))
                elif index:
                    keys = line.lower().replace('"', "").split(",")
                else:
                    summary = line
        return {"summary": summary, "data": data} if summary and data else None

    def set_login(self):
        if self.credential and "user" in self.credential and "password" in self.credential:
            self.action = ["--action", "login"]
            self.login = ["--user", self.credential["user"]]
            self.login += ["--password", self.credential["password"]]
            self.set_command()
            self.set_response()
            self.login = (
                ["--login", self.response]
                if not self.error and self.response.startswith("JSESSIONID")
                else None
            )
            if self.verbose:
                self.print_response_or_error()
        else:
            self.login = None

    def set_command(self):
        self.command = (
            self.jar + self.action + self.login if self.jar and self.action and self.login else None
        )

    def print_response_or_error(self):
        if self.response:
            print("REMOTE> %r" % self.response)
        elif self.error:
            print("REMOTE> %r" % self.error)

    def set_response(self):
        try:
            self.response = (
                check_output(self.command, universal_newlines=True).rstrip()
                if self.command
                else None
            )
            self.error = None
        except CalledProcessError as error:
            self.response = None
            self.error = error
            if self.error.stderr and self.error.stderr.endswith("not authorized."):
                print(
                    "REMOTE> Either your session has expired, or your credentials are not valid. "
                    "Please try a fresh session, or check the credentials in your netrc file."
                )
