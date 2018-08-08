#!/bin/sh
#
# Copyright (C) 2017-2018 Virgo Venture, Inc.
# @%@~LICENSE~@%@

certbot renew --preferred-challenges=dns --manual-auth-hook /usr/local/bin/certbot-dns-authenticator.sh

