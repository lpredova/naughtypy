#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import ConfigParser
import time

from bs4 import BeautifulSoup
import pytumblr


bot = False


# Parse configuration
def config_section_map(section):
    dict1 = {}
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def main():
    get_comment()


# Parse comments
def get_comment():
    consumer_key = config_section_map("tumblr")['consumer_key']
    consumer_secret = config_section_map("tumblr")['consumer_secret']
    oauth_token = config_section_map("tumblr")['oauth_token']
    oauth_secret = config_section_map("tumblr")['oauth_secret']

    client = pytumblr.TumblrRestClient(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret)

    try:
        page = urllib2.urlopen('http://www.pornhub.com/random').read()
        soup = BeautifulSoup(page, "lxml")

        if len(soup.select("div.commentMessage")) > 0:
            for s in soup.select("div.commentMessage")[0].stripped_strings:
                if len(s) > 10 and s != "[[commentMessage]]":  # I'm so sorry

                    image = soup.find("meta", {"name": "twitter:image"})['content']
                    url = soup.find("meta", {"name": "twitter:url"})['content']

                    client.create_photo("dailyrandomporn",
                                        tags=["random porn quotes", "dailyrandomporn", s, url],
                                        state="published", slug=soup.title,
                                        source=image, caption=url
                    )

                    print "Posted!"
                    time.sleep(5)
                    break
                else:
                    get_comment()
    except Exception, e:
        raise e


if __name__ == "__main__":
    main()