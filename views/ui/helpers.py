# -*- coding: utf-8 -*-
import os
import platform
import datetime
import psutil

__VERSION__ = '0.1'
__STARTED__ = datetime.datetime.now()

# Helper functions
def make_info_dict(request):
    now = datetime.datetime.now()
    uptime = unicode(now - __STARTED__)
    uptime = uptime.split('.', 1)[0]
    py_ver = platform.python_version()
    pr_pid = psutil.Process().pid
    remote = request.remote_addr
    browser = request.user_agent

    uname = platform.uname()
    proc_type = uname[5]
    if proc_type == '':
        proc_type = uname[4];

    return { 'agent_version': __VERSION__,
             'uptime': uptime,
             'processor': proc_type,
             'node': uname[1],
             'system': uname[0],
             'release': uname[2],
             'python' : py_ver,
             'pid' : pr_pid,
             'remote': remote,
             'browser': browser}