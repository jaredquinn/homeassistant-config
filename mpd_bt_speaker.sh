#!/bin/bash

ACTION=$1
SPEAKER=$2

case $SPEAKER in
	echo)  	        USE_BT=0; SPEAKER_ID=3; MPD_HOSTS="/var/run/mpd/socket";;
	bathroom)  	USE_BT=0; BT="00:58:56:4C:C0:91"; CONTROLLER="00:1A:7D:DA:71:13"; SPEAKER_ID=2; MPD_HOSTS="/var/run/mpd/socket";;
	bathannounce)   USE_BT=0; MPD_HOSTS="/var/run/mpd/announce-socket";;
	#bathroom)  USE_BT=0; BT="00:58:56:4C:C0:91"; CONTROLLER="00:1A:7D:DA:71:13"; SPEAKER_ID=2; MPD_HOSTS="/var/run/mpd-announce/socket /var/run/mpd/socket";;
	*)         echo "Unknown Speaker $SPEAKER."; exit 3;;
esac

case $ACTION in
	connect)   
		   if [ $USE_BT == 1 ]; then
			   echo -e "select $CONTROLLER\nconnect $BT" | bluetoothctl
		           sleep 5
	           fi
		   for i in $MPD_HOSTS
	           do
	 	     mpc --host=$i pause
	 	     mpc --host=$i enable $SPEAKER_ID
	 	     mpc --host=$i play
		   done
		   ;;

	disconnect)   
		   for i in $MPD_HOSTS
	           do
	 	     mpc --host=$i pause
	 	     mpc --host=$i disable $SPEAKER_ID
	 	     mpc --host=$i play
		   done
		   if [ $USE_BT == 1 ]; then
			   echo -e "select $CONTROLLER\ndisconnect $BT" | bluetoothctl
		   fi
		   ;;

 	*) 	   echo "Unknown Action $ACTION."; exit 4;;
esac



