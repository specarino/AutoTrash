![AutoTrash](https://github.com/specarino/AutoTrash/blob/main/assets/AutoTrash-128px.png?size=48)

# AutoTrash
A small Python script to trash unavailable files on Plex. Although Plex does this automatically, it does not check for if the remote mount is active. Therefore having it on has the possibility of completely wiping out all of the metadata if the mount link ever breaks.

This piece of code is tailored to be used with rclone and MergerFS, although the idea is the same for other types of remote mount.

# Installation
Ensure that python3 and pip are installed on the machine. This script depends on two external libraries,

```bash
pip install plexapi
pip install discord-webhook
```

The following variables needs to be set for the script to work,
- `baseurl`: The URL of the Plex server (SSL is recommended here)
- `token`: Obtained by viewing the XML of a media and taking the token off of the URL
- `anchorPath`: File name and location of the anchor file on the mount/merged folder (suggested to use the merged folder)
- `webhookURL`: A Discord webhook URL, can be left blank too

# Configuration

## Manually running the code
To run the script from shell,

```bash
chmod +x AutoTrash.py
./AutoTrash.py
```

This will only work if the following lines have `shell=False` set,

```python
rcloneCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "rclone-vfs.service"], shell=False)
mergerFSCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "mergerfs.service"], shell=False)
```

## Using cron setup
This is the recommended way of setting this up. For instance, this is how it is setup to run every 15 minutes. [crontab.guru](https://crontab.guru/) can be used to easily obtain the necessary interval.
```
*/15 * * * * /home/username/AutoTrash.py >> /dev/null 2>&1
```
However, to do this a change needs to be made in the script. The `shell=True` flag needs to be used during the `subprocess.call`

```python
rcloneCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "rclone-vfs.service"], shell=True)
mergerFSCheck = subprocess.call(["systemctl", "--user", "--quiet", "is-active", "mergerfs.service"], shell=True)
```
