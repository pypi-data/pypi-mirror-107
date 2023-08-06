#!/bin/sh

DIR="$( cd "$( dirname "${0}" )" && pwd )"

BINARY="${1}"
TEST="${2}"

echo -n "${TEST}	"

"${BINARY}" "${DIR}/${TEST}.nfer" < "${DIR}/${TEST}.events" | diff -w - "${DIR}/${TEST}.result" > /dev/null

RETURN=$?

if [ ${RETURN} = 0 ]; then
  echo "\e[32m[PASS]\e[0m"
else
  echo "\e[1;31m[FAIL]\e[0m"
fi

exit ${RETURN}
