# factorio-discord-notify
factorioのconsole-logを監視し、誰かがJOIN/LEAVEしたときDiscordへ通知するBotです。factorio headlessが動作しているサーバへインストールして利用します。
本Botをsystemdに登録するserviceファイルだけではなく、factorio本体をsystemdに登録するserviceファイルも含みます。
README.mdのUsageには、facotiro本体のインストールと、サードパーティ製のアップデートスクリプト（factorio-updater）の設定を含みます。

## Usage
### Install Package
```
sudo yum install git python3-pip -y
pip install python-dotenv discord.py requests
```

### Download files
```
cd /opt
sudo git clone https://github.com/yamauth/factorio-discord-notify.git
sudo git clone https://github.com/narc0tiq/factorio-updater.git
sudo curl -o factorio.tar -OL https://www.factorio.com/get-download/1.1.91/headless/linux64
sudo tar xf factorio.tar
sudo rm factorio.tar

sudo useradd factorio
sudo chown -R factorio:factorio factorio factorio-discord-notify factorio-updater
```

### Update files
```
sudo -u factorio python3 factorio-updater/update_factorio.py --apply-to factorio/bin/x64/factorio
```

### Settings
```
sudo -u factorio ./factorio/bin/x64/factorio --create ./factorio/saves/save.zip
echo -e "TOKEN=__YOUR_DISCORD_TOKEN_HERE__\nCHANNEL_ID=__YOUR_DISCORD_CHANNEL_ID_HERE__" | sudo -u factorio tee factorio-discord-notify/.env

sudo cp factorio-discord-notify/factorio.service /etc/systemd/system
sudo cp factorio-discord-notify/factorio_discord_notify.service /etc/systemd/system

sudo systemctl enable factorio
sudo systemctl start factorio

# wait
ll factorio/console-log

sudo systemctl enable factorio_discord_notify
sudo systemctl start factorio_discord_notify
```

## When factorio update
```
cd /opt
sudo systemctl stop factorio
sudo -u factorio python3 factorio-updater/update_factorio.py --apply-to factorio/bin/x64/factorio
sudo systemctl start factorio
```