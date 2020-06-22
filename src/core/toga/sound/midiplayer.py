from toga.platform import get_platform_factory


class MIDIPlayer:
    def __init__(self, midi_data, sound_font=None, factory=None, loop=False):
        self.factory = get_platform_factory(factory)
        self._impl = self.factory.MIDIPlayer(interface=self, midi_data=midi_data, sound_font=sound_font, loop=loop)

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
