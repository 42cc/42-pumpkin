!/bin/bash

COMMAND="$*"

eval "$COMMAND"

if [ $? -eq 0 ]
then
   eval 'notify-send -t 5 "$COMMAND Done!"'
else
   eval 'notify-send -t 5 "$COMMAND Failed!"'
fi
