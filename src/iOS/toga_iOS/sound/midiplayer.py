from toga_iOS.libs import AVMIDIPlayer, NSURL
from rubicon.objc import Block
from rubicon.objc.runtime import objc_id


class TogaMIDIPlayer(AVMIDIPlayer):
    pass


class MIDIPlayer:
    def __init__(self, interface, midi_data, sound_font, loop):
        self.interface = interface
        self.interface._impl = self
        self.native = None
        self.midi_data = midi_data
        self.loop = loop
        sound_font_url = None
        if isinstance(sound_font, NSURL):
            sound_font_url = sound_font
        elif sound_font:
            sound_font_url = NSURL.fileURLWithPath(str(sound_font))
        self.native = TogaMIDIPlayer.alloc().initWithData(self.midi_data, soundBankURL=sound_font_url, error=None)
        self.native.interface = self.interface

    def play(self):
        callback = None
        if self.loop:
            callback = Block(self.restart, None, objc_id)
        self.native.play(callback)

    def stop(self):
        self.native.stop(None)

    def restart(self, action: objc_id) -> None:
        if self.native.currentPosition >= self.native.duration - 0.02:
            self.native.currentPosition = 0
            self.play()

    @property
    def rate(self):
        return self.native.rate

    @rate.setter
    def rate(self, value):
        self.native.rate = value

    @property
    def current_time(self):
        return float(self.native.currentPosition)

    @current_time.setter
    def current_time(self, value):
        self.native.currentPosition = value

    @property
    def duration(self):
        return float(self.native.duration)

    @property
    def playing(self):
        return self.native.playing
