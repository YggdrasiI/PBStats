# Installation:

```
sudo apt install tcpdump
pip install .
```

# Usage

see `civpb-watchdog --help`

## Stopping the program:
  Long press(!) of Ctrl+C.

## Sketch for usage of pitboss_watchdog without sudo:

It runs with `AmbientCapabilities=CAP_NET_RAW`

## Alternatively

Give Python3 network access

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