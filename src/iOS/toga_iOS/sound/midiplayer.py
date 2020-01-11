from toga_iOS.libs import AVMIDIPlayer, NSURL


class TogaMIDIPlayer(AVMIDIPlayer):
    pass


class MIDIPlayer:
    def __init__(self, interface, midi_data, sound_font):
        self.interface = interface
        self.interface._impl = self
        self.native = None
        self.midi_data = midi_data
        sound_font_url = None
        if isinstance(sound_font, NSURL):
            sound_font_url = sound_font
        elif sound_font:
            sound_font_url = NSURL.fileURLWithPath(str(sound_font))
        self.native = TogaMIDIPlayer.alloc().initWithData(self.midi_data, soundBankURL=sound_font_url, error=None)
        self.native.interface = self.interface

    def play(self):
        self.native.play(None)

    def stop(self):
        self.native.stop(None)

    @property
    def rate(self):
        return self.native.rate

    @rate.setter
    def rate(self, new_rate):
        self.native.rate = new_rate

    @property
    def current_time(self):
        return float(self.native.currentPosition)

    @current_time.setter
    def current_time(self, new_current_time):
        self.native.currentPosition = new_current_time

    @property
    def duration(self):
        return float(self.native.duration)

    @property
    def playing(self):
        return self.native.playing
