#!/bin/sh

FROM=${1}
TO=${2}

if [ -f "${FROM}.nfer" ]; then
  if [ ! -z ${TO} ]; then
  
    if [ ! -f "${TO}.nfer" ]; then
      cp -i "${FROM}.nfer" "${TO}.nfer"
      cp -i "${FROM}.events" "${TO}.events"
      cp -i "${FROM}.result" "${TO}.result"
    else
      echo "Destination test already exists"
      exit 1
    fi
  else
    echo "Specify a destination name"
  fi
else
  echo "No test found from which to copy"
  exit 1 
fi

echo "done"