# **AutoForest** 


To use this bot better choose Linux based OS.

## **Install**##

0) Python 3
		 sudo apt install python3 

1) Telegram-cli (from @vysheng) by official guide:
https://github.com/vysheng/tg/

for UBUNTU:
```shell
 git clone --recursive https://github.com/vysheng/tg.git && cd tg
		
 sudo apt-get install libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libpython-dev make 
```  

Go to /loc/to/tg and there:
```shell
 ./configure && make
```  
if having issues try:
```shell
 git clone --recursive https://github.com/vysheng/tg.git
 cd tg
 wget -O openssl.patch 'https://aur.archlinux.org/cgit/aur.git/plain/telegram-cli-git.patch?h=telegram-cli-git'
 patch -p1 < openssl.patch
 ./configure && make
```  

try to use telegram-cli by going to /loc/to/tg/bin/ and calling
```shell
 ./telegram-cli
```
if everything works fine you are ready for the next step.

2) PyTg by official guide:
https://github.com/luckydonald/pytg

for UBUNTU:
```shell
 pip install pytg
 git clone https://github.com/luckydonald/pytg.git && cd pytg
```
to update:
```shell
 git pull
 sudo python setup.py install
```

3) Finally the AutoForest bot
for UBUNTU:
```shell
 git clone https://github.com/SergySanJj/AutoForest.git && cd AutoForest

Open ports for telegram-cli by going to /loc/to/tg/bin/ then
```shell
 ./telegram-cli --json -P 4458
```
Go to /loc/to/AutoForest/ then:
```shell
 python3 autoforest.py
```

Now AutoForest will run until you Ctrl-Z or shut down terminal.

Feel free to post issues, fork, pull etc.
