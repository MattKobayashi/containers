#!/bin/bash

sleep $[RANDOM\%300] ; cd /home/peeringdb-mirror/ ; touch peeringdb.sync.log ; date >> peeringdb.sync.log ; poetry run peeringdb sync >> peeringdb.sync.log 2>&1
