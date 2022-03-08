# title.py

import html
import re

from bobbit.utils import strip_html

# Metadata

NAME    = 'title'
ENABLE  = True
PATTERN = r'.*(?P<url>http[^\s]+).*'
USAGE   = '''Usage: <url>
Looks up title of URL.
Example:
    > http://www.insidehighered.com/quicktakes/2019/06/24/uc-santa-cruz-removes-catholic-mission-bell
    Title: UC Santa Cruz Removes Catholic Mission Bell
'''

# Constants

CHANNEL_BLACKLIST = []
DOMAIN_BLACKLIST  = ['reddit.com', 'twitter.com']
AVOID_EXTENSIONS  = ('.gif', '.jpg', '.mkv', '.mov', '.mp4', '.png')

# Command

async def title(bot, message, url=None):
    if message.channel in CHANNEL_BLACKLIST or \
        any(url.lower().endswith(extension) for extension in AVOID_EXTENSIONS) or \
        any(domain in url for domain in DOMAIN_BLACKLIST):
        return

    async with bot.http_client.get(url) as response:
        try:
            text       = (await response.text()).replace('\n', ' ')
            html_title = re.findall(r'<title[^>]*>([^<]+)</title>', text)[0]
            response   = bot.client.format_text(
                '{color}{green}Title{color}: {bold}{title}{bold}',
                title = strip_html(html.unescape(html_title)).strip()
            )
        except (IndexError, ValueError):
            return

        return message.with_body(response)

# Register

def register(bot):
    global CHANNEL_BLACKLIST

    config = bot.config.load_module_config('title')
    CHANNEL_BLACKLIST = config.get('blacklist', CHANNEL_BLACKLIST)

    if config.get('disabled', False):
        return []

    return (
        ('command', PATTERN, title),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
