#!/bin/bash
#while :
#do
    #lsusb -d 03eb:2ff0
    grep -e "32U2" /sys/bus/usb/devices/*/product
    if [ $? -eq 0 ]
    then
      dfu-programmer atmega32u2 erase
      dfu-programmer atmega32u2 flash $1
      dfu-programmer atmega32u2 reset
      dfu-programmer atmega32u2 reset
      dfu-programmer atmega32u2 reset
      echo 32U2 DFU Found!
    else
      echo 32U2 DFU Not found
    fi

#    sleep .1
    #read -n 1 -s
#    clear
#done
