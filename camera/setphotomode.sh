#!/bin/bash

error() {
  echo "$1";
  exit 1;
}

[ ! -z $1 ] || error "Interface not set."

echo "Setting photo mode, linearFOV, and flat colour."
if [ $1 == "local" ]
then
  latest=`curl http://10.5.5.9:8080/videos/DCIM/100GOPRO/ | tail -n 2 | grep -o 'GOPR0.*JPG"' | sed 's/"$//'`
  # set linear FOV
  curl http://10.5.5.9/gp/gpControl/setting/4/4
  # set photo mode
  curl http://10.5.5.9/gp/gpControl/command/mode?p=1
else
  interface=$1
  # get the name of the most recently taken photo on the gopro
  latest=`curl http://10.5.5.9:8080/videos/DCIM/100GOPRO/ --interface $interface | tail -n 2 | grep -o 'GOPR0.*JPG"' | sed 's/"$//'`
  # set linear FOV
  curl http://10.5.5.9/gp/gpControl/setting/4/4 --interface $interface
  # set photo mode
  curl http://10.5.5.9/gp/gpControl/command/mode?p=1 --interface $interface
fi
