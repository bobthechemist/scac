#!/bin/sh

PIPENAME=/tmp/speech
FTEELOC=/home/pi/bin/ftee
ADCDEV=plughw:1,0
CORPUS=simple
#LOG=/tmp/speech.log
LOG=/dev/stdout
if [ ! -p $PIPENAME ]
  then
    echo "$PIPENAME either does not exist or is not a named pipe."
    echo "Make the pipe on your own with the command mkfifo $PIPENAME."
    echo "Exiting..."
    exit
fi

# The sed filter is only appropriate for pocketsphinx 0.8-5.  Later versions have different output formats.  
pocketsphinx_continuous -adcdev $ADCDEV -logfn /dev/null -lm $CORPUS.lm -dict $CORPUS.dic 2>/dev/null | sed --unbuffered -n 's/^[0-9: ]\{11\}\(.*\)/\1/p' | $FTEELOC $PIPENAME > $LOG & 
