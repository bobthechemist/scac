import os
from helper import *
def textonly(string):
  print col.PURPLE + string + col.NONE

def espeak(string):
  os.system('espeak -ven-us+f2 "{0}" 2>/dev/null'.format(string))


