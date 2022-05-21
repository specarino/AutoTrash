#!/usr/bin/env python3

import sys
import socket
import subprocess
from os import path
from plexapi.server import PlexServer
from discord_webhook import DiscordWebhook, DiscordEmbed

# Please ensure that the "anchor.lock" file is available in your mount's root (can change the path to anything)
# It is recommended to use the path using MergerFS as then the anchor file will be unavailable if either services go down
# Input Plex token here, https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
# -----------------------------------------------------------------------------
token = 'PLEX_TOKEN_HERE'
# Path starts from home, this one is ~/MergerFS/anchor.lock
anchorPath = "/MergerFS/anchor.lock"
webhook = DiscordWebhook(url='DISCORD_WEBHOOK_URL_HERE')

# This is used to check the the rclone and MergerFS services are running on the machine
# -----------------------------------------------------------------------------
# shell=True needs to be used if this script is in use with a crontab. Use shell=False if you are executing it from a terminal
rcloneCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "rclone-vfs.service"], shell=True)
mergerFSCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "mergerfs.service"], shell=True)

# Plex URL, and Anchor file location
# -----------------------------------------------------------------------------
baseurl = 'http://plexserver:32400'
plex = PlexServer(baseurl, token)

anchor = path.exists(path.expanduser('~') + anchorPath)

# Script
# -----------------------------------------------------------------------------
# This bit is for the discord embed, useful for logging during crontab use
def printe(scriptStatus, anchorStatus, serviceStatus):

  if scriptStatus == 'Success':
    embedColor = '03b2f8'
  else:
    embedColor = 'f84903'

  titleFull = 'Empty Trash Task: ' + scriptStatus + '!'
  embed = DiscordEmbed(title=titleFull, description="Automatic emptying of trash for Plex based on remote mount's availability", color=embedColor)
  embed.set_author(name='AutoTrash by specarino', url='https://github.com/specarino/AutoTrash/', icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px-Python-logo-notext.svg.png')
  embed.set_timestamp()
  embed.add_embed_field(name="Anchor File (through MergerFS)", value=anchorStatus, inline=False)
  embed.add_embed_field(name="rclone & MergerFS Services", value=serviceStatus, inline=False)
  webhook.add_embed(embed)
  response = webhook.execute()

scriptStatus = 'Failed'

if anchor:
  anchorStatus = ':white_check_mark: Available'
  if rcloneCheck == 0 and mergerFSCheck == 0:
    serviceStatus = ':white_check_mark: Active'
    # The API call to empty the trash for all the libraries
    plex.library.emptyTrash()
    scriptStatus = 'Success'
  else:
    serviceStatus = ':x: Inactive'
else:
  anchorStatus = ':x: Unavailable'
  if rcloneCheck == 0 and mergerFSCheck == 0:
    serviceStatus = ':white_check_mark: Active'
  else:
    serviceStatus = ':x: Inactive'

printe(scriptStatus, anchorStatus, serviceStatus)
