#!/bin/bash
#
# Copyright (C) 2017-2018 Virgo Venture, Inc.
# @%@~LICENSE~@%@

# Passed-in environment variables we use:
# CERTBOT_DOMAIN
# CERTBOT_VALIDATION

DNS_AUTH_HOST=yourssldns.com

curl http://${DNS_AUTH_HOST}:8119/${CERTBOT_DOMAIN}/${CERTBOT_VALIDATION}

sleep 7s

