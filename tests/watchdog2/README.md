# Dependencies:
```
sudo apt install tcpdump
pip install .
```

## Example call:
```
sudo python3 civpb_watchdog.py eth0 192.168.0.2 ~/PBs/PB1,~/PBs/PB2
```

## Exit of programm:
  Long press(!) of Ctrl+C.

## Systemd service:
```
  make install_service|uninstall_service
  make start|stop|restart|log
```


# Sketch for usage of civpb_watchdog without sudo:

  # Python3 Netzwerkzugriff geben (das ist noch wie beim letzten mal)
```
  cp /usr/bin/python3 .
  sudo setcap cap_net_raw=+ep ./python3

  # tcpdump need also acces on network interfaces
  # Laut https://askubuntu.com/questions/530920/tcpdump-permissions-problem 
  sudo groupadd pcap
  sudo usermod -a -G pcap ramkhamhaeng

  sudo chgrp pcap /usr/sbin/tcpdump
  sudo chmod 750 /usr/sbin/tcpdump

  sudo setcap cap_net_raw=ep /usr/sbin/tcpdump
```
