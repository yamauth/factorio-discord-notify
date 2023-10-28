#!/bin/bash

# APTパッケージのアップデート
yum update -y

# GitとPython3-Pipのインストール
yum install -y python3-pip

# Pythonパッケージのインストール
pip install python-dotenv discord.py

# GitHubリポジトリのクローン
git clone https://github.com/yamauth/factorio-discord-notify.git

# factorio_discord_notify.serviceの設定
cp factorio-discord-notify/factorio_discord_notify.service /etc/systemd/system/
systemctl daemon-reload

# factorio.serviceのExecStartにオプション追加
sed -i 's/ExecStart=\/bin\/sh -c '\''\/usr\/bin\/screen -DmS factorio /opt/factorio/factorio/bin\/x64\/factorio --start-server \/opt/factorio\/savedata\/factorio_save'\''/ExecStart=\/bin\/sh -c '\''\/usr\/bin\/screen -DmS factorio /opt/factorio/factorio/bin\/x64\/factorio --start-server \/opt\/factorio\/savedata\/factorio_save --console-log \/opt\/factorio\/factorio\/console-log'\''/' /etc/systemd/system/factorio.service

# factorio_discord_notify.serviceの有効化
systemctl enable factorio_discord_notify.service

# factorio.serviceの停止と再起動
systemctl stop factorio.service
systemctl start factorio.service

if [ $? -eq 0 ]; then
    echo "設定が正常に完了しました。"
else
    echo "設定の適用中にエラーが発生しました。"
fi