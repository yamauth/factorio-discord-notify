# factorio-discord-notify
factorioのconsole-logを監視し、誰かがJOIN/LEAVEしたときDiscordへ通知するBotです。factorio headlessが動作しているサーバへのインストールが必須要件です。ディレクトリ構成や設定は、<conoha.jp>で構築したサーバを前提にしている。

## Usage
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
# grep ExecStart /etc/systemd/system/factorio.service
ExecStart=/bin/sh -c '/usr/bin/screen -DmS factorio /opt/factorio/factorio/bin/x64/factorio --start-server /opt/factorio/savedata/factorio_save --console-log /opt/factorio/factorio/console-log --server-settings /opt/factorio/factorio/data/server-settings.json'
```
その後、適宜、サービスを再起動する。
```
systemctl stop factorio.service
systemctl start factorio.service
```
### Make ``.env``
```
TOKEN=MTE2MTEw...
CHANNEL_ID=11610...
```