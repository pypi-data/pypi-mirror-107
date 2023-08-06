#!/bin/sh

DIR="$( cd "$( dirname "${0}" )" && pwd )"
BINARY="${1}"
RUNNER="${DIR}/functional/run_test.sh"
RESULT=0
OUTPUT="Test	Result\n--------------------	-------\n"
ESC=$(printf '\033')

for file in "${DIR}"/functional/*.nfer; do
  TEST=`echo $file | sed -e 's/.*\///' -e 's/.nfer$//'`
  OUTPUT="${OUTPUT}`${RUNNER} ${BINARY} ${TEST}`\n"
  if [ $? != 0 ]; then
    RESULT=1
  fi
done

echo -ne ${OUTPUT} | column -t -s"	 " | sed "1{N;s/\(.*\)\n/${ESC}[1m\1${ESC}[0m\n/}"

exit ${RESULT}
