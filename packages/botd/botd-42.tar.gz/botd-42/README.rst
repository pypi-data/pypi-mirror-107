README
######

Welcome to BOTD,

BOTD is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel, it can be used to display RSS feeds,
act as a UDP to IRC relay and you can program your own commands for it.

note: as of version 42 BOTD uses an internal bot package instead of botl.
      if you want to use previous data change botl and botd to bot in 
      /var/lib/botd/store.

BOTD is placed in the Public Domain and has no COPYRIGHT and no LICENSE. 

INSTALL
=======

installation is through pypi::

 $ sudo pip3 install botd --upgrade --force-reinstall

CONFIGURE
=========

BOTD has it's own CLI, the botctl program you can run it on the shell prompt 
and, as default, it won't do anything:: 

 $ sudo botctl
 $ 

use botctl <cmd> to run a command directly, e.g. the cmd command shows
a list of commands::

 $ sudo botctl cmd
 cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,krn,log,met,mod,rem,rss,thr,ver,upt

configuration is done with the cfg command::

 $ sudo botctl cfg server=botd.openbsd.amsterdam channel=\#botd nick=botd
 ok

if the users option is set in the irc config then users need to be added 
before they can give commands, use the met command::

 $ sudo botctl met ~botfather@jsonbot/daddy
 ok

RSS
===

BOTD provides, with the use of feedparser, the possibility to serve rss
feeds in your channel::

 $ sudo apt install python3-feedparser

to add an url use the rss command with an url::

 $ sudo botctl rss https://github.com/bthate/botd/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ sudo botctl fnd rss
 0 https://github.com/bthate/botd/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ sudo botctl ftc
 fetched 20

UDP
===

BOTD also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
output to the IRC channel is done with the use python3 code to send a UDP
packet to BOTD, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

COMMANDS
========

BOTD, on purpose, doesn't read modules from a directory, instead you must
include your own written commands with a updated version fo the code.

Use the repository at github to get the latest repo and install setuptools::

 $ git clone http://github.com/bthate/botd
 $ cd botd
 $ sudo apt install python3-setuptools
 
to program your own commands, open bot/hlo.py and add the following code::

    def register(k):
        k.regcmd(hlo)

    def hlo(event):
        event.reply("hello %s" % event.origin)

add the command in the bot/all.py module::

    import bot.hlo

    Kernel.addmod(bot.hlo)

edit the list of modules to load in bin/bot or bin/botd:

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,hlo"

install the bot on the system with install::

 $ sudo python3 setup.py install

now you can type the "hlo" command, showing hello <user>::

 $ bot hlo
 hello root@console

SYSTEMD
=======

to run BOTD 24/7 you need to enable the BOTD service under systemd, edit 
/etc/systemd/system/botd.service and add the following txt::

 [Unit]
 Description=BOTD - 24/7 channel daemon
 After=multi-user.target

 [Service]
 DynamicUser=True
 StateDirectory=botd
 LogsDirectory=botd
 CacheDirectory=botd
 ExecStart=/usr/local/bin/botd
 CapabilityBoundingSet=CAP_NET_RAW

 [Install]
 WantedBy=multi-user.target

then enable the bot with::

 $ sudo systemctl enable botd
 $ sudo systemctl daemon-reload
 $ sudo systemctl restart botd

disable botd to start at boot with removing the service file::

 $ sudo rm /etc/systemd/system/botd.service

RC.D
====

BOTD also runs on BSD albeit it is secondary to running under systemd::

 # cp files/rc.d/botd /etc/rc.d/botd
 # chmod +x /etc/rc.d/botd
 # groupadd botd
 # useradd -b /var/lib -d /var/lib/botd -w -g botd botd
 # chown -R botd:botd /var/lib/botd
 # rcctl enable botd
 # rcctl start botd

CONTACT
=======

if you have any questions or want to report bugs etc. you can write me at::

 Bart Thate (bthate@dds.nl, thatebart@gmail.com)

or contact me on irc (could take some time to respond)::

 botfather on #dunkbots irc.freenode.net
