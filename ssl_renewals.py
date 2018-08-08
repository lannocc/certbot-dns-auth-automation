#!/usr/bin/env python3
#
# Copyright (C) 2017-2018 Virgo Venture, Inc.
# @%@~LICENSE~@%@

from datetime import datetime
from flask import Flask
from subprocess import call

daemon = Flask(__name__)

@daemon.route("/<path:path>")
def renew(path):
    print("ssl update request: {}".format(path))

    domain, key = path.split('/', 1)
    now = datetime.now()

    with open('/etc/bind/pri/{}.zone'.format(domain)) as zonefile:
        zone = zonefile.read().splitlines()

    with open('/etc/bind/pri/{}.zone'.format(domain), 'w') as zonefile:
        for line in zone:

            if line.endswith("; serial number"):
                line = "               {}00 ; serial number".format(now.strftime("%Y%m%d"))

            elif line.startswith(" IN TXT "):
                line = ' IN TXT "{}"'.format(key)

            print(line, file=zonefile)

    call(["/etc/init.d/named", "reload"])

    return "success"


daemon.run(host='127.0.0.1', port=8119)

