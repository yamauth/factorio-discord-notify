# factorio-discord-notify
factorioが動作しているサーバにインストールすることで、factorioのconsole-logを監視して誰かがJOIN/LEAVEしたときにDiscordへ通知するBotです。

## How To Use
### Install Package
```
apt update
apt install python3-pip
pip install python-dotenv
pip install discord.py
```
### Edit service file
`/etc/systemd/system/factorio.service` の `ExecStart` に `--console-log /opt/factorio/factorio/console-log` の起動オプションを追加する。
```
# cat /etc/systemd/system/factorio.service
[Unit]
Description=Factorio Server
After=network.target nss-lookup.target

[Service]
Type=simple
User=factorio
Group=factorio
WorkingDirectory=/opt/factorio
ExecStart=/bin/sh -c '/usr/bin/screen -DmS factorio /opt/factorio/factorio/bin/x64/factorio --start-server /opt/factorio/savedata/factorio_save --console-log /opt/factorio/factorio/console-log --server-settings /opt/factorio/factorio/data/server-settings.json'
ExecStop=/usr/bin/screen -p 0 -S factorio -X eval 'stuff "/server-save\015"'
ExecStop=/bin/sleep 5
ExecStop=/usr/bin/screen -p 0 -S factorio -X eval 'stuff ^C'
ExecStop=/bin/sleep 5
Restart=always

[Install]
WantedBy=multi-user.target

```
その後、適宜、サービスを再起動する。
systemctl stop factorio.service
systemctl start factorio.service
