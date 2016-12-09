import numpy as np
import os
import scipy.io.wavfile as wav
import scipy.signal as signal


# GLOBAL VARIABLES
SMP_PATH = './db/samples/'
FRAMERATE = 44100


# OBJECTS ARE Wavefile AND Resample. NORMALIZED IMPORT
class Wavefile:

    def __init__(self, path):
        self.__path = path
        self.__name = os.path.split(self.path)[1][:-4]
        self.__framerate = None
        self.__nframes = None
        self.__nchannels = None
        self.__data = None
        self.__datatype = None
        self.__readwave()
        self.__getnchannels()
        self.__normalize()

    def __str__(self):
        return "Name:      {}\n"\
               "Path:      {}\n"\
               "Framerate: {}\n"\
               "Frames:    {}\n"\
               "Channels:  {}\n" \
               "Datatype:  {}\n" \
               "Data:  \n{}\n"\
               "".format(
                self.name,
                self.path,
                self.framerate,
                self.nframes,
                self.nchannels,
                self.datatype,
                self.data)

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        return self.__name

    @property
    def framerate(self):
        return self.__framerate

    @property
    def nframes(self):
        return self.__nframes

    @property
    def nchannels(self):
        return self.__nchannels

    @property
    def data(self):
        return self.__data

    @property
    def datatype(self):
        return self.__datatype

    def __readwave(self):

        try:
            self.__framerate, self.__data = wav.read(self.path)
            self.__nframes = self.data.shape[0]
            self.__datatype = self.data.dtype

        except ValueError as ve:
            print("{}.wav: {}".format(self.name, ve))

    def __getnchannels(self):

        try:
            self.__nchannels = self.data.shape[1]

        except IndexError:
            self.__nchannels = 1

    def __normalize(self):

        datatypes = ['uint8', 'int16', 'int32', 'float32']
        divisors = [255., 32768., 2147483648., 1.]

        try:
            divisor = divisors[datatypes.index(self.datatype)]

            if self.datatype == 'uint8':
                self.__data = np.multiply(np.subtract((np.divide(self.data, divisor)), 0.5), 2).astype(np.float32)

            else:
                self.__data = np.divide(self.data, divisor).astype(np.float32)

        except IndexError as e:
            print("{}: DATATYPE {} OF {} NOT SUPPORTED\n".format(e, self.datatype, self.name))

        self.__datatype = self.data.dtype

    def getchannel(self, channel):

        self.__name = os.path.split(self.path)[1][:-4]
        self.__name = '{}_ch_{}'.format(self.name, str(channel))

        return self.data[:, channel]

    def monosum(self):

        self.__name = os.path.split(self.path)[1][:-4]

        return np.divide(np.sum(self.data, axis=1), self.nchannels)


class ReSample:

    def __init__(self, name, in_rate, out_rate, data):
        self.__name = name
        self.__framerate = in_rate
        self.__data = data
        self.__nframes = data.shape[0]
        self.__resample(in_rate, out_rate)

    def __str__(self):
        return "Name:      {}\n"\
               "Framerate: {}\n"\
               "Frames:    {}\n" \
               "Datatype:  {}\n" \
               "Range:     {:.2f} | {:.2f}\n" \
               "Data: \n{}\n" \
               "".format(
                self.name,
                self.framerate,
                self.nframes,
                self.data.dtype,
                min(self.data),
                max(self.data),
                self.data)

    @property
    def name(self):
        return self.__name

    @property
    def framerate(self):
        return self.__framerate

    @property
    def nframes(self):
        return self.__nframes

    @property
    def data(self):
        return self.__data

    def __resample(self, in_rate, out_rate):

        if in_rate != out_rate:
            self.__data = signal.resample(self.data, int(self.nframes * out_rate / in_rate))
            self.__framerate = out_rate

        self.__data = np.divide(self.data, max(abs(self.data))).astype(np.float32)
        self.__nframes = self.data.shape[0]


# FUNCTIONAL PART OF WAVEIMPORT
def import_folder(folder=''):
    """
    :param folder: ENTER FOLDER TO BE IMPORTED RELATIVE TO './db/samples/'
    :return: DICT OF SAMPLES
    FOLDER IMPORT ONLY SUPPORTS MONO SUM IMPORT OF STEREO FILES
    """

    path = SMP_PATH + str(folder)
    smpls = {}
    nosmpls = []
    i = 0

    for root, dirs, files in os.walk(path):
        for file in files:

            if file.endswith('.wav'):
                try:
                    s = Wavefile(os.path.join(root, file))

                except (AttributeError, ValueError):
                    s = file
                    nosmpls.append(s)
                    i += 1

                else:
                    if s.nchannels == 1:
                        s = ReSample(s.name, s.framerate, FRAMERATE, s.data)

                    else:
                        s = ReSample(s.name, s.framerate, FRAMERATE, s.monosum())

                    smpls.update({s.name: s.data})
                    i += 1

    print("\nFILES:        ", i)
    print("SAMPLES:      ", len(smpls))
    print("NOT IMPORTED: ", nosmpls)
    print()
    return smpls


def import_file_mono(wavefile, folder=SMP_PATH):
    """
    :param wavefile: A SPECIFIC WAVE FILE IN FOLDER
    :param folder: STANDARD FOLDER IS SAMPLES FOLDER. OTHER FOLDERS CAN BE ACCESSED
    :return: DICT OF 1 MONOSUMMED SAMPLE
    """

    smpl = None

    for root, dirs, files in os.walk(folder):

        if str(wavefile) in files:
            try:
                s = Wavefile(os.path.join(root, str(wavefile)))

            except (AttributeError, ValueError):
                smpl = "NOT ABLE TO IMPORT FILE: {}".format(str(wavefile))
                break

            else:
                if s.nchannels == 1:
                    s = ReSample(s.name, s.framerate, FRAMERATE, s.data)

                else:
                    s = ReSample(s.name, s.framerate, FRAMERATE, s.monosum())

                smpl = {s.name: s.data}

    if smpl is None:
        print("FILE NOT FOUND : {}".format(str(wavefile)))

    elif type(smpl) == dict:
        print("IMPORTED FILE: {}".format(str(wavefile)))

    return smpl


def import_channel(wavefile, channel, folder=SMP_PATH):
    """
    THIS FUNCTION REMAINS UNUSED IN THE BEATS PROCEDURE
    :param wavefile: A SPECIFIC WAVE FILE IN FOLDER
    :param channel: 0 OR 1 for left or right channel
    :param folder: STANDARD FOLDER IS SAMPLES FOLDER. OTHER FOLDERS CAN BE ACCESSED
    :return: DICT OF 1 CHANNEL OF THE SAMPLE
    """

    smpl = None

    for root, dirs, files in os.walk(folder):

        if str(wavefile) in files:
            try:
                s = Wavefile(os.path.join(root, str(wavefile)))

            except (AttributeError, ValueError):
                smpl = "NOT ABLE TO IMPORT FILE: {}".format(str(wavefile))
                break

            else:
                if s.nchannels == 1:
                    s = ReSample(s.name, s.framerate, FRAMERATE, s.data)

                else:
                    s = ReSample(s.name, s.framerate, FRAMERATE, s.getchannel(channel))

                smpl = {s.name: s.data}

    if smpl is None:
        print("FILE NOT FOUND : {}".format(str(wavefile)))

    elif type(smpl) == dict:
        print("IMPORTED FILE: {}".format(str(wavefile)))

    return smpl
