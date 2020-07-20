from toga.platform import get_platform_factory


class MIDIPlayer:
    def __init__(self, midi_sample, sound_font=None):
        self.factory = get_platform_factory()
        self._impl = self.factory.MIDIPlayer(interface=self, midi_sample=midi_sample, sound_font=sound_font)

    def set_sample(self, midi_sample, sound_font=None):
        self._impl.set_sample(midi_sample, sound_font=sound_font)

    def play(self):
        self._impl.play()

    def stop(self):
        self._impl.stop()

    def delete(self):
        self._impl.delete()

    @property
    def rate(self):
        return self._impl.rate

    @rate.setter
    def rate(self, value):
        if value == 0:
            raise ZeroDivisionError
        self._impl.rate = value

    @property
    def current_time(self):
        return float(self._impl.current_time)

    @current_time.setter
    def current_time(self, value):
        self._impl.current_time = value

    @property
    def duration(self):
        return float(self._impl.duration)

    @property
    def playing(self):
        return self._impl.playing

    @property
    def loop(self):
        return self._impl.loop

    @loop.setter
    def loop(self, value):
        self._impl.loop = value
