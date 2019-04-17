
Installation
---
```
sudo pip install git+https://github.com/synchrone/diskmond.git
sudo ln -s /usr/local/lib/python3.6/dist-packages/diskmond/diskmond.service /etc/systemd/system/diskmond.service
```

Configuration
----
```
mkdir -p /etc/systemd/system/diskmond.service.d
cat <<EOF > /etc/systemd/system/diskmond.service.d/override.conf
[Service]
Environment=DISKMON_INTERVAL=300
EOF
sudo systemctl daemon-reload
sudo systemctl restart diskmond
```
