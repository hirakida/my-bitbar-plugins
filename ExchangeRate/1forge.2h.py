#!/usr/local/bin/python3

import configparser
import json
import os
import urllib.request
import urllib.parse
import urllib.error
from builtins import ValueError
from datetime import datetime

CONFIG_FILE = "~/.bitbarrc"
PAIRS = "USDJPY,EURJPY"


def get_api_key():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))
    if not config.has_option("1forge", "api_key"):
        raise ValueError("api_key not found.")
    return config["1forge"]["api_key"]


def main():
    api_key = get_api_key()
    url = "http://forex.1forge.com/1.0.3/quotes"
    params = urllib.parse.urlencode({"pairs": PAIRS, "api_key": api_key})
    req = urllib.request.Request("{}?{}".format(url, params))
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode("utf8")
            rates = json.loads(content)
            for rate in rates:
                print("{0}: {1}".format(rate["symbol"], rate["price"]))
                print("bid: {0}".format(rate["bid"]))
                print("ask: {0}".format(rate["ask"]))
                print("{0}".format(datetime.fromtimestamp(rate["timestamp"])))
                print("---")
    except urllib.error.HTTPError as err:
        print(err.reason)
    except urllib.error.URLError as err:
        print(err.reason)


if __name__ == '__main__':
    main()
