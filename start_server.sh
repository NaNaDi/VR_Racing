#!/bin/bash

# get directory of script
DIR="$( cd "$( dirname "$0" )" && pwd )"

# assuming a local guacmole version is located properly
#LOCAL_GUACAMOLE="$DIR/../../../guacamole"
#LOCAL_AVANGO="$DIR/../../../avango"

# if not, this path will be used
GUACAMOLE=/opt/guacamole/master
AVANGO=/opt/avango/master

# third party libs
#export LD_LIBRARY_PATH=/opt/boost/boost_1_55_0/lib:/opt/zmq/current/lib:/opt/Awesomium/lib:/opt/pbr/inst_cb/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/boost/current/lib:/opt/openscenegraph/3.0.1/lib64/:/opt/zmq/current/lib:/opt/pbr/inst_cb/lib:/opt/Awesomium/lib:/opt/OculusSDK/currentSDK2/LibOVR/Lib/Linux/x86_64/Release

# schism
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/schism/current/lib/linux_x86

# avango
#export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH:/opt/pbr/inst_cb/lib:/opt/Awesomium/lib
export LD_LIBRARY_PATH="$LOCAL_AVANGO/lib":$AVANGO/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$AVANGO/lib/python3.5

# guacamole
export LD_LIBRARY_PATH="$LOCAL_GUACAMOLE/lib":$GUACAMOLE/lib:$LD_LIBRARY_PATH


# run daemon
python3 ./daemon.py > /dev/null &
#python3 daemon.py

# run program
#cd "$DIR" && python3.4 ./main.py
cd "$DIR" && DISPLAY=:0.0 python3 ./server.py $1

# kill daemon
kill %1

