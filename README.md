# scac - the Simplified Command and Control

## Introduction

This is my attempt at a minimalist speech recognition program.  My original intent is to develop a platform for voice activation of bespoke scientific instrumentation.  It is inspired by systems such as [Jasper]() but with much less overhead (and in all likelihood, correspondingly less functionality).

## Installation

I am assuming the hardware is a Raspberry Pi version 2 running Raspian Jessie with a USB microphone.  The only additional packages that need to be installed are pocketsphinx and espeak:
```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install pocketsphinx espeak
```
Once the installation is complete, this repository can be cloned using `git clone https:\\github.com\bobthechemist\scc.git`

## Setup

You should make sure that your system is capable of playing and recording sound.  As far as I can tell, if you can successfully hear audio with `aplay` and record audio with `arecord` then scac should work for you.  Note, you do not need to play games with default audio devices and re-ording the loading of modules.  On a clean install, you will need to use `sudo raspi-config` to ensure that audio (under Advanced options) is being directed to your sound system of choice (I'm testing on the 3.5 mm jack). Additionally, your microphone device address is likely plughw:1,0.  If so, you need not change any of the scripts here.

scac relies on a named pipe for transferring speech-to-text (STT) information from the STT engine (Pocketsphinx) to the main python script.  In order to have a persistent connection to the STT engine, I am using a non-blocking pipe implementation called ftee that is [taken from here]().  You will have to compile it by navigating to the asset subdirectory and typing `gcc -o ftee ftee.c`.  You may keep the executable in the asset directory; however scac assumes that it is in your path, so it might be best to move it to a folder already in your path or to modify `startspeechpipe.sh` to point to the full path of ftee.

Make a named pipe by running `mkfifo /tmp/speech`.  Feel free to use a different location, just change PIPENAME in `startspeechpipe.sh`.

### Creating the language model and associated functions

You will need a set of commands and the (python) functions corresponding to those commands.  I've created a script to simplify the language model creation.  First, create a text file with the command you wish to have recognized (no punctuation, in all caps) followed by a comma and the name of the python function that will be called.  The file will look something like this:

```
# Comments are allowed, but only on a line by themselves.
TURN ON LIGHT, ledOn
SHUT OFF LIGHT, ledOff
# You must choose your own keyphrase, which will be indicated by the 'function' keyphrase
LISTEN TO ME, keyphrase
```

I assume that the name of this file ends with ".info" and is located in the assets directory. When it is completed, run `./makemodel.sh <file>.info` and we will use CMU's lmtool to create the language model and dictionary.  Whatever four-digit number is assigned to your .lm and .dic files must be entered into the CORPUS variable in `startspeechpipe.sh`

Custom functions that are associated with your commands will be placed in the library subdirectory.  Define the functions in some myfunctions.py file and then be sure to import the functions in `main.py` using:

```
from library.myfunctions import *
```

(Note: I'm not a python programmer - heck, I'm not a programmer at all, so if you cringe at what I've written here, please feel free to get in touch with me and propose some suggestions.)

Lastly, edit `main.py` to set your preferred text-to-speech (TTS) engine.  Right now, your options are "textonly" and "espeak".  The former is useful when you don't want to make a lot of noise.  My wife is finishing up her dissertation, and our desks are in the same office; therefore, making noise right now is *NOT* an option.

## Operation
First, start the STT engine with `startspeechpipe.sh`.  In addition to writing to the pipe, all recognized speech is sent to a logfile which is useful for debugging purposes.  You can change the value of LOG to "/dev/null" if you don't want the log or (as I do) /dev/stdout if you have a terminal dedicated to watching this stream.

Next, start scac with `python main.py` (filename will change eventually.)  You should see some informational messages, and a quick sanity check, which makes sure there are functions associated with each of the commands.  At this point, it deletes any orphaned commands.  The program then waits for the keyphrase at which point it will listen for an actual command.  Press CTRL-c to end the program. To stop the STT engine, type `killall pocketsphinx_continuous`.

## Next steps
Yup, that's it for the moment.  Before adding features I want to refactor, and test a proof-of-concept design to ensure that the system as I've designed it will work for my purposes.

