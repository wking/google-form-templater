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

You can specify the location of this config file on the command line
(with -c / --config), or use the default
~/.config/google-form-templater.conf.

http://www.google.com/forms/about/
https://developers.google.com/drive/

[1]: https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
"""

try:  # Python 3
    import configparser
except ImportError:  # Python 2
    import ConfigParser as configparser
import os


def main(config):
    print(config)


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
