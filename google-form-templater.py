#!/usr/bin/env python
#
# Copyright (c) 2015 W. Trevor King <wking@tremily.us>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Create new Google Forms based on existing templates.

This script is configured with a ConfigParser INI file [1], which will
look something like:

  [auth]
  email = you@gmail.com
  password = your password

  [client]
  id = <the id you get from Google>.apps.googleusercontent.com
  secret = <the secret you get from Google>
  redirect_uri = https://your.registered/callback

You can specify the location of this config file on the command line
(with -c / --config), or use the default
~/.config/google-form-templater.conf.  The client credentials come
from setting up a new web application client in the Google Developers
Console [2].

http://www.google.com/forms/about/
https://developers.google.com/drive/

[1]: https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
[2]: https://console.developers.google.com/
"""

from __future__ import print_function

try:  # Python 3
    import configparser
except ImportError:  # Python 2
    import ConfigParser as configparser
import os

import requests_oauthlib


try:  # Python 2
    input = raw_input
except NameError:  # Python 3
    pass


# OAuth endpoints given in the Google API documentation
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
SCOPE = [
    'profile',
    'email',
]


def get_authorized_client(config):
    """Get an OAuth-authorized client

    Following
    http://requests-oauthlib.readthedocs.org/en/latest/examples/google.html
    """
    client = requests_oauthlib.OAuth2Session(
        client_id=config['client']['id'],
        scope=SCOPE,
        redirect_uri=config['client']['redirect_uri'])

    # redirect user for authorization
    authorization_url, state = client.authorization_url(
        url=AUTHORIZATION_BASE_URL,
        access_type='offline',    # offline for refresh token
        approval_prompt='force')  # force to always make user click authorize
    print('Please go here and authorize,', authorization_url)

    # get the authorization verifier code from the callback url
    redirect_response = input('Paste the full redirect URL here: ')

    # fetch the access token
    client.fetch_token(
        token_url=TOKEN_URL,
        client_secret=config['client']['secret'],
        authorization_response=redirect_response)

    return client


def main(config):
    client = get_authorized_client(config)
    # fetch a protected resource, e.g. user profile
    r = client.get('https://www.googleapis.com/oauth2/v1/userinfo')
    print(r.content)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        '-c', '--config', metavar='PATH',
        default=os.path.expanduser(os.path.join(
            '~', '.config', 'google-form-templater.conf')),
        help='path to the config file')

    args = parser.parse_args()

    cp = configparser.ConfigParser()
    cp.read(args.config)
    config = {}
    for section in cp.sections():
        config[section] = {}
        for option in cp.options(section):
            config[section][option] = cp.get(section, option)

    main(config=config)
