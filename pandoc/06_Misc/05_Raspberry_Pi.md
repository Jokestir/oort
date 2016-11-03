# Raspberry Pi



## 1. How to flash OS to raspberry pi?



1. download raspbian OS img file from:  https://www.raspberrypi.org/downloads/raspbian/
2. download win32diskimager from: http://sourceforge.net/projects/win32diskimager/
3. Run win32diskimager as admin
4. insert sd card into adapter and insert it inside the laptop
5. Run the win32diskimager facility
6. select the drive letter of sd card and img file as downloaded file
7. press write. after write is successul, insert sd card in the raspberry pi and power it up
8. Now either control the Pi through screen, keyboard and mouse or through *ssh*.





## 2. How to ssh to pi?



1. connect the Pi to the router using ethernet cable
2. find out the ip address of the Pi using the router login page or Ipscanner tool. 
3. ssh into the Pi using terminal: 192.168.1.2 as example. If you get connection refused error, ssh is disabled on the OS.
4. default usernanme: pi , default password: raspberry. Veni. Vedi. Vici.
5. Change the username and password using : sudo raspi-config > change password.
6. Increase file size: sudo raspi-config > increase root size



## 3. How to setup wlan dongle with Pi?



1. Insert Wi-Fi dongle in one of the USB ports
2. Update the interface file as: sudo nano /etc/network/interfaces

    Replace everything with:


                            auto lo

                            iface lo inet loopback
                            iface eth0 inet dhcp
       
                            auto wlan0
                            iface wlan0 inet dhcp
                            wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
       
                            # optional
                            iface default inet static
                            address 192.168.1.2
                            netmask 255.255.255.0
                            gateway 192.168.1.1

Type: Ctrl + X
Type: Y

3. Update wpa_supplicant file: sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

    Replace everything with:

                            ctrl_interface=/var/run/wpa_supplicant
                            ctrl_interface_group=0
                            update_config=1
       
                            network={
                                      ssid="LOLWA"
                                      psk="roflcopter"
                            }

    Type: Ctrl + X
    Type: Y

4. Reboot: sudo reboot

5. Reconnect using terminal.

6. Run ifconfig wlan0 to check if it is connected. If connected IP address for wlan address will be shown



### wlan commands:



1. check scan results: sudo iwlist wlan0 scan | grep ESSID
2. check current status of wlan: ifconfig wlan0 or iwconfig
3. Turn off wlan: sudo ifdown wlan0
4. Turn on wlan : sudo ifup wlan0



## 4. How to reserve IP address of Pi on the router



1. Go to Advanced settings > LAN setup > Reserve devices. Add details such as device name, MAC address, ip address to be assigned etc.
2. Apply
