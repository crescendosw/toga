from toga.platform import get_platform_factory


class MIDIPlayer:
    def __init__(self, midi_data, sound_font=None, factory=None):
        self.factory = get_platform_factory(factory)
        self._impl = self.factory.MIDIPlayer(interface=self, midi_data=midi_data, sound_font=sound_font)

    def play(self):
        self._impl.play()

    def stop(self):
        self._impl.stop()

    @property
    def rate(self):
        return self._impl.rate

    @rate.setter
    def rate(self, new_rate):
        if new_rate == 0:
            raise ZeroDivisionError
        self._impl.rate = new_rate

    @property
    def current_time(self):
        return float(self._impl.current_time)

    @current_time.setter
    def current_time(self, new_current_time):
        self._impl.current_time = new_current_time

    @property
    def duration(self):
        return float(self._impl.duration)

    @property
    def playing(self):
        return self._impl.playing
