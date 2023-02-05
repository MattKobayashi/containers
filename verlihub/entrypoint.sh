#!/bin/bash
MODE=${1:---run}

if [ ${MODE} = "--install" ]
    then
        /usr/local/bin/vh --install

elif [ ${MODE} = "--run" ]
    then
        /usr/local/bin/verlihub

fi