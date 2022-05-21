#!/usr/bin/env python3

import subprocess
from os import path
from plexapi.server import PlexServer
from discord_webhook import DiscordWebhook, DiscordEmbed

# Please ensure that the "anchor.lock" file is available in your mount's root (can change the path to anything)
# It is recommended to use the path using MergerFS as then the anchor file will be unavailable if either services go down
# -----------------------------------------------------------------------------
# Input Plex URL and token
baseurl = 'http://[PMS_IP_Address]:32400'
token = 'TOKEN'
# Path starts from home, this one is ~/MergerFS/anchor.lock
anchorPath = "/MergerFS/anchor.lock"
# Leave empty to not use Discord for logging. Paste in the webhook URL if it is in use.
webhookURL = ''

# This is used to check the the rclone and MergerFS services are running on the machine
# -----------------------------------------------------------------------------
# shell=True needs to be used if this script is in use with a crontab. Use shell=False if you are executing it from a terminal
rcloneCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "rclone-vfs.service"], shell=False)
mergerFSCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "mergerfs.service"], shell=False)

# Plex URL (SSL recommended), and Anchor file location
# -----------------------------------------------------------------------------
plex = PlexServer(baseurl, token)

# Edit this line to change the path of the mount to start from root instead
anchor = path.exists(path.expanduser('~') + anchorPath)

# Script
# -----------------------------------------------------------------------------
scriptStatus = 'Failed'

if anchor:
  anchorStatus = ':white_check_mark: Available'
  # The subprocess.call returns a 0 if the service is active
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

# This bit is for the discord embed, useful for logging during crontab use
if webhookURL:
  webhook = DiscordWebhook(url=DiscordWebhookURL, username='AutoTrash', avatar_url='https://github.com/specarino/AutoTrash/blob/main/assets/AutoTrash-128px.png?raw=True')
  
  def printe(scriptStatus, anchorStatus, serviceStatus):

    if scriptStatus == 'Success':
      embedColor = '03b2f8'
    else:
      embedColor = 'f84903'

    titleFull = 'Empty Trash Task: ' + scriptStatus + '!'
    embed = DiscordEmbed(title=titleFull, description="Automatic emptying of trash for Plex based on remote mount's availability", color=embedColor)
    embed.set_author(name='specarino/AutoTrash', url='https://github.com/specarino/AutoTrash/', icon_url='https://github.com/specarino.png?size=48')
    embed.set_timestamp()
    embed.add_embed_field(name="Anchor File (through MergerFS)", value=anchorStatus, inline=False)
    embed.add_embed_field(name="rclone & MergerFS Services", value=serviceStatus, inline=False)
    webhook.add_embed(embed)
    response = webhook.execute()
    
  printe(scriptStatus, anchorStatus, serviceStatus)
