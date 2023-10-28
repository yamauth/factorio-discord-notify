# factorio-discord-notify
factorioのconsole-logを監視し、誰かがJOIN/LEAVEしたときDiscordへ通知するBotです。factorio headlessが動作しているサーバへインストールして利用します。facotiro自体のインストール方法から記します。

## Usage
### Install Package
```
sudo yum install git python3-pip -y
pip install python-dotenv discord.py
```

### Download files
```
cd /opt
sudo git clone https://github.com/yamauth/factorio-discord-notify.git
sudo curl -o factorio.tar -OL https://www.factorio.com/get-download/1.1.91/headless/linux64
sudo tar xf factorio.tar
sudo rm factorio.tar

sudo useradd factorio
sudo chown -R factorio:factorio factorio factorio-discord-notify
```

### Settings
```
sudo -u factorio ./factorio/bin/x64/factorio --create ./factorio/saves/save.zip
echo -e "TOKEN=YOUR_DISCORD_TOKEN_HERE\nCHANNEL_ID=YOUR_DISCORD_CHANNEL_ID_HERE" | sudo -u factorio tee factorio-discord-notify/.env

sudo cp factorio-discord-notify/factorio.service /etc/systemd/system
sudo cp factorio-discord-notify/factorio_discord_notify.service /etc/systemd/system

sudo systemctl enable factorio
sudo systemctl start factorio

# wait
ll factorio/console-log

sudo systemctl enable factorio_discord_notify
sudo systemctl start factorio
```