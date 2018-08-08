# certbot-dns-auth-automation

A collection of simple scripts for automating the DNS challenge response for creating or renewing certbot (Let's Encrypt) SSL certificates.

## The Problem

You want to use DNS authentication with certbot but you use a 3rd-party provider that doesn't easily support automation or (like me) you run your own DNS.

## The Solution

On your main DNS server(s) you create NS records for each of the `_acme-challenge` subdomains that points to another DNS server (BIND) which you run yourself. This is the last time you have to update the main DNS server(s) for certbot... now all validation go to your own server which exists for this limited purpose. Because our DNS server is most likely not on the same machine where we want to renew certificates, a small Python process listens on a given port for requests to alter the DNS zones accordingly.

## Setup

Let's assume you have two hosts: **Host A** is the webserver where certbot needs to generate certificates, and **Host B** is our new DNS server for handling the certbot TXT records.

### Host A (Webserver)

Copy these files to `/usr/local/bin/`:

    certbot-dns-authenticator.sh
    certbot_renew_all.sh
    certbot_new_cert.sh

Edit `certbot-dns-authenticator.sh` and set the `DNS_AUTH_HOST` variable to IP or name of your **Host B**:

    DNS_AUTH_HOST=yourssldns.com

### Host B (DNS)

You will need BIND and Python 3 with Flask (`pip install flask`).

1. Copy the `named.conf` file to your BIND configuration directory, replacing the two instances of _yourdomain.com_ with the domain you're creating certificates for. This section can be repeated as necessary.
2. Copy the template `yourdomain.com.zone` file to the BIND primary zone file directory, renaming the file and replacing the two instances of _yourdomain.com_ with the name used in #1 and instances of _yourssldns.com_ with this host's publicly-addressable name. This file may be copied and repeated as necessary for any number of domains.
3. Edit the `ssl_renewals.py` script to set the proper interface to listen on. The default will listen only on 127.0.0.1. **WARNING:** You should not expose this to the open Internet, it is meant to be run either on a local network or on a VPN interface only:

    daemon.run(host='127.0.0.1', port=8119)

The `ssl_renewals.py` script needs to be able to modify your BIND zone file(s) and restart BIND, so you'll have to ensure it has permissions to do so or run it as root as your own risk.

## Using

Assuming BIND and the `ssl_renewals.py` script are running on **Host B** and that you set up the NS record properly for the domain in question, it is now quite simple to generate or renew a certificate on **Host A**:

    certbot_new_cert.sh

Will prompt for interactive creation of a new certificate.

To renew all certificates without interaction:

    certbot_renew_all.sh

That's it! I hope this was helpful. Please submit an issue or pull request on GitHub if you have a problem or fix.

