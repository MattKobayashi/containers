#! /usr/bin/env python3

import re
import json
from os import environ
from sys import exit
from datetime import datetime, timedelta
from time import mktime
import http.client
import urllib
import feedparser


def is_within_one_hour(target_datetime):
    """
    Checks if a datetime object is within one hour of the current time.

    Args:
      target_datetime: A datetime object representing the target date and time.

    Returns:
      True if the target datetime is within one hour of the current time,
      False otherwise.
    """
    now = datetime.now()
    # Add and subtract an hour from the current time using timedelta
    one_hour_before = now - timedelta(hours=1)
    one_hour_after = now + timedelta(hours=1)
    # Check if the target datetime falls within this one-hour window
    return one_hour_before <= target_datetime <= one_hour_after


if not environ['PUSHOVER_APP_TOKEN'] or not environ['PUSHOVER_USER_KEY']:
    print(
        "ERROR: Please set the PUSHOVER_APP_TOKEN",
        "and PUSHOVER_USER_KEY environment variables."
        )
    exit()

blog_feed = feedparser.parse("https://blog.vyos.io/tag/release/rss.xml")
latest_post = blog_feed.entries[0]

print(f"Latest blog entry: {latest_post.title}")
print(f"Published: {latest_post.published}")

if is_within_one_hour(
    datetime.fromtimestamp(mktime(latest_post.published_parsed))
):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode({
            "token": f"{environ['PUSHOVER_APP_TOKEN']}",
            "user": f"{environ['PUSHOVER_USER_KEY']}",
            "message": f"""
                There's a new post on the VyOS blog. Link: {latest_post.link}
            """,
            }),
        {"content-type": "application/x-www-form-urlencoded"}
    )
    conn.getresponse()

    if "1.3" in latest_post.title:
        conn2 = http.client.HTTPSConnection(
            "api.github.com:443"
        )
        conn2.request(
            "POST",
            "/repos/MattKobayashi/vyos-autobuild/dispatches",
            json.dumps({
                "event_type": "1.3 Blog Release",
                "client_payload": {
                    "version": next(
                        i for i
                        in latest_post.title.split(" ")
                        if re.match(r"1\.3\.[0-9]{1,2}", i)
                    )
                }
            }),
            {
                "User-Agent": "vyos-release-alert",
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {environ['GITHUB_PAT']}",
                "Content-Type": "application/vnd.github+json"
            }
        )
        print(
            "Triggered new autobuild for VyOS 1.3:",
            "https://github.com/MattKobayashi/vyos-autobuild/actions"
        )

    if "1.4" in latest_post.title:
        conn2 = http.client.HTTPSConnection(
            "api.github.com:443"
        )
        conn2.request(
            "POST",
            "/repos/MattKobayashi/vyos-autobuild/dispatches",
            json.dumps({
                "event_type": "1.4 Blog Release",
                "client_payload": {
                    "version": next(
                        i for i
                        in latest_post.title.split(" ")
                        if re.match(r"1\.4\.[0-9]{1,2}", i)
                    )
                }
            }),
            {
                "User-Agent": "vyos-release-alert",
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {environ['GITHUB_PAT']}",
                "Content-Type": "application/vnd.github+json"
            }
        )
        print(
            "Triggered new autobuild for VyOS 1.4:",
            "https://github.com/MattKobayashi/vyos-autobuild/actions"
        )
