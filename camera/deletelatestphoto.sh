#!/bin/bash

error() {
  echo "$1";
  exit 1;
}

[ ! -z $1 ] || error "Interface not set."

if [ $1 == "local" ]
then
  latest=`curl http://10.5.5.9:8080/videos/DCIM/100GOPRO/ | tail -n 2 | grep -o 'GOPR0.*JPG"' | sed 's/"$//'`
  # remove the photo locally (it still exists on the gopro)
  echo "Deleting latest photo."
  rm "camera/photos/$latest"
else
  interface=$1
  # get the name of the most recently taken photo on the gopro
  latest=`curl http://10.5.5.9:8080/videos/DCIM/100GOPRO/ --interface $interface | tail -n 2 | grep -o 'GOPR0.*JPG"' | sed 's/"$//'`
  # remove the photo locally (it still exists on the gopro)
  echo "Deleting latest photo."
  rm "camera/photos/$latest"
fi
