#!/bin/sh

MAX_USERS=${MAX_USERS:-500}
HUB_NAME=${HUB_NAME:-}
HUB_ADDR=${HUB_ADDR:-}
TCP_PORTS=${TCP_PORTS:-411}
UDP_PORTS=${UDP_PORTS:-0}
ADMIN_NICK=${NICK:-Admin}
ENCODING=${ENCODING:-cp1252} # Use `iconv -l` to see the list of acceptable encodings on your OS

if [ ! -d /config/cfg ]
then

	if [ -z ${HUB} ]
	then
		echo "You must specify a hub name using the HUB environment variable. Exiting..."
		exit 1
	fi

	if [ -z ${HUB_ADDR} ]
	then
		echo "You must specify a hub address using the HUB_ADDR environment variable. Exiting..."
		exit 1
	fi

	sed -i -e '/#MaxUsers	=	500/c MaxUsers	=	${MAX_USERS}' /config/cfg/Settings.pxt
	sed -i -e '/#HubName	=	<Enter hub name here>/c HubName	=	${HUB_NAME}' /config/cfg/Settings.pxt
	sed -i -e '/#HubAddress	=	<Enter hub address here>/c HubAddress	=	${HUB_ADDR}' /config/cfg/Settings.pxt
	sed -i -e '/#TCPPorts	=	1209;411/c TCPPorts	=	${TCP_PORTS}' /config/cfg/Settings.pxt
	sed -i -e '/#UDPPort	=	0/c UDPPort	=	${UDP_PORTS}' /config/cfg/Settings.pxt
	sed -i -e '/#AdminNick	=	Admin/c AdminNick	=	${ADMIN_NICK}' /config/cfg/Settings.pxt
	sed -i -e '/#Encoding	=	cp1252/c Encoding	=	${ENCODING}' /config/cfg/Settings.pxt
fi

/ptokax/PtokaX -c /config
