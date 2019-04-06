#!/bin/bash

error() {
  echo "$1";
  exit 1;
}

[ ! -z $1 ] || error "Interface not set."

echo "Downloading latest photo."
if [ $1 == "local" ]
then
  latest=`curl http://10.5.5.9:8080/videos/DCIM/100GOPRO/ | tail -n 2 | grep -o 'GOPR0.*JPG"' | sed 's/"$//'`
  # append the name of the photo to download to the end of url to curl
  path="http://10.5.5.9:8080/videos/DCIM/100GOPRO/$latest"
  # download the photo
  curl "$path" -o "camera/photos/$latest"
else
  interface=$1
  # get the name of the most recently taken photo on the gopro
  latest=`curl http://10.5.5.9:8080/videos/DCIM/100GOPRO/ --interface $interface | tail -n 2 | grep -o 'GOPR0.*JPG"' | sed 's/"$//'`
  # append the name of the photo to download to the end of url to curl
  path="http://10.5.5.9:8080/videos/DCIM/100GOPRO/$latest"
  # download the photo
  curl "$path" -o "camera/photos/$latest" --interface $interface
fi
