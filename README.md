<p align="center">
  <img width="64" height="64" src="https://github.com/specarino/AutoTrash/blob/main/assets/AutoTrash-128px.png?raw=True">
</p>

# AutoTrash
A small Python script to trash unavailable files on Plex. Although Plex does this automatically, it does not check for if the remote mount is active. Therefore having it on has the possibility of completely wiping out all of the metadata if the mount link ever breaks.

This piece of code is tailored to be used with rclone and MergerFS, although the idea is the same for other types of remote mount.

# Installation
Ensure that python3 and pip are installed on the machine. This script depends on two external libraries,

```bash
pip install plexapi
pip install discord-webhook
```

Create an anchor file on the remote mount. For instance, `anchor.lock` was placed in the root of the remote for this script development.

The following variables needs to be set for the script to work,
- `baseurl`: The URL of the Plex server (SSL is recommended here)
- `token`: Obtained by viewing the XML of a media and taking the token off of the URL
- `anchorPath`: File name and location of the anchor file on the mount/merged folder (suggested to use the merged folder)
- `DiscordWebhookURL`: A Discord webhook URL, can be left blank too
- `DiscordUserID`: Discord account's ID (used to ping the user), can be left blank too

# Configuration

## Manually running the code
To run the script from shell,

```bash
chmod +x AutoTrash.py
./AutoTrash.py
```

```
usage: AutoTrash.py [-h] [-s]

optional arguments:
  -h, --help   show this help message and exit
  -s, --shell  Invoke a shell, used for cron (default: False)
```

## Using cron setup
This is the recommended way of setting this up. For instance, this is how it is setup to run every 15 minutes. [crontab.guru](https://crontab.guru/) can be used to easily obtain the necessary interval.
```
*/15 * * * * /home/username/AutoTrash.py -s >> /dev/null 2>&1
```
Ensure the use of `-s` or `--shell`, as the `shell=True` flag needs to be used during the `subprocess.call`

This is due to the use of `--user` flag with the `systemctl` command. The script needs to run the command in a shell to have access to the right environmental variables. Otherwise, the following error will be displayed,
```
Failed to connect to bus: No such file or directory
```

# Discord Embed

The following image shows the Discord embed working, the first log is when the trash was cleared due to remote mount availability, and the second log did not clear the trash due to lack of an anchor file.

<p align="center">
  <img src="https://github.com/specarino/AutoTrash/blob/main/assets/AutoTrash_Example_V2.jpg?raw=True">
</p>
