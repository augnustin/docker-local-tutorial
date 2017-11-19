#!/bin/bash

# echo "$(cat pitchme/scss/theme-override.scss)"
FILE_CONTENT=$(sed -E ':a;N;$!ba;s/\r{0,1}\n/\\n/g' pitchme/scss/theme-override.scss)
# echo $FILE_CONTENT
COMMAND="curl 'https://www.sassmeister.com/app/3.4/compile' -g -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{\"input\":\"$FILE_CONTENT\",\"compiler\":\"3.4\",\"syntax\":\"scss\",\"original_syntax\":\"scss\",\"output_style\":\"expanded\"}'"
# echo $COMMAND

JSON=$(eval $COMMAND)

echo $JSON | python -c 'import json,sys;obj=json.load(sys.stdin);print obj["css"]' > pitchme/css/theme-override.css
