import json
import numpy as np
import sounddevice
import wave
import struct

import waveimport


# GLOBAL VARIABLES
PRJ_PATH = './db/projects/'
PRJ_FILE = 'songs.json'
FRAMERATE = waveimport.FRAMERATE


# OBJECTS ARE Sample, Track, Song AND Songs
class Sample:

    def __init__(self, data):
        self.__data = data

    @property
    def data(self):
        return self.__data

    # FITS THE SAMPLE TO THE DURATION REQUIRED BY PATTERN AND APPLIES AMPLITUDE
    def fit(self, nframes, amplitude):

        if amplitude == 'X':

            if nframes < self.data.shape[0]:
                data = self.data[:nframes]

            elif nframes > self.data.shape[0]:
                data = np.append(self.data, np.zeros(nframes - self.data.shape[0]))

            else:
                data = self.data

        else:

            try:

                if nframes < self.data.shape[0]:
                    data = self.data[:nframes]
                    data = np.multiply(data, int(amplitude) / 10)

                elif nframes > self.data.shape[0]:
                    data = np.append(self.data, np.zeros(nframes - self.data.shape[0]))
                    data = np.multiply(data, int(amplitude) / 10)

                else:
                    data = np.multiply(self.data, int(amplitude) / 10)

            except ValueError:
                raise ValueError("AMPLITUDE VALUE MUST BE INTEGER 1-9 OR X")

        data = data.astype(np.float32)
        return data


class Track:

    def __init__(self, sampledata, pattern, trigger):
        self.__sample = Sample(sampledata)
        self.__trigger = trigger
        self.__pattern = pattern.replace('|', '')
        self.__patterns = ''
        self.__getpatterns()
        self.__data = np.empty(0, dtype=np.float32)
        self.__make()

    @property
    def sample(self):
        return self.__sample

    @property
    def trigger(self):
        return self.__trigger

    @property
    def pattern(self):
        return self.__pattern

    @property
    def patterns(self):
        return self.__patterns

    @property
    def data(self):
        return self.__data

    def __getpatterns(self):

        for i in self.pattern:

            if i == '.':
                self.__patterns += i

            else:
                self.__patterns += '|{}'.format(i)

        self.__patterns = self.patterns.split('|')
        self.__patterns = [i for i in self.patterns if i != '']

    def __make(self):

        for i in range(len(self.patterns)):

            length = len(self.patterns[i]) * self.trigger

            if self.patterns[i].startswith('.'):
                amplitude = 0

            else:
                amplitude = self.patterns[i][0]

            part = self.sample.fit(length, amplitude)
            self.__data = np.append(self.data, part)


class Song:

    def __init__(self, name):
        with open('{}{}'.format(PRJ_PATH, PRJ_FILE), 'r') as songsfile:

            song = json.load(songsfile)[name]

            self.__name = name
            self.__nchannels = song['Channels']
            self.__beat = len(song['Beat'])
            self.__repeat = song['Repeat']
            self.__tracks = song['Tracks']
            self.__tempo = song['Tempo']
            self.__trigger = int(60 / song['Tempo'] * FRAMERATE / self.beat)

        self.__channels = {}
        self.__length = None
        self.__maketracks()

        self.__data = None
        self.__makedata()

    def __str__(self):
        return "\n"\
<<<<<<< HEAD
               "Name:      {}\n" \
=======
               "Name:      {}\n"\
               "Tempo:     {}\n" \
>>>>>>> 08a533d243a627558d446cda61698ea2c028af08
               "Channels:  {}\n" \
               "Tracks:    {}\n" \
               "Tempo:     {}\n" \
               "Repeat:    {}\n" \
               "".format(
                self.name,
                self.tempo,
                self.nchannels,
                len(self.tracks),
                self.tempo,
                self.repeat)

    @property
    def name(self):
        return self.__name

    @property
    def tempo(self):
        return self.__tempo

    @property
    def nchannels(self):
        return self.__nchannels

    @property
    def beat(self):
        return self.__beat

    @property
    def repeat(self):
        return self.__repeat

    @property
    def tracks(self):
        return self.__tracks

    @property
    def tempo(self):
        return self.__tempo

    @property
    def trigger(self):
        return self.__trigger

    @property
    def channels(self):
        return self.__channels

    @property
    def length(self):
        return self.__length

    @property
    def data(self):
        return self.__data

    def __maketracks(self):

        # GENERATE EACH TRACK
        for t in self.tracks:

            samplename = self.tracks[t].get('SampleName')
            pattern = ''.join(self.tracks[t].get('Pattern'))
            align = self.tracks[t].get('Align')

            samplefile = samplename + '.wav'
            sampledata = waveimport.import_file_mono(samplefile)

            track = Track(sampledata[samplename], pattern, self.trigger)

            self.__channels.update({t: {"Align": align, "Data": track.data}})

            if self.length is None:
                self.__length = track.data.shape[0]

    def __makedata(self):

        # CONCENTRATE TRACKS PER CHANNEL TO PLAYABLE AND RECORDABLE DATA
        if self.nchannels == 2:

            left, l = np.zeros((self.length,), dtype=np.float32), 0
            right, r = np.zeros((self.length,), dtype=np.float32), 0

            for track, trackvalue in self.channels.items():

                if trackvalue['Align'] == 'L':

                    left += trackvalue['Data']
                    l += 1

                elif trackvalue['Align'] == 'R':

                    right += trackvalue['Data']
                    r += 1

                elif trackvalue['Align'] == 'C':

                    left += trackvalue['Data']
                    right += trackvalue['Data']
                    l += 1
                    r += 1

                else:
                    raise ValueError("CHANNEL CAN ONLY BE EITHER ['L', 'R', 'C']")

            left = np.divide(left, l).astype(np.float32)
            right = np.divide(right, r).astype(np.float32)

            self.__data = np.empty((self.length * 2), dtype=np.float32)
            self.__data[0::2] = left
            self.__data[1::2] = right

        else:

            mono = np.zeros((self.length,), dtype=np.float32)

            for track, trackvalue in self.channels.items():
                mono += trackvalue['Data'] / len(self.channels)

            self.__data = mono


class Songs:

    def __init__(self):
        with open('{}{}'.format(PRJ_PATH, PRJ_FILE), 'r') as songsfile:

            self.songs = list(json.load(songsfile).keys())


# FUNCTIONAL PART OF SONG
def play(channels, data, framerate, rep=1):

    if channels != 1:

        datarep = data

        for j in range(rep - 1):
            datarep = np.append(datarep, data)

        datarep = np.reshape(datarep, (-1, channels))

    else:

        datarep = data

        for j in range(rep - 1):
            datarep = np.append(datarep, data)

    sounddevice.play(datarep, framerate)
    sounddevice.wait()


def record(name, channels, data, framerate, rep=1):

    with wave.open('{}{}.wav'.format(PRJ_PATH, name), 'wb') as output:
        output.setparams((channels, 2, framerate, 0, 'NONE', 'not compressed'))

        data.astype(np.float16)
        values = []
        for j in range(rep):
            for l in range(0, len(data)):

                    value = int(data[l] * 32767)
                    packed_value = struct.pack('h', value)
                    values.append(packed_value)

        value_str = b''.join(values)

        output.writeframes(value_str)
