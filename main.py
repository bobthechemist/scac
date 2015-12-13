from base import *
from base.helper import *
# Here we need to explicitly state which modules in the library are being used
from library.detector import *
from library.source import *
import os

# base name of the corpus (don't include .info suffix)
corpus = "simple"

# Define the TTS engine
say = tts.textonly

# Connect functions to commands
print "*** Creating command function dictionary" 
fdict = {}
with open("assets/"+corpus+".info") as raw:
  for line in raw:
    if line[0] != '#':
      cmd, func = line.partition(",")[::2]
      fdict[cmd.rstrip()]=func.strip()

# Checking if there exists a function for each command, remove command if not
# Cannot modify a dictionary while iterating, so make a copy
print "*** Checking dictionary"
for k,v in fdict.copy().iteritems():
  if v in locals().keys():
    print " - found", k, "which calls", v
  else:
    if v=='keyphrase':
      print " - found keyphrase"
      keyphrase = k
    else:
      print col.RED + " - no function found for", k,"(",v,")", \
        "deleting" + col.NONE
      del fdict[k]


# Should be able to do this in previous loop.
keyphrase = "None found!"
for cmd, func in fdict.iteritems():
  if func=='keyphrase':
    keyphrase = cmd
# Add test and bail here
print "*** The keyphrase is:", keyphrase

# Open the speech pipe; should have default config file with this filename
#   since it is also needed to start pocketsphinx
spipe = open('/tmp/speech')

try:
  while True:
    waiting = True
    while waiting:
      line = spipe.readline().rstrip()
      if line == keyphrase: 
        waiting = False
        say("Yes?")

    line = spipe.readline().rstrip()
    try:
      say(locals()[fdict[line]]())
    except KeyError:
      say("I do not understand")
      print line
except KeyboardInterrupt:
  print "Stopping"

print "closing file"

spipe.close()



