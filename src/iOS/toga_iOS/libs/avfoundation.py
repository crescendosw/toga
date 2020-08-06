##########################################################################
# System/Library/Frameworks/AVFoundation.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################
avfoundation = cdll.LoadLibrary(util.find_library('AVFoundation'))
media_player = cdll.LoadLibrary(util.find_library('MediaPlayer'))
######################################################################

######################################################################
# NSBundle.h
AVMIDIPlayer = ObjCClass('AVMIDIPlayer')
AVAudioSession = ObjCClass('AVAudioSession')
AVAudioSessionCategoryPlayback = 'AVAudioSessionCategoryPlayback'
CommandCenter = ObjCClass('MPRemoteCommandCenter')
