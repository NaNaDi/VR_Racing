#!/bin/bash

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

# assuming a local guacmole version is located properly
LOCAL_GUACAMOLE="$DIR/../../../guacamole"
LOCAL_AVANGO="$DIR/../../../avango"

# if not, this path will be used
GUACAMOLE=/opt/guacamole/master
AVANGO=/opt/avango/master

# third party libs
export LD_LIBRARY_PATH=/opt/boost/current/lib:/opt/zmq/current/lib:/opt/Awesomium/lib:/opt/pbr/inst_cb/lib

# schism
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/bernste4/src/schism/lib/linux_x86

# avango
export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH:/opt/pbr/inst_cb/lib:/opt/Awesomium/lib
export PYTHONPATH="$LOCAL_AVANGO/lib/python3.4":"$LOCAL_AVANGO/examples":$AVANGO/lib/python3.4:$AVANGO/examples

# guacamole
export LD_LIBRARY_PATH="$LOCAL_GUACAMOLE/lib":$GUACAMOLE/lib:$LD_LIBRARY_PATH

# run program
if [[ $* == *-d* ]]
then
cd "$DIR" && gdb --args python3.4 ./main.py
else
cd "$DIR" && python3.4 ./main.py
fi

# kill daemon
kill %1
