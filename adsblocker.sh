#!/bin/bash

echo "...Start..."
sudo apt-get update
sudo apt-get upgrade -y

echo "...Installing Bind9..."
# Install Bind9 (DNS Server)
sudo apt-get install -y bind9

echo "...Copying Configuration Files..."
sudo cp named.conf /etc/bind/named.conf
sudo cp adsblocker.py /etc/bind/adsblocker.py

echo "...Fetch updated domain list..."
sudo python3 adsblocker.py

echo "...Restart Services..."
sudo systemctl restart named

sudo systemctl restart bind9

echo "...Verify Data..."
sudo named-checkconf
sudo named-checkzone rpz /etc/bind/adsblocker.db

#Schedule Cron Job to fetch updated domain list
echo "...Set Cronjob for future update..."
sudo crontab -l > adblocker
#cron job which will run at 00:00 on Sunday.
echo "0 0 * * 0 sudo python3 /etc/bind/adsblocker.py >> /etc/bind/adsblocker.log" >> adblocker
#install new cron file
sudo crontab adblocker

sudo rm adblocker
echo "...Finish..."



