Model of local client + web server for visualization
================================

Sensor model connects to the mqtt broker to publish following messages (example):
--Cpu temperature (--ct)
--Cpu load (--cl)
--Virtual memory (--memo)

Update refresh rate is configurable in seconds within 1..100 sec. (--refr 1.5)

Requires running broker. Instructions how to run Mosquitto broker:
http://www.steves-internet-guide.com/install-mosquitto-linux/


Requirements:
---------------

- paho
- enum
- flask
- numpy
- pandas
- ipaddress
- argparse


How To Run:
------------

1. $ python remoteSensMain.py --host 192.168.0.14 -p 1883 --refr 1.5 --ct --cl --memo



